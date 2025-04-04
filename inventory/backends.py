from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuthBackend(ModelBackend):
    """
    Custom authentication backend to authenticate users based on email and password.
    This backend also checks if the user is approved before allowing login.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Use get_user_model() to get the custom user model
            user = UserModel.objects.get(email=email)
            # Check if the user is approved
            if user.check_password(password):
                if user.is_approved:  # Check if the user is approved
                    return user
                else:
                    return None  # User is not approved
        except UserModel.DoesNotExist:
            return None