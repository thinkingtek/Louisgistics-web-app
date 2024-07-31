from django import forms
from .models import Profile
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

        
class UserRegForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name',
                  'last_name', 'password1', 'password2')

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email Address",max_length=60)
    password = forms.CharField(label="Password",strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    remember_me = forms.BooleanField(required=False, label='Stay logged in ?')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email,password=password)
            if not user:
                raise forms.ValidationError("Wrong email or password")
        return super(UserLoginForm,self).clean()

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
