import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,  force_str, DjangoUnicodeDecodeError
from .utils import token_generator 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.core.validators import EmailValidator
from django.http import JsonResponse
# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/reg.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        constext = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(email = email).exists():
            if not User.objects.filter(username = username).exists():
                if len(password) > 5:
                    user = User.objects.create_user(username = username, email = email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()

                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    token = token_generator.make_token(user)
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs= {"uidb64":uidb64, "token":token})
                    active_url = "http://" + domain + link
                    
                    email_subject = "Progress Tracker Account Activation"
                    email_body = ("Hello " + username+  ", \n Use this link to activate your account. \n" + active_url)
                    email_body = "\n".join(email_body)
                    email = EmailMessage(
                        email_subject, 
                        email_body,
                        'noreply@semicolon.com',
                        [email],
                    )
                    
                    email.send(fail_silently=False)
                    messages.success(request, 'Successfully registered. Check your email for an activation link and login to your account. See you soon!')
                    
                    return render(request, 'auth/login.html')
                else:
                    messages.error(request, 'Password length should be at least 6')
                    return render(request, 'auth/reg.html')
            else:
                messages.error(request, 'Username already exists. Choose another one please.')
                return render(request, 'auth/reg.html')
        else:
            return render(request, 'auth/login.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')



class Activation(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = id)

        if not token_generator.check_token(user, token):
            return redirect('/login/?message=not valid activation link')

            
        
        if user.is_active:
            return redirect('login')
        
        user.is_active = True
        user.save()
        
        return redirect('login')


class emailValidation(View):
    def post(self, request):
        data= json.loads(request.body)
        email = data['email']
        def valid_mail(email):
            validator = EmailValidator()
            try:
                validator(email)
                return True
            except:
                return False
        if not valid_mail(email):
            
            return JsonResponse({'emailError':True,}, status=400)
        
        return JsonResponse({'valid':True})

class passwordValidation(View):
    def post(self,request):
        data= json.loads(request.body)
        password = data['password']

        if len(password) < 6:
            
            return JsonResponse({'passwordError':True}, status=400)
        
        return JsonResponse({'valid':True})
    

class usernameValidation(View):
    def post(self,request):
        data= json.loads(request.body)
        username = data['username']

        if User.objects.filter(username == username).exists():
            
            return JsonResponse({'usernameError':True,}, status=400)
        
        return JsonResponse({'valid':True})

        
