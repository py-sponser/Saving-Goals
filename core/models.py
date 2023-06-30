from django.db import models
from django.contrib.auth.models import AbstractUser
from core.managers import UserSignUpManager
from datetime import datetime
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserSignUpManager()


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    date = models.DateField()
    monthly_deposit_amount = models.FloatField(null=True)
    current_date = models.DateField(null=True)

    def calculate_monthly_deposit_amount(self, target_date, current_date, total_amount):
        total_months = diff_month(target_date, current_date)
        self.monthly_deposit_amount = round(total_amount/total_months, 2)
        self.save()
