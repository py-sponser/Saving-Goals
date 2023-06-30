from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import Response, APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from core.permissions import IsNotAuthenticated
from rest_framework import permissions
from core.utils import *
from core.models import User, SavingGoal
from core.serializers import SavingsSerializer, SavingGoalsGetterSerializer
from django.contrib.auth import logout
# Create your views here.


class LoginView(TokenObtainPairView):
    permission_classes = (IsNotAuthenticated, )


@method_decorator(csrf_protect, name="dispatch")
class SignUpView(APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        # username = request.data.get("username")
        email = request.data.get("email")
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")

        if email and password1 and password2:
            if validate_email(email):  # if email satisfies requirements
                if password1 == password1:
                    # if password_requirements_validator(password1):  # if password satisfies requirements
                        if User.objects.filter(email=email).exists():  # checking if there's an account of same email
                            return Response({"email_exist": "[-] Email is already exist."})
                        else:
                            username = f"{email.split('@')[0]}{random.randint(1, 1000000000000)}"

                            # activation_code = generate_mail_code()
                            # reset_code = generate_mail_code()
                            # user = User.objects.create_user(username=username, email=email,
                            #                                 is_active=False, activation_code=activation_code,
                            #                                 password_reset_code=reset_code)
                            user = User.objects.create_user(email=email, username=username, is_active=True)
                            user.set_password(password1)
                            user.save()
                            # email_thread = Thread(
                            #     target=self.send_email,
                            #     kwargs={
                            #         "email": email,
                            #         "mode": "activate",
                            #         "activation_code": user.activation_code,
                            #         "password_reset_code": user.password_reset_code,
                            #     }
                            # )
                            # Using python threads are more faster to deliver emails.
                            # We won't let Django take responsibility to send email which takes time to send.

                            # email_thread.start()  # Frontend should redirect user to 6-digits code (otp) page
                            # and show message for user to check email address
                            return Response({"success": "[+] User is created successfully."})
                    # else:
                    #     return Response({"password_requirements": "[-] Password doesn't satisfy requirements."})
                else:
                    return Response({"password_not_match": "[-] Passwords are not matched"})
            else:
                return Response({"email_invalid": "[-] Email doesn't satisfy requirements. example@example.com"})
        else:
            return Response({"error": "[-] Please fill all registration input fields."})


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        logout(request)
        return Response({"success": "User is logged out."})


class SavingsView(APIView):
    def get(self, request):
        goals = SavingGoal.objects.filter(user=request.user)
        goals_serializer = SavingGoalsGetterSerializer(goals, many=True)
        return Response(goals_serializer.data)

    def post(self, request):
        goals_serializer = SavingsSerializer(data=request.data, context={"user": request.user})
        if goals_serializer.is_valid():
            goals_serializer.save()
            return Response({"success": "Goal has been saved successfully."})
        else:
            return Response({"error": "Data sent aren't valid or complete.", "errors": goals_serializer.errors})
