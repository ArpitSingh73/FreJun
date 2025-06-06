from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# from django.conf import settings
from django.conf import settings


# CustomUserModel = get_user_model()  # this gets your custom user model
# Create your models here.
class UserModel(AbstractUser):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Expense(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} on {self.date}"

    class Meta:
        ordering = ["-date"]  # Order by date descending
