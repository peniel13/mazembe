from django.contrib import admin
from django.contrib import admin
from .models import (
    Supporteur,
    ContributionJour,
    PaiementContribution,
    RubriqueDepense,
    Depense,
    News,
    Comment,
    ReplyComment,
    JournalAction
)
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



# class CustomUserAdmin(UserAdmin):
#     list_display = (
#         'username', 'email', 'profile_pic', 'is_active_user', 
#         'is_active', 'is_staff', 'is_superuser', 'role',
#         'province', 'ville_ou_district', 'commune_ou_contree', 
#         'phone', 'last_login',
#     )

#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password', 'profile_pic')}),
#         ('Informations personnelles', {'fields': ('role', 'bio', 'phone', 'province', 'ville_ou_district', 'commune_ou_contree',' is_acces_staf')}),
#         ('Permissions', {'fields': ( 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "username", "password1", "password2", "profile_pic",
#                            "role", "bio", "phone", "province", "ville_ou_district", "commune_ou_contree", ' is_acces_staf'),
#             },
#         ),
#     )

#     search_fields = ('email', 'username', 'role', 'province', 'ville_ou_district', 'commune_ou_contree',' is_acces_staf')
#     list_filter = ('is_staff', 'is_superuser', 'province', 'ville_ou_district')

# admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'profile_pic',
        'is_active_user',
        'is_active',
        'is_staff',
        'is_superuser',
        'role',
        'province',
        'ville_ou_district',
        'commune_ou_contree',
        'phone',
        'is_acces_staf',
        'last_login',
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'profile_pic')}),

        ('Informations personnelles', {
            'fields': (
                'role',
                'bio',
                'phone',
                'province',
                'ville_ou_district',
                'commune_ou_contree',
                'is_acces_staf'
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),

        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "profile_pic",
                    "role",
                    "bio",
                    "phone",
                    "province",
                    "ville_ou_district",
                    "commune_ou_contree",
                    "is_acces_staf",
                ),
            },
        ),
    )

    search_fields = (
        'email',
        'username',
        'role',
        'province',
        'ville_ou_district',
        'commune_ou_contree',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'province',
        'ville_ou_district',
        'is_acces_staf'
    )


admin.site.register(CustomUser, CustomUserAdmin)


# ============================
# ADMIN JOURNAL
# ============================
@admin.register(JournalAction)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("action", "utilisateur", "citoyen", "date_action")
    list_filter = ("action", "date_action")
    search_fields = ("citoyen__nom", "citoyen__prenom", "utilisateur__email")



from django.contrib import admin
from django.conf import settings
from .models import Supporteur

@admin.register(Supporteur)
class SupporteurAdmin(admin.ModelAdmin):

    list_display = (
        "prenom",
        "nom",
        "postnom",
        "telephone",
        "numero_supporteur",
        "statut",
        "statut_adhesion",
        "paye",              # ✅ nouveau champ
        "date_paiement",     # ✅ nouveau champ
        "province",
        "ville",
        "commune",
        "cree_par",
        "valide_par",
        "date_creation",
    )

    list_filter = (
        "statut",
        "statut_adhesion",
        "paye",              # ✅ filtre paiement
        "province",
        "ville",
        "sexe"
    )

    search_fields = (
        "prenom",
        "nom",
        "telephone",
        "numero_supporteur"
    )

    readonly_fields = (
        "qr_code",
        "date_creation",
        "cree_par",
        "valide_par",
        "date_paiement",     # ✅ empêche modification manuelle
    )

    ordering = ("-date_creation",)

    # 🔹 Remplir automatiquement le créateur
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.cree_par = request.user
        super().save_model(request, obj, form, change)
# @admin.register(Supporteur)
# class SupporteurAdmin(admin.ModelAdmin):

#     list_display = (
#         "prenom",
#         "nom",
#         "telephone",
#         "numero_supporteur",
#         "statut",
#         "statut_adhesion",
#         "province",
#         "ville",
#         "cree_par",
#         "valide_par",
#         "date_creation",
#     )

#     list_filter = (
#         "statut",
#         "statut_adhesion",
#         "province",
#         "ville",
#         "sexe"
#     )

#     search_fields = (
#         "prenom",
#         "nom",
#         "telephone",
#         "numero_supporteur"
#     )

#     readonly_fields = (
#         "qr_code",
#         "date_creation",
#         "cree_par",
#         "valide_par",
#     )

#     ordering = ("-date_creation",)

#     # 🔹 Optionnel : remplir automatiquement 'cree_par' à la création
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             obj.cree_par = request.user
#         super().save_model(request, obj, form, change)

# @admin.register(ContributionJour)
# class ContributionJourAdmin(admin.ModelAdmin):

#     list_display = (
#         "supporteur",
#         "date",
#         "statut",
#         "montant",
#         "date_paiement"
#     )

#     list_filter = (
#         "statut",
#         "date"
#     )

#     search_fields = (
#         "supporteur__prenom",
#         "supporteur__nom",
#     )

#     date_hierarchy = "date"

#     ordering = ("-date",)


# @admin.register(PaiementContribution)
# class PaiementContributionAdmin(admin.ModelAdmin):

#     list_display = (
#         "supporteur",
#         "montant_total",
#         "phone_number",
#         "id_transaction",
#         "date_paiement"
#     )

#     search_fields = (
#         "supporteur__prenom",
#         "supporteur__nom",
#         "phone_number",
#         "id_transaction"
#     )

#     date_hierarchy = "date_paiement"

#     filter_horizontal = ("contributions",)
from django.contrib import admin
from .models import ContributionJour, PaiementContribution


@admin.register(ContributionJour)
class ContributionJourAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "statut",
        "montant",
        "date_paiement"
    )

    list_filter = (
        "statut",
        "date"
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "user__email",
    )

    date_hierarchy = "date"
    ordering = ("-date",)


@admin.register(PaiementContribution)
class PaiementContributionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "montant_total",
        "phone_number",
        "id_transaction",
        "statut",
        "date_paiement"
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "user__email",
        "phone_number",
        "id_transaction"
    )

    list_filter = (
        "statut",
        "date_paiement"
    )

    date_hierarchy = "date_paiement"
    filter_horizontal = ("contributions",)

@admin.register(RubriqueDepense)
class RubriqueDepenseAdmin(admin.ModelAdmin):

    list_display = (
        "nom",
    )

    search_fields = (
        "nom",
    )

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):

    list_display = (
        "titre",
        "rubrique",
        "montant",
        "date_depense",
        "cree_par",
    )

    list_filter = (
        "rubrique",
        "date_depense",
    )

    search_fields = (
        "titre",
        "description",
    )

    date_hierarchy = "date_depense"

    ordering = ("-date_depense",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "media_type",
        "total_likes",
        "share_count",
        "created_at",
        "is_active"
    )

    list_filter = (
        "media_type",
        "is_active",
        "created_at"
    )

    search_fields = (
        "title",
        "content"
    )

    date_hierarchy = "created_at"

    filter_horizontal = ("likes",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "author",
        "news",
        "created_at",
        "is_active"
    )

    list_filter = (
        "is_active",
        "created_at"
    )

    search_fields = (
        "author__username",
        "content"
    )


@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):

    list_display = (
        "author",
        "comment",
        "created_at",
        "is_active"
    )

    list_filter = (
        "is_active",
        "created_at"
    )

    search_fields = (
        "author__username",
        "content"
    )


from django.contrib import admin
from .models import PrixSupporteur, PaiementSupporteur


@admin.register(PrixSupporteur)
class PrixSupporteurAdmin(admin.ModelAdmin):

    list_display = (
        "prix",
        "devise",
        "actif",
        "date_creation",
    )

    list_filter = (
        "actif",
        "devise",
    )

    search_fields = (
        "prix",
    )

    ordering = ("-date_creation",)

    readonly_fields = (
        "date_creation",
    )


from django.utils import timezone

from django.utils import timezone
from django.contrib import admin
from .models import PaiementSupporteur, Supporteur
from django.utils import timezone
from django.contrib import admin
from .models import PaiementSupporteur, Supporteur

from django.utils import timezone
from django.contrib import admin
from .models import PaiementSupporteur, Supporteur

from django.contrib import admin
from django.utils import timezone
from .models import PaiementSupporteur, Supporteur

@admin.register(PaiementSupporteur)
class PaiementSupporteurAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "montant",
        "devise",
        "phone_number",
        "id_transaction",
        "statut",
        "valide_par",
        "date_paiement",
    )

    list_filter = ("statut", "devise", "date_paiement")

    search_fields = (
        "user__email",
        "phone_number",
        "id_transaction",
    )
                
# @admin.register(PaiementSupporteur)
# class PaiementSupporteurAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "statut",
#         "valide_par",
#         "date_paiement",
#     )

#     list_filter = (
#         "statut",
#         "devise",
#         "date_paiement",
#     )

#     search_fields = (
#         "user__email",
#         "phone_number",
#         "id_transaction",
#     )

#     ordering = ("-date_paiement",)

#     readonly_fields = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "date_paiement",
#     )

#     actions = ["valider_paiement"]

#     def valider_paiement(self, request, queryset):
#         for paiement in queryset:
#             # Valider le paiement
#             paiement.statut = "validated"
#             paiement.valide_par = request.user
#             paiement.save()

#             # Associer uniquement les supporteurs créés avant ou au moment du paiement
#             supporteurs_non_payes = Supporteur.objects.filter(
#                 cree_par=paiement.user,
#                 paye=False,
#                 date_creation__lte=paiement.date_paiement  # <-- limite au groupe existant
#             )

#             # Lier ces supporteurs à ce paiement et les marquer comme payés
#             for s in supporteurs_non_payes:
#                 s.paye = True
#                 s.date_paiement = paiement.date_paiement or timezone.now()
#                 s.paiement = paiement  # <-- associe le supporteur au paiement courant
#                 s.save()

#     valider_paiement.short_description = "Valider les paiements sélectionnés"
    
# @admin.register(PaiementSupporteur)
# class PaiementSupporteurAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "statut",
#         "valide_par",
#         "date_paiement",
#     )

#     list_filter = (
#         "statut",
#         "devise",
#         "date_paiement",
#     )

#     search_fields = (
#         "user__email",
#         "phone_number",
#         "id_transaction",
#     )

#     ordering = ("-date_paiement",)

#     readonly_fields = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "date_paiement",
#     )

#     actions = ["valider_paiement"]

#     def valider_paiement(self, request, queryset):
#         for paiement in queryset:
#             # Mettre à jour le statut du paiement
#             paiement.statut = "validated"
#             paiement.valide_par = request.user
#             paiement.save()

#             # Mettre à jour uniquement les supporteurs créés avant ou au moment du paiement
#             supporteurs_non_payes = Supporteur.objects.filter(
#                 cree_par=paiement.user,
#                 paye=False,
#                 date_creation__lte=paiement.date_paiement  # <-- groupe existant au moment du paiement
#             )
#             for s in supporteurs_non_payes:
#                 s.paye = True
#                 s.date_paiement = paiement.date_paiement or timezone.now()
#                 s.save()

#     valider_paiement.short_description = "Valider les paiements sélectionnés"
# from django.utils import timezone

# @admin.register(PaiementSupporteur)
# class PaiementSupporteurAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "statut",
#         "valide_par",
#         "date_paiement",
#     )

#     list_filter = (
#         "statut",
#         "devise",
#         "date_paiement",
#     )

#     search_fields = (
#         "user__email",
#         "phone_number",
#         "id_transaction",
#     )

#     ordering = ("-date_paiement",)

#     readonly_fields = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "date_paiement",
#     )

#     actions = ["valider_paiement"]

#     def valider_paiement(self, request, queryset):
#         for paiement in queryset:
#             # Mettre à jour le statut du paiement
#             paiement.statut = "validated"
#             paiement.valide_par = request.user
#             paiement.save()

#             # Mettre à jour tous les supporteurs non payés de cet utilisateur
#             supporteurs_non_payes = Supporteur.objects.filter(cree_par=paiement.user, paye=False)
#             for s in supporteurs_non_payes:
#                 s.paye = True
#                 s.date_paiement = timezone.now()  # <-- date réelle de validation
#                 s.save()

#     valider_paiement.short_description = "Valider les paiements sélectionnés"
    
# @admin.register(PaiementSupporteur)
# class PaiementSupporteurAdmin(admin.ModelAdmin):

#     list_display = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "statut",
#         "valide_par",
#         "date_paiement",
#     )

#     list_filter = (
#         "statut",
#         "devise",
#         "date_paiement",
#     )

#     search_fields = (
#         "user__email",
#         "phone_number",
#         "id_transaction",
#     )

#     ordering = ("-date_paiement",)

#     readonly_fields = (
#         "user",
#         "montant",
#         "devise",
#         "phone_number",
#         "id_transaction",
#         "date_paiement",
#     )

#     actions = ["valider_paiement"]

#     def valider_paiement(self, request, queryset):
#         queryset.update(
#             statut="validated",
#             valide_par=request.user
#         )

#     valider_paiement.short_description = "Valider les paiements sélectionnés"