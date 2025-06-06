from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class UserModel(AbstractUser):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} on {self.date}"

    class Meta:
        ordering = ["-date"]  # Order by date descending
