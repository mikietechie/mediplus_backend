from django.forms import ModelForm
from app.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone", "DOB", "address", "password"]