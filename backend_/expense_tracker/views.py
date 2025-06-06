from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Expense, UserModel
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ExpenseSerializer  # assuming it's already created
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.contrib.auth.hashers import make_password, check_password


@api_view(["POST"])
@csrf_exempt
def signup(request):
    data = request.data
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    print(f"User data for signup --> : {data}")

    try:
        if UserModel.objects.filter(email=email).exists():
            return Response(
                {"error": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = UserModel.objects.create(
            name=name,
            email=email,
            password=make_password(password),  # hash the password
        )
        return Response(
            {"message": "User added successfully"}, status=status.HTTP_201_CREATED
        )
    except Exception as e:
        print(f"Error during signu --->: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@csrf_exempt
def login(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    print(f"User data for login ---> {data}")

    try:
        user = UserModel.objects.get(email=email )  
        if not user: # if user exists -->
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if check_password(password, user.password): # if user exists and password matches -->
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User Logged in!",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response({"error": "Invalid credentials"}, status=401)
       
    except Exception as e:
        print(f"Error during login ---> {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def add_expense(request):
    if request.method == "POST": # if user wants to add expense -->
        data = request.data
        title = data.get("title")
        amount = data.get("amount")
        category = data.get("category")

        print(f"User data for adding expense: {data}")

        try:
            expense = Expense.objects.create(
                user=request.user,  # Comes from JWT 
                title=title,
                amount=amount,
                category=category,
            )
            serializer = ExpenseSerializer(expense)
            return Response(
                {"message": "Expense added successfully", "expense": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(f"Error during adding expense ---> {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET": # if user wants to get all expenses -->
        user = request.user
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "start_date and end_date query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            expenses = Expense.objects.filter(user=user, date__range=[start_date, end_date])
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error during fetching expenses ---> {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def expense_analytics(request):
    user = request.user
    period = request.GET.get("period", "daily")  # default to daily

    try:
        expenses = Expense.objects.filter(user=user)  # Fetch all user's expenses
        total = expenses.aggregate(total_amount=Sum("amount"))["total_amount"] or 0 # Total sum

        # Category-wise totals
        category_data = (
            expenses.values("category").annotate(total=Sum("amount")).order_by("-total")
        )

        # Determine time grouping
        if period == "weekly":
            trunc = TruncWeek("date")
        elif period == "monthly":
            trunc = TruncMonth("date")
        else:
            trunc = TruncDay("date")  # default to daily

        # Periodic trends
        trends = (
            expenses.annotate(period=trunc)
            .values("period")
            .annotate(total=Sum("amount"))
            .order_by("period")
        )

        return Response(
            {"total_expense": total, "category_breakdown": category_data, "trends": trends},
            status=200,
        )
    except Exception as e:
        print(f"Error during fetching analytics ---> {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)