from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login

# from .forms import CustomUserCreationForm, CustomLoginForm
from .models import CustomUser
from .cleaner import Cleaner, LoginCleaner, ForgotPass


def login_view(request):

    if request.method == 'POST' and request.POST.get('signup') == 'signup':

        user = CustomUser()

        # process the data in first_name= form.cleaned_data as required
        fullname = request.POST.get('fullname')
        email = request.POST.get('emailAddress')
        address = request.POST.get('address')
        bday = request.POST.get('bday')
        password = request.POST.get('password')
        question = request.POST.get('securityQuestion')
        answer = request.POST.get('securityAnswer')
        accountType = request.POST.get('accountType')

        s = Cleaner(fullname, bday, email)

        user.email = s.email_check()
        user.first_name, user.last_name = s.first_last_name()
        # print(user.first_name, user.last_name)
        user.birthday = bday
        user.securityquestion = question
        user.securityanswer = answer
        user.address = address
        user.usertype = accountType
        user.password = make_password(password)
        user.username = s.create_username()
        user.save()
        messages.success(request, "Sign up successfully!")
        # redirect to a new URL:
        return render(request, 'register/login.html')

    elif request.method == 'POST' and request.POST.get('forgotpassword') == 'forgotpassword':

        email = request.POST.get('emailAddress')

        f = ForgotPass(email)

        user = f.is_email_valid()

        if user is not None:
            user = CustomUser.objects.filter(email=email).get()
            context = {
                'user': user,
            }
            return render(request, 'register/forgot.html', context)
        else:
            return "Failed"

    elif request.method == 'POST' and request.POST.get('login') == 'login':

        email = request.POST.get('loginemail')
        password = request.POST.get('loginPassword')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                user = CustomUser.objects.filter(email=email).get()
                messages.info(request, "You are now logged in")
                return redirect('account')
        else:
            messages.error(request, "Invalid username or password.")

        # l = LoginCleaner(email, password)
        # user = l.user_check()

        # if user is not None:
        #     user = Users.objects.filter(email=email).get()
        #     user.is_authenticated = True
        #     user.save()
        #     id = user.id
        #     messages.info(request, "You are now logged in")
        #     context = {
        #         'id': id,
        #     }
        #     return render(request, 'accounting/home.html', context)
        # else:
        #     messages.error(request, "Invalid username or password.")

        context = {}
    return render(request, 'register/login.html', {})


def forgotpassword(request):
    pass


def logout_view(request):
    logout(request)
    messages.info(request, "You are now logged out")
    return redirect('/login')
