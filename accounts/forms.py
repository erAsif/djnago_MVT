from django                   import forms
from django.contrib.auth.forms import UserCreationForm
from .models                  import CustomUser


# ── 1. SIGNUP FORM ──────────────────────────────────────────────
class SignupForm(UserCreationForm):
    # Extra fields jo UserCreationForm mein nahi hain
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-input','placeholder': 'you@example.com',}) )
    phone = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'placeholder': '+91XXXXXXXXXX'}))
    dob = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
    password1 = forms.CharField( label="Password", widget=forms.PasswordInput, help_text=""  )
    password2 = forms.CharField( label="Confirm Password", widget=forms.PasswordInput, help_text=""  )
    # address = forms.CharField( required=False, widget=forms.Textarea(attrs={'rows': 3}) )
    # profile_img = forms.ImageField(required=False)

    class Meta:
        model  = CustomUser
        fields = ['username','email','phone','dob','password1','password2',# 'address','profile_img','first_name','last_name',
                  ]

    def clean_email(self):
        # Email pehle se registered toh nahi?
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered!")
        return email

    def clean_phone(self):
        # Phone number format validate karo
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() and not phone.startswith('+'):
            raise forms.ValidationError(
                "Enter a valid phone number.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email   = self.cleaned_data['email']
        user.phone   = self.cleaned_data['phone']
        user.dob     = self.cleaned_data.get('dob')
        # user.address = self.cleaned_data.get('address', '')
        if commit:
            user.save()
        return user


# ── 2. LOGIN FORM (Email + Password) ────────────────────────────
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email address','autofocus':   True,})    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',})    )
    remember_me = forms.BooleanField(required=False)


# ── 3. PROFILE UPDATE FORM ──────────────────────────────────────
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model   = CustomUser
        fields  = ['username',  'phone', 'dob', # 'address',# 'profile_img', # 'bio',first_name', 'last_name',
        ]
        widgets = {
            'dob':     forms.DateInput(attrs={'type': 'date'}),
            # 'address': forms.Textarea(attrs={'rows': 3}),
            # 'bio':     forms.Textarea(attrs={'rows': 4}),
        }
    