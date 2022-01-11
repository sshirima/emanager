from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str,  DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth

from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading

# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently= False)


class UserenameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should contains only alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry, username already in use, choose another one'},status=409)

        
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry, email already in use, choose another one'},status=409)

        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():

            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'Password, too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                #Send account activation email
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                token = token_generator.make_token(user)
                link = reverse('activate-account', kwargs={
                    'uidb64':uidb64,
                    'token':token,
                })
                activate_url = 'http://'+domain+link
                email_body = 'Hi '+user.username+', Please use below link to activate your account\n'+activate_url
                email_subject = 'Account activation email'

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'norepy@expenseswebsite.com',
                    [email]
                )
                EmailThread(email).start()
                messages.success(request, 'Account successful created')

                return render(request, 'authentication/register.html')
            else:
                messages.error(request, 'Email already exists')
        else:
            messages.error(request, 'Username already exists')

        return render(request, 'authentication/register.html', context)

class EmailVerificationView(View):

    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.info(request, 'User already activated')
                return redirect('login')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            messages.error(request, 'There was an error activating your account')
            print(str(ex))

        return redirect('login')

class LoginView(View):

    def get(self, request):
        return render(request, 'authentication/login.html')


    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:

            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Hello '+user.username+', you are now logged in!')
                    return redirect('expenses')

                messages.error('Your account is not activated, please activate the account first')
                return redirect('login')
            
            messages.error(request, 'Fail to authenticate username/password')
            return redirect('login')

        messages.error(request, 'Please fill all fields')
        return redirect('login')


class LogoutView(View):

    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')

    def post(self, request):

        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, "Email not valid")

            return render(request, 'authentication/reset_password.html', {'values': request.POST})

        user = User.objects.filter(email=email).first()
        print(user)
        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            token = PasswordResetTokenGenerator().make_token(user)
            link = reverse('set-new-password', kwargs={
                'uidb64':uidb64,
                'token':token,
            })

            reset_url = 'http://'+domain+link
            email_body = 'Hi there,  Please use below link to reset your password\n'+reset_url
            email_subject = 'Password reset instruction'
            

            email = EmailMessage(
                email_subject,
                email_body,
                'norepy@expenseswebsite.com',
                [email]
            )
            EmailThread(email).start()
        else:
            messages.error(request, 'Email does not exists')

        messages.success(request, 'Password reset link has been sent')

        return render(request, 'authentication/reset_password.html')
        

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, "Password link is invalid, please request a new one")
                return render(request, 'authentication/reset_password.html')
            
        except Exception as e:  
            print('Error, requesting password reset link: {}'.format(str(e)))
            messages.error(request, 'Something went wrong, please try again')
            return render(request, 'authentication/reset_password.html')

        return render(request, 'authentication/set_newpassword.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Password did not match')
            return render(request, 'authentication/set_newpassword.html', context)

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset succcess')

            return redirect('login')
        except Exception as e:  
            print('Error, reseting password: {}'.format(str(e)))
            messages.error(request, 'Something went wrong, please try again')
            return render(request, 'authentication/set_newpassword.html', context) 
        

        