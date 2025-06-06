from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("expense/", add_expense, name="expense"),
    path("expense/analytics/", expense_analytics, name="expense_analytics"),
]
