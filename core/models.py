from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify # type: ignore
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active_user = models.BooleanField(default=False)
    province = models.CharField(max_length=100, blank=True, null=True)
    ville_ou_district = models.CharField(max_length=100, blank=True, null=True)
    commune_ou_contree = models.CharField(max_length=100, blank=True, null=True)
    is_acces_staf = models.BooleanField(
        default=False,
        help_text="Si décoché, l'utilisateur ne pourra pas accéder aux informations détaillées."
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email

    def maj_contributions_manquees(self):
        today = timezone.now().date()
        ContributionJour.objects.filter(
            user=self,
            date__lt=today,
            statut="pending"
        ).update(statut="missed")

    def creer_contribution_du_jour(self):
        self.maj_contributions_manquees()
        today = timezone.now().date()
        contribution, created = ContributionJour.objects.get_or_create(
            user=self,
            date=today,
            defaults={"statut": "pending"}
        )
        return contribution



# class Supporteur(models.Model):

#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("valid", "Valide"),
#         ("blocked", "Bloqué"),
#     )
#     SEXE_CHOICES = (
#         ("M", "Masculin"),
#         ("F", "Féminin"),
#     )

#     ADHESION_CHOICES = (
#         ("membre_honneur", "Membre d'honneur"),
#         ("president_federation", "Président Fédération"),
#         ("president_cellule", "Président Cellule"),
#     )
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="supporteur"
#     )

#     prenom = models.CharField(max_length=100)
#     nom = models.CharField(max_length=100)

#     telephone = models.CharField(max_length=20)

#     province = models.CharField(max_length=150, blank=True, null=True)
#     ville = models.CharField(max_length=150, blank=True, null=True)

#     photo = models.ImageField(upload_to="supporteurs/photos/", blank=True, null=True)

#     numero_supporteur = models.CharField(max_length=20, unique=True, blank=True)

#     qr_code = models.ImageField(upload_to="supporteurs/qrcodes/", blank=True, null=True)

#     statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="pending")
#     # Statut d'adhésion
#     statut_adhesion = models.CharField(
#         max_length=30,
#         choices=ADHESION_CHOICES,
#         default="membre_honneur"
#     )
#     sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default="M")
#     date_creation = models.DateTimeField(auto_now_add=True)
    
#     cree_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="citoyens_crees"
#     )
#     valide_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="citoyens_valides"
#     )
#     def save(self, *args, **kwargs):
#         # Numéro unique si absent
#         if not self.numero_supporteur:
#          self.numero_supporteur = str(uuid.uuid4().int)[:12]
        
#         # Génération du QR code si absent
#         if not self.qr_code:
#             # qr_img = qrcode.make(f"https://monsite.com/verifier_qr/?numero={self.numero_identite}")
#             qr_img = qrcode.make(f"http://13.244.101.138/user/verifier_qr/?numero={self.numero_supporteur}")
#             buffer = BytesIO()
#             qr_img.save(buffer, format="PNG")
#             filename = f"qr_{self.numero_supporteur}.png"
#             self.qr_code.save(filename, File(buffer), save=False)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.prenom} {self.postnom or ''} {self.nom} ({self.numero_supporteur})"
    
#     def maj_contributions_manquees(self):
#         today = timezone.now().date()
#         ContributionJour.objects.filter(
#         supporteur=self,
#         date__lt=today,
#         statut="pending"
#     ).update(statut="missed")




# class ContributionJour(models.Model):

#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("paid", "Contribué"),
#         ("missed", "Manqué"),
#     )

#     supporteur = models.ForeignKey(
#         Supporteur,
#         on_delete=models.CASCADE,
#         related_name="contributions"
#     )

#     date = models.DateField()

#     statut = models.CharField(
#         max_length=20,
#         choices=STATUT_CHOICES,
#         default="pending"
#     )

#     montant = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )

#     date_paiement = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         unique_together = ("supporteur", "date")

#     def __str__(self):
#         return f"{self.supporteur} - {self.date}"
import uuid
from io import BytesIO
import qrcode
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files import File

from django.utils import timezone

class PaiementSupporteur(models.Model):

    STATUT_CHOICES = (
        ("pending", "En attente"),
        ("validated", "Validé"),
        ("rejected", "Refusé"),
    )

    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name="paiements_supporteurs"
    # )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    related_name="paiements_supporteurs"
    )

    montant = models.DecimalField(max_digits=12, decimal_places=2)

    devise = models.CharField(
        max_length=3,
        choices=[('USD', 'Dollar américain'), ('FC', 'Franc congolais')],
        default='USD'
    )

    id_transaction = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="pending"
    )

    date_paiement = models.DateTimeField(auto_now_add=True)

    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="paiements_valides"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 🔥 Si le paiement est validé -> tous les supporteurs deviennent payés
        if self.statut == "validated":
            self.supporteurs_du_lot.update(
                paye=True,
                date_paiement=timezone.now()
            )

    def __str__(self):
        return f"{self.user} - {self.montant} {self.devise}"
# class PaiementSupporteur(models.Model):

#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("validated", "Validé"),
#         ("rejected", "Refusé"),
#     )

#     DEVISE_CHOICES = (
#         ('USD', 'Dollar américain'),
#         ('FC', 'Franc congolais'),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="paiements_supporteurs"
#     )

#     montant = models.DecimalField(max_digits=12, decimal_places=2)

#     devise = models.CharField(
#         max_length=3,
#         choices=DEVISE_CHOICES,
#         default='USD'
#     )

#     id_transaction = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20)

#     statut = models.CharField(
#         max_length=20,
#         choices=STATUT_CHOICES,
#         default="pending"
#     )

#     date_paiement = models.DateTimeField(auto_now_add=True)

#     valide_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="paiements_valides"
#     )

#     def __str__(self):
#         return f"{self.user} - {self.montant} {self.devise}"
    
class Supporteur(models.Model):

    STATUT_CHOICES = (
        ("pending", "En attente"),
        ("valid", "Valide"),
        ("blocked", "Bloqué"),
    )
    SEXE_CHOICES = (
        ("M", "Masculin"),
        ("F", "Féminin"),
    )
    ADHESION_CHOICES = (
        ("membre_honneur", "Membre d'honneur"),
        ("president_federation", "Président Fédération"),
        ("president_cellule", "Président Cellule"),
    )
    
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20)
    province = models.CharField(max_length=150, blank=True, null=True)
    ville = models.CharField(max_length=150, blank=True, null=True)
    commune = models.CharField(max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to="supporteurs/photos/", blank=True, null=True)
    numero_supporteur = models.CharField(max_length=20, unique=True, blank=True)
    qr_code = models.ImageField(upload_to="supporteurs/qrcodes/", blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="pending")
    statut_adhesion = models.CharField(max_length=30, choices=ADHESION_CHOICES, default="membre_honneur")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default="M")
    date_creation = models.DateTimeField(auto_now_add=True)
    paye = models.BooleanField(default=False)
    # <-- Ajout du lien vers PaiementSupporteur
    paiement = models.ForeignKey(
        PaiementSupporteur,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="supporteurs_du_lot"
    )
    date_paiement = models.DateTimeField(blank=True, null=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="supporteurs_crees"
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supporteurs_valides"
    )

    def save(self, *args, **kwargs):
        # Numéro unique si absent
        if not self.numero_supporteur:
            self.numero_supporteur = str(uuid.uuid4().int)[:12]

        # Génération du QR code si absent
        if not self.qr_code:
            qr_img = qrcode.make(f"http://13.244.101.138/user/verifier_qr/?numero={self.numero_supporteur}")
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            filename = f"qr_{self.numero_supporteur}.png"
            self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.numero_supporteur})"



# ============================
# 4. JOURNAL DES ACTIONS
# ============================
class JournalAction(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    citoyen = models.ForeignKey(Supporteur, on_delete=models.CASCADE, related_name="journaux")
    action = models.CharField(max_length=200)  # Exemple : "Validation", "Blocage", "Création"
    date_action = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action} par {self.utilisateur} sur {self.citoyen}"




from django.conf import settings
from django.db import models
from django.utils import timezone


from django.conf import settings
from django.db import models
from django.utils import timezone


from django.conf import settings
from django.db import models
from django.utils import timezone


# class ContributionJour(models.Model):
#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("paid", "Contribué"),
#         ("missed", "Manqué"),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="contributions"
#     )
#     date = models.DateField()
#     statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="pending")
#     montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     date_paiement = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         unique_together = ("user", "date")
#         ordering = ["-date"]

#     def __str__(self):
#         return f"{self.user} - {self.date} ({self.statut})"


# from django.conf import settings
# from django.db import models
# from django.utils import timezone


# class PaiementContribution(models.Model):
#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("validated", "Validé"),
#         ("rejected", "Rejeté"),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="paiements_contribution"
#     )
#     montant_total = models.DecimalField(max_digits=10, decimal_places=2)
#     phone_number = models.CharField(max_length=20)
#     id_transaction = models.CharField(max_length=255)

#     contributions = models.ManyToManyField(
#         ContributionJour,
#         related_name="paiements",
#         blank=True
#     )

#     statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="pending")

#     valide_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="paiements_contribution_valides"
#     )

#     date_paiement = models.DateTimeField(auto_now_add=True)

#     def valider_paiement(self, admin_user=None):
#         self.statut = "validated"
#         if admin_user:
#             self.valide_par = admin_user
#         self.save(update_fields=["statut", "valide_par"])

#         self.contributions.update(
#             statut="paid",
#             date_paiement=timezone.now()
#         )

#     def __str__(self):
#         return f"{self.user} - {self.montant_total}"

from django.conf import settings
from django.db import models
from django.utils import timezone


# class ContributionJour(models.Model):
#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("paid", "Contribué"),
#         ("missed", "Manqué"),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="contributions"
#     )
#     date = models.DateField()
#     statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="pending")
#     montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     date_paiement = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         unique_together = ("user", "date")
#         ordering = ["-date"]

#     def __str__(self):
#         return f"{self.user} - {self.date} ({self.statut})"

from django.conf import settings
from django.db import models


class ContributionJour(models.Model):

    STATUT_PENDING = "pending"
    STATUT_PAID = "paid"
    STATUT_MISSED = "missed"

    STATUT_CHOICES = (
        (STATUT_PENDING, "En attente"),
        (STATUT_PAID, "Contribué"),
        (STATUT_MISSED, "Manqué"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions"
    )

    date = models.DateField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=STATUT_PENDING
    )

    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000
    )

    date_paiement = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["statut"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.date} ({self.get_statut_display()})"

    def marquer_payee(self, date_paiement):
        """Marquer la contribution comme payée"""
        self.statut = self.STATUT_PAID
        self.date_paiement = date_paiement
        self.save(update_fields=["statut", "date_paiement"])

class PaiementContribution(models.Model):
    STATUT_CHOICES = (
        ("pending", "En attente"),
        ("validated", "Validé"),
        ("rejected", "Rejeté"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="paiements_contribution"
    )
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    id_transaction = models.CharField(max_length=255)

    contributions = models.ManyToManyField(
        ContributionJour,
        related_name="paiements",
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="pending"
    )

    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paiements_contribution_valides"
    )

    date_paiement = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 🔥 Si le paiement est validé -> toutes les contributions liées deviennent payées
        if self.statut == "validated":
            self.contributions.update(
                statut="paid",
                date_paiement=timezone.now()
            )

    def __str__(self):
        return f"{self.user} - {self.montant_total}"
    
# 4️⃣ Rubrique de dépenses

# Pour la transparence financière du club.

class RubriqueDepense(models.Model):

    nom = models.CharField(max_length=200)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom



# 5️⃣ Dépenses du club
class Depense(models.Model):

    rubrique = models.ForeignKey(
        RubriqueDepense,
        on_delete=models.CASCADE,
        related_name="depenses"
    )

    titre = models.CharField(max_length=255)

    description = models.TextField()

    montant = models.DecimalField(max_digits=10, decimal_places=2)

    preuve = models.FileField(
        upload_to="depenses/preuves/",
        blank=True,
        null=True
    )

    date_depense = models.DateField()

    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.montant}"
    


User = settings.AUTH_USER_MODEL

class News(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Vidéo'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True)
    media_file = models.FileField(upload_to='news_media/', blank=True, null=True)  # photo ou vidéo
    created_at = models.DateTimeField(default=timezone.now)

    # 🔥 interactions
    likes = models.ManyToManyField(User, related_name='liked_news', blank=True)
    share_count = models.PositiveIntegerField(default=0)

    # 🔧 options
    allow_comments = models.BooleanField(default=True)  # admin peut désactiver les commentaires
    is_active = models.BooleanField(default=True)  # pour archiver/supprimer sans supprimer physiquement

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comments(self):
        return self.comments.count()


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # possibilité de masquer un commentaire

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.news.title}"


class ReplyComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Réponse de {self.author} à un commentaire sur {self.comment.news.title}"


class PrixSupporteur(models.Model):

    prix = models.DecimalField(max_digits=10, decimal_places=2)
    devise = models.CharField(max_length=5, default="USD")
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prix} {self.devise}"


# class PaiementSupporteur(models.Model):

#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("validated", "Validé"),
#         ("rejected", "Refusé"),
#     )

#     DEVISE_CHOICES = (
#         ('USD', 'Dollar américain'),
#         ('FC', 'Franc congolais'),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="paiements_supporteurs"
#     )

#     montant = models.DecimalField(max_digits=12, decimal_places=2)

#     devise = models.CharField(
#         max_length=3,
#         choices=DEVISE_CHOICES,
#         default='USD'
#     )

#     id_transaction = models.CharField(max_length=255)

#     phone_number = models.CharField(max_length=20)
#     supporteurs = models.ManyToManyField('Supporteur', blank=True, related_name='paiements')
#     statut = models.CharField(
#         max_length=20,
#         choices=STATUT_CHOICES,
#         default="pending"
#     )

#     date_paiement = models.DateTimeField(auto_now_add=True)

#     valide_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="paiements_valides"
#     )

#     def __str__(self):
#         return f"{self.user} - {self.montant} {self.devise}"



# class PrixSupporteur(models.Model):
#     prix = models.DecimalField(max_digits=10, decimal_places=2, default=10)
#     devise = models.CharField(max_length=5, default="USD")
#     actif = models.BooleanField(default=True)
#     date_creation = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.prix} {self.devise}"


# class FactureSupporteur(models.Model):

#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("paid", "Payé"),
#         ("validated", "Validé"),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="factures_supporteurs"
#     )

#     nombre_supporteurs = models.IntegerField()
#     prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

#     montant_total = models.DecimalField(max_digits=12, decimal_places=2)

#     statut = models.CharField(
#         max_length=20,
#         choices=STATUT_CHOICES,
#         default="pending"
#     )

#     date_creation = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - {self.montant_total}"



# class PaiementSupporteur(models.Model):

#     DEVISE_CHOICES = (
#         ('USD', 'Dollar américain'),
#         ('FC', 'Franc congolais'),
#     )

#     facture = models.ForeignKey(
#         FactureSupporteur,
#         on_delete=models.CASCADE,
#         related_name="paiements"
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )

#     montant = models.DecimalField(max_digits=12, decimal_places=2)

#     devise = models.CharField(
#         max_length=3,
#         choices=DEVISE_CHOICES,
#         default='USD'
#     )

#     id_transaction = models.CharField(max_length=255)

#     phone_number = models.CharField(max_length=20)

#     valide_admin = models.BooleanField(default=False)

#     date_paiement = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - {self.montant} {self.devise}"