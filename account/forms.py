from account.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",
                  "nickname",
                  "password1",
                  "password2",
                  "email",
                  "gender",
                  "age",
                  )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "nickname",
            "gender",
            "age",
            "image",
        )
        pass

    field_order = ["username",
                   "nickname",
                   "password1",
                   "password2",
                   "email",
                   "gender",
                   "age",
                   "image"]
    pass
