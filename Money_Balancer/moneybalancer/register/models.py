from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    user_types = (
        (1, "Accountant"),
        (2, "Manager"),
        (3, "Admin"),
    )

    security_questions = (
        (1, "Whats is your mother maiden name?"),
        (2, "What is your favorite color?"),
        (3, "What is your biggest fear?"),
    )

    usertype = models.IntegerField(choices=user_types, default=1)
    approved = models.BooleanField(default=False)
    birthday = models.DateField(null=True)
    securityquestion = models.IntegerField(
        choices=security_questions, null=True)
    securityanswer = models.CharField(max_length=100, null=True)
    is_suspended = models.BooleanField(default=False)
    deactivetimestart = models.DateField(null=True, blank=True)
    deactivetimeend = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=250, blank=True)
