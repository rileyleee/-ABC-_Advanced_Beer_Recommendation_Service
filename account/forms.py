from account.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",
                  "password1",
                  "password2",
                  )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "email",
            "gender",
            "age",
            "bestbeer",
            "image",

        )
        pass

    field_order = ["username",
                   "bestbeer",
                   "email",
                   "password1",
                   "password2",
                   "gender",
                   "age",
                   "image"]
    pass
