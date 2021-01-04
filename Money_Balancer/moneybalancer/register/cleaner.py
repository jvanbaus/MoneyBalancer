from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import CustomUser


class Cleaner():
    def __init__(self, fullname, bday, email):
        self.fullname = fullname
        self.bday = bday
        self.email = email

    def email_check(self):
        r = CustomUser.objects.filter(email=self.email)
        if r.count():
            raise ValidationError("Email already exists")
        return self.email

    def first_last_name(self):
        firstname = self.fullname.strip().split(' ')[0]
        lastname = ' '.join((self.fullname + ' ').split(' ')[1:]).strip()
        return firstname, lastname

    def create_username(self):

        fname, lname = self.first_last_name()

        intial = fname[0].lower()
        lname = lname.lower()
        date = str(self.bday)
        username = (intial + lname + date[2:4] + date[5:7])
        return username


class LoginCleaner():

    def __init__(self, email, password):
        self.password = password
        self.email = email

    def user_check(self):
        r = CustomUser.objects.filter(email=self.email)

        if r.count() == 0:
            raise ValidationError("User not found")
            return None

        user = r.get(email=self.email)
        p_check = check_password(self.password, user.password)

        if not p_check:
            raise ValidationError("Incorrect Password")
            return None

        if not user.is_active:
            raise ValidationError("User is not active")
            return None

        return r


class ForgotPass():

    def __init__(self, email):
        self.email = email

    def is_email_valid(self):
        user = CustomUser.objects.filter(email=self.email)

        if user.count() == 0:
            raise ValidationError("User not found")
            return None

        return user
