from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model




class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]

from django import forms
from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateProfileForm(forms.ModelForm):
    # On définit les champs avec leurs widgets pour Bootstrap
    first_name = forms.CharField(
        label="Prénom",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Entrez votre prénom"})
    )
    last_name = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Entrez votre nom"})
    )
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Nom d'utilisateur"})
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "votre@email.com"})
    )
    profile_pic = forms.ImageField(
        label="Photo de profil",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )
    address = forms.CharField(
        label="Adresse",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Adresse physique"}),
        required=False
    )
    phone = forms.CharField(
        label="Téléphone",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Ex: +243..."}),
        required=False
    )
    bio = forms.CharField(
        label="Ma biographie",
        widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Parlez-nous de vous...", "rows": 3}),
        required=False
    )
    role = forms.CharField(
        label="Fonction / Rôle",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Ex: Supporter Fidèle"}),
        required=False
    )

    # Champs de localisation
    province = forms.CharField(
        label="Province",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Ex: Haut-Katanga"}),
        required=False
    )
    ville_ou_district = forms.CharField(
        label="Ville / District",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Ex: Lubumbashi"}),
        required=False
    )
    commune_ou_contree = forms.CharField(
        label="Commune / Contrée",
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Ex: Annexe"}),
        required=False
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "username", "email", "address",
            "bio", "phone", "role", "profile_pic",
            "province", "ville_ou_district", "commune_ou_contree"
        ]

    # Optionnel : Validation spécifique pour l'email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Vérifie si l'email est déjà pris par un autre utilisateur
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre compte.")
        return email


from django import forms
from .models import (
    Supporteur,
    ContributionJour,
    PaiementContribution,
    RubriqueDepense,
    Depense,
    News,
    Comment,
    ReplyComment
)

class SupporteurForm(forms.ModelForm):

    class Meta:
        model = Supporteur
        fields = [
            "prenom",
            "nom",
            "postnom",
            "telephone",
            "province",
            "ville",
            "commune",
            "photo",
            "sexe",
            "statut_adhesion"
        ]

        widgets = {
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "postnom": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "province": forms.TextInput(attrs={"class": "form-control"}),
            "ville": forms.TextInput(attrs={"class": "form-control"}),
            "commune": forms.TextInput(attrs={"class": "form-control"}),
            "sexe": forms.Select(attrs={"class": "form-control"}),
            "statut_adhesion": forms.Select(attrs={"class": "form-control"}),
        }

class ContributionJourForm(forms.ModelForm):

    class Meta:
        model = ContributionJour
        fields = [
            "date",
            "montant"
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "montant": forms.NumberInput(attrs={"class": "form-control"}),
        }

class PaiementContributionForm(forms.ModelForm):

    class Meta:
        model = PaiementContribution
        fields = [
            "montant_total",
            "phone_number",
            "id_transaction",
        ]

        widgets = {
            "montant_total": forms.NumberInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "id_transaction": forms.TextInput(attrs={"class": "form-control"}),
        }

class RubriqueDepenseForm(forms.ModelForm):

    class Meta:
        model = RubriqueDepense
        fields = [
            "nom",
            "description"
        ]

        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class DepenseForm(forms.ModelForm):

    class Meta:
        model = Depense
        fields = [
            "rubrique",
            "titre",
            "description",
            "montant",
            "preuve",
            "date_depense"
        ]

        widgets = {
            "rubrique": forms.Select(attrs={"class": "form-control"}),
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "montant": forms.NumberInput(attrs={"class": "form-control"}),
            "date_depense": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
        

class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = [
            "title",
            "content",
            "media_type",
            "media_file",
            "allow_comments"
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "media_type": forms.Select(attrs={"class": "form-control"}),
        }
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Écrire un commentaire..."
            })
        }
        

class ReplyCommentForm(forms.ModelForm):

    class Meta:
        model = ReplyComment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Répondre..."
            })
        }
        

class ContributionMultipleForm(forms.Form):

    contributions = forms.ModelMultipleChoiceField(
        queryset=ContributionJour.objects.filter(statut__in=["pending","missed"]),
        widget=forms.CheckboxSelectMultiple
    )

    montant = forms.DecimalField(
        max_digits=10,
        decimal_places=2
    )  
    

from django import forms
from .models import PrixSupporteur, PaiementSupporteur


class PrixSupporteurForm(forms.ModelForm):

    class Meta:
        model = PrixSupporteur
        fields = ["prix", "devise", "actif"]

        widgets = {
            "prix": forms.NumberInput(attrs={
                "class": "w-full border rounded-lg p-2",
                "placeholder": "Prix par supporteur"
            }),
            "devise": forms.Select(attrs={
                "class": "w-full border rounded-lg p-2"
            }),
            "actif": forms.CheckboxInput(attrs={
                "class": "h-4 w-4"
            }),
        }
    
class PaiementSupporteurForm(forms.ModelForm):

    class Meta:
        model = PaiementSupporteur
        fields = [
            
            "phone_number",
            "id_transaction",
        ]

        widgets = {
            

            "phone_number": forms.TextInput(attrs={
                "class": "w-full border rounded-lg p-2",
                "placeholder": "Numéro utilisé pour le paiement"
            }),

            "id_transaction": forms.TextInput(attrs={
                "class": "w-full border rounded-lg p-2",
                "placeholder": "ID de transaction Mobile Money"
            }),
        }