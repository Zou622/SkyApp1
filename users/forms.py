from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, get_user_model

from commercials.models import Commercial
from techniciens.models import Technicien
from .models import User

ROLE_CHOICES = [
    ('technicien', 'Technicien'),
    ('commercial', 'Commercial')
]

class LoginForm(AuthenticationForm):
    """Formulaire de connexion"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur",
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect")
            elif not self.user_cache.est_actif:
                raise forms.ValidationError("Ce compte est désactivé")
            elif not self.user_cache.est_valide:
                raise forms.ValidationError("Ce compte n'a pas encore été validé par un administrateur")
        return self.cleaned_data


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription"""

    user_type = forms.ChoiceField(
        choices=User.TYPE_USER,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telephone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'user_type', 'telephone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé")
        return email
    


User = get_user_model()
class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text="Laisser vide pour ne pas changer"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telephone', 'photo', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        # 🔹 Ne changer le mot de passe que si un mot de passe est saisi
        if password:
            user.set_password(password)
        # Sinon on conserve l'ancien mot de passe

        if commit:
            user.save()
        return user
    

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-sm"
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telephone',
            'photo'
        ]

        labels = {
            'username': "Nom d'utilisateur",
            'first_name': "Prénom",
            'last_name': "Nom",
            'email': "Email",
            'telephone': "Téléphone",
            'photo': "Photo de profil",
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'photo': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email',
        }),
        label='Adresse Email'
    )

    # Optionnel : vérifier si l'email existe
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("Cet email n'est associé à aucun compte actif.")
        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'}),
    )
    new_password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}),
    )