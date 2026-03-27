from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegisterForm,UpdateProfileForm,PaiementContributionForm


from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Compte créé avec succès ! Vous pouvez vous connecter.")
            return redirect("signin")
        else:
            # Ajouter un message global si le formulaire n'est pas valide
            messages.error(request, "❌ Des erreurs sont survenues. Veuillez corriger les champs ci-dessous.")
    else:
        form = RegisterForm()

    return render(request, "core/signup.html", {"form": form})

def signin (request):
    if request.method == 'POST':
        email = request.POST["email"]
        password= request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context= {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("index")


from django.db.models import Q

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Supporteur, CustomUser


from .models import Supporteur, PrixSupporteur

@login_required(login_url="signin")
def profile(request, user_id):

    user = get_object_or_404(CustomUser, id=user_id)
    query = request.GET.get("q")

    supporteurs_qs = Supporteur.objects.filter(cree_par=user).order_by("-date_creation")

    # Recherche
    if query:
        query = query.strip()
        terms = query.split()

        q_objects = Q()
        for term in terms:
            q_objects |= (
                Q(prenom__icontains=term) |
                Q(nom__icontains=term) |
                Q(telephone__icontains=term) |
                Q(numero_supporteur__icontains=term) |
                Q(numero_supporteur__endswith=term)
            )

        supporteurs_qs = supporteurs_qs.filter(q_objects)

    # Pagination
    paginator = Paginator(supporteurs_qs, 6)
    page = request.GET.get("page")

    try:
        supporteurs = paginator.page(page)
    except PageNotAnInteger:
        supporteurs = paginator.page(1)
    except EmptyPage:
        supporteurs = paginator.page(paginator.num_pages)

    # Statistiques
    total_supporteurs = Supporteur.objects.filter(cree_par=user).count()
    supporteurs_payes = Supporteur.objects.filter(cree_par=user, paye=True).count()
    supporteurs_non_payes = Supporteur.objects.filter(cree_par=user, paye=False).count()

    prix = PrixSupporteur.objects.filter(actif=True).first()

    montant_total = 0
    if prix:
        montant_total = supporteurs_non_payes * prix.prix

    context = {
        "user": user,
        "supporteurs": supporteurs,
        "query": query,
        "total_supporteurs": total_supporteurs,
        "supporteurs_payes": supporteurs_payes,
        "supporteurs_non_payes": supporteurs_non_payes,
        "montant_total": montant_total,
        "prix": prix,
    }

    return render(request, "core/profile.html", context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Supporteur, PrixSupporteur, PaiementSupporteur


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Supporteur, PrixSupporteur, PaiementSupporteur

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Supporteur, PrixSupporteur, PaiementSupporteur

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url="signin")
def payer_supporteurs(request):
    user = request.user

    # Supporteurs non payés
    supporteurs_non_payes = Supporteur.objects.filter(cree_par=user, paye=False)
    if not supporteurs_non_payes.exists():
        messages.error(request, "Aucun supporteur à payer.")
        return redirect("profile", user.id)

    # Prix actif
    prix_obj = PrixSupporteur.objects.filter(actif=True).first()
    if not prix_obj:
        messages.error(request, "Aucun prix défini pour les supporteurs.")
        return redirect("profile", user.id)

    montant_total = supporteurs_non_payes.count() * prix_obj.prix

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        id_transaction = request.POST.get("id_transaction")

        if not phone_number or not id_transaction:
            messages.error(request, "Veuillez renseigner tous les champs.")
            return redirect("payer_supporteurs")

        # Création du paiement
        paiement = PaiementSupporteur.objects.create(
            user=user,
            montant=montant_total,
            devise=prix_obj.devise,
            phone_number=phone_number,
            id_transaction=id_transaction,
            statut="pending"
        )

        # Lier chaque supporteur individuellement pour garantir que save() soit appelé
        for s in supporteurs_non_payes:
            s.paiement = paiement
            s.save()

        messages.success(request, "Paiement envoyé. En attente de validation par l'admin.")
        return redirect("profile", user.id)

    context = {
        "supporteurs_non_payes": supporteurs_non_payes,
        "nombre_supporteurs": supporteurs_non_payes.count(),
        "montant_total": montant_total,
        "prix": prix_obj,
    }
    return render(request, "core/payer_supporteurs.html", context)

# @login_required(login_url="signin")
# def payer_supporteurs(request):
#     user = request.user

#     # On ne prend que les supporteurs non payés
#     supporteurs_non_payes = Supporteur.objects.filter(
#         cree_par=user,
#         paye=False
#     )

#     nombre_supporteurs = supporteurs_non_payes.count()

#     # Prix actif
#     prix_obj = PrixSupporteur.objects.filter(actif=True).first()
#     if not prix_obj:
#         messages.error(request, "Aucun prix défini pour les supporteurs.")
#         return redirect("profile", user.id)

#     montant_total = nombre_supporteurs * prix_obj.prix

#     if request.method == "POST":
#         phone_number = request.POST.get("phone_number")
#         id_transaction = request.POST.get("id_transaction")

#         if not phone_number or not id_transaction:
#             messages.error(request, "Veuillez renseigner tous les champs.")
#             return redirect("payer_supporteurs")

#         # Créer le paiement pour le lot actuel de supporteurs non payés
#         paiement = PaiementSupporteur.objects.create(
#             user=user,
#             montant=montant_total,
#             devise=prix_obj.devise,
#             phone_number=phone_number,
#             id_transaction=id_transaction,
#             statut="pending"
#         )

#         # On peut stocker le paiement comme "lot" pour plus tard (optionnel)
#         # Par exemple : supporteurs_non_payes.update(paiement=paiement)

#         messages.success(request, "Paiement envoyé. En attente de validation par l'admin.")
#         return redirect("profile", user.id)

#     context = {
#         "supporteurs_non_payes": supporteurs_non_payes,
#         "nombre_supporteurs": nombre_supporteurs,
#         "montant_total": montant_total,
#         "prix": prix_obj,
#     }

#     return render(request, "core/payer_supporteurs.html", context)

# @login_required(login_url="signin")
# def payer_supporteurs(request):
#     user = request.user

#     # Supporteurs non payés
#     supporteurs_non_payes = Supporteur.objects.filter(
#         cree_par=user,
#         paye=False
#     )

#     nombre_supporteurs = supporteurs_non_payes.count()

#     # Prix actif
#     prix_obj = PrixSupporteur.objects.filter(actif=True).first()

#     if not prix_obj:
#         messages.error(request, "Aucun prix défini pour les supporteurs.")
#         return redirect("profile", user.id)

#     montant_total = nombre_supporteurs * prix_obj.prix

#     if request.method == "POST":
#         phone_number = request.POST.get("phone_number")
#         id_transaction = request.POST.get("id_transaction")

#         if not phone_number or not id_transaction:
#             messages.error(request, "Veuillez renseigner tous les champs.")
#             return redirect("payer_supporteurs")

#         PaiementSupporteur.objects.create(
#             user=user,
#             montant=montant_total,
#             devise=prix_obj.devise,
#             phone_number=phone_number,
#             id_transaction=id_transaction,
#             statut="pending"
#         )

#         messages.success(request, "Paiement envoyé. En attente de validation par l'admin.")
#         return redirect("profile", user.id)

#     context = {
#         "supporteurs_non_payes": supporteurs_non_payes,
#         "nombre_supporteurs": nombre_supporteurs,
#         "montant_total": montant_total,
#         "prix": prix_obj,
#     }

#     return render(request, "core/payer_supporteurs.html", context)


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PaiementSupporteur, CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url="signin")
def liste_paiements_supporteurs(request, user_id=None):
    """
    Liste des paiements des supporteurs.
    Si user_id est fourni, filtre pour ce créateur.
    Sinon, affiche pour l'utilisateur connecté.
    """

    # Si admin ou superuser, peut voir n'importe quel user
    if user_id and request.user.is_superuser:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user

    # Récupère tous les paiements de ce user
    paiements_qs = PaiementSupporteur.objects.filter(user=user).order_by("-date_paiement")

    # Pagination
    paginator = Paginator(paiements_qs, 10)  # 10 paiements par page
    page = request.GET.get("page")
    try:
        paiements = paginator.page(page)
    except PageNotAnInteger:
        paiements = paginator.page(1)
    except EmptyPage:
        paiements = paginator.page(paginator.num_pages)

    # Montant total payé et en attente
    montant_total = sum(p.montant for p in paiements_qs)
    montant_pending = sum(p.montant for p in paiements_qs if p.statut == "pending")
    montant_validated = sum(p.montant for p in paiements_qs if p.statut == "validated")

    context = {
        "user": user,
        "paiements": paiements,
        "montant_total": montant_total,
        "montant_pending": montant_pending,
        "montant_validated": montant_validated,
        "page_obj": paiements,  # utile pour la pagination dans le template
    }

    return render(request, "core/liste_paiements_supporteurs.html", context)

# @login_required(login_url="signin")
# def liste_paiements_supporteurs(request, user_id=None):
#     """
#     Liste des paiements des supporteurs.
#     Si user_id est fourni, filtre pour ce créateur.
#     Sinon, affiche pour l'utilisateur connecté.
#     """

#     # Si admin ou superuser, peut voir n'importe quel user
#     if user_id and request.user.is_superuser:
#         user = get_object_or_404(CustomUser, id=user_id)
#     else:
#         user = request.user

#     # Récupère tous les paiements de ce user
#     paiements = PaiementSupporteur.objects.filter(user=user).order_by("-date_paiement")

#     # Montant total payé et en attente
#     montant_total = sum(p.montant for p in paiements)
#     montant_pending = sum(p.montant for p in paiements if p.statut == "pending")
#     montant_validated = sum(p.montant for p in paiements if p.statut == "validated")

#     context = {
#         "user": user,
#         "paiements": paiements,
#         "montant_total": montant_total,
#         "montant_pending": montant_pending,
#         "montant_validated": montant_validated,
#     }

#     return render(request, "core/liste_paiements_supporteurs.html", context)
# @login_required(login_url="signin")
# def profile(request, user_id):

#     user = get_object_or_404(CustomUser, id=user_id)
#     query = request.GET.get("q")

#     supporteurs_qs = Supporteur.objects.filter(cree_par=user).order_by("-date_creation")

#     # Recherche
#     if query:
#         query = query.strip()
#         terms = query.split()

#         q_objects = Q()
#         for term in terms:
#             q_objects |= (
#                 Q(prenom__icontains=term) |
#                 Q(nom__icontains=term) |
#                 Q(telephone__icontains=term) |
#                 Q(numero_supporteur__icontains=term) |
#                 Q(numero_supporteur__endswith=term)
#             )

#         supporteurs_qs = supporteurs_qs.filter(q_objects)

#     # Pagination
#     paginator = Paginator(supporteurs_qs, 6)
#     page = request.GET.get("page")

#     try:
#         supporteurs = paginator.page(page)
#     except PageNotAnInteger:
#         supporteurs = paginator.page(1)
#     except EmptyPage:
#         supporteurs = paginator.page(paginator.num_pages)

#     # Nombre total de supporteurs créés par ce user
#     total_supporteurs = Supporteur.objects.filter(cree_par=user).count()

#     context = {
#         "user": user,
#         "supporteurs": supporteurs,
#         "query": query,
#         "total_supporteurs": total_supporteurs,
#     }

#     return render(request, "core/profile.html", context)

@login_required(login_url="signin")
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect("profile", user_id=user.id)
        else:
            print(form.errors)  # 🔥 DEBUG IMPORTANT
    else:
        form = UpdateProfileForm(instance=user)

    context = {"form": form}
    return render(request, "core/update_profile.html", context)

# @login_required(login_url="signin")
# def update_profile(request):
#     if request.user.is_authenticated:
#         user = request.user
#         form = UpdateProfileForm(instance=user)
#         if request.method == 'POST':
#             form = UpdateProfileForm(request.POST, request.FILES, instance=user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Profile mis à jour")
#                 return redirect("profile", user_id=user.id)
                
#     context = {"form": form}
#     return render(request, "core/update_profile.html", context)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import SupporteurForm
from core.models import Supporteur, JournalAction

from django.utils import timezone

@login_required(login_url="signin")
def supporteur_create(request):
    if request.method == "POST":
        form = SupporteurForm(request.POST, request.FILES)
        if form.is_valid():
            supporteur = form.save(commit=False)

            # 🔥 Créateur
            supporteur.cree_par = request.user

            # 🔥 Validation automatique
            supporteur.statut = "valid"
            supporteur.valide_par = request.user

            # (optionnel) date de validation = maintenant
            supporteur.date_paiement = timezone.now()  # ou créer un champ date_validation si tu veux propre

            supporteur.save()

            # Journal
            JournalAction.objects.create(
                action="Création et validation de la carte supporteur",
                utilisateur=request.user,
                citoyen=supporteur
            )

            messages.success(request, "Carte supporteur créée et validée automatiquement !")
            return redirect("supporteur_detail", pk=supporteur.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = SupporteurForm()

    return render(request, "core/supporteur_create.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.models import User

def creer_supporteur_public(request):
    if request.method == "POST":
        form = SupporteurForm(request.POST, request.FILES)

        if form.is_valid():
            supporteur = form.save(commit=False)

            # 🔥 Toujours en attente
            supporteur.statut = "pending"

            # 🔥 Si connecté → associer
            if request.user.is_authenticated:
                supporteur.cree_par = request.user
            else:
                supporteur.cree_par = None  # ou créer un user auto si tu veux

            supporteur.save()

            # 🔥 Stocker en session (important pour non connecté)
            request.session["supporteur_id"] = supporteur.id

            messages.success(request, "Carte créée avec succès. Veuillez procéder au paiement pour qu'elle soit valider.")

            return redirect("payer_supporteur_unique")

    else:
        form = SupporteurForm()

    return render(request, "core/creer_supporteur_public.html", {"form": form})


def payer_supporteur_unique(request):
    supporteur_id = request.session.get("supporteur_id")

    if not supporteur_id:
        messages.error(request, "Aucun supporteur trouvé.")
        return redirect("creer_supporteur_public")

    supporteur = Supporteur.objects.filter(id=supporteur_id).first()

    if not supporteur:
        messages.error(request, "Supporteur introuvable.")
        return redirect("creer_supporteur_public")

    # 🔥 Prix
    prix_obj = PrixSupporteur.objects.filter(actif=True).first()
    if not prix_obj:
        messages.error(request, "Prix non défini.")
        return redirect("creer_supporteur_public")

    montant_total = prix_obj.prix

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        id_transaction = request.POST.get("id_transaction")

        if not phone_number or not id_transaction:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect("payer_supporteur_unique")

        # 🔥 Créer paiement
        paiement = PaiementSupporteur.objects.create(
            user=request.user if request.user.is_authenticated else None,
            montant=montant_total,
            devise=prix_obj.devise,
            phone_number=phone_number,
            id_transaction=id_transaction,
            statut="pending"
        )

        # 🔥 Lier supporteur
        supporteur.paiement = paiement
        supporteur.save()

        messages.success(request, "Paiement envoyé. En attente de validation.")

        return redirect("index")  # ou page confirmation

    return render(request, "core/payer_supporteur_unique.html", {
        "supporteur": supporteur,
        "montant_total": montant_total,
        "prix": prix_obj,
    })
# @login_required(login_url="signin")
# def supporteur_create(request):
#     if request.method == "POST":
#         form = SupporteurForm(request.POST, request.FILES)
#         if form.is_valid():
#             supporteur = form.save(commit=False)
#             supporteur.cree_par = request.user  # l'utilisateur qui crée la carte
#             supporteur.save()

#             # Journaliser l'action
#             JournalAction.objects.create(
#                 action="Création de la carte supporteur",
#                 utilisateur=request.user,
#                 citoyen=supporteur
#             )

#             messages.success(request, "Carte supporteur créée avec succès !")
#             return redirect("supporteur_detail", pk=supporteur.id)
#         else:
#             messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
#     else:
#         form = SupporteurForm()

#     return render(request, "core/supporteur_create.html", {"form": form})


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Supporteur
from .forms import SupporteurForm

@login_required(login_url="signin")
def modifier_carte_supporteur(request, supporteur_id):
    supporteur = get_object_or_404(Supporteur, id=supporteur_id)

    # Vérifier que l'utilisateur connecté est le créateur
    if request.user != supporteur.cree_par:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette carte.")
        return redirect("profile")

    if request.method == "POST":
        form = SupporteurForm(request.POST, request.FILES, instance=supporteur)
        if form.is_valid():
            form.save()
            messages.success(request, "Carte supporteur modifiée avec succès ✅")
            return redirect("profile", user_id=request.user.id)
    else:
        form = SupporteurForm(instance=supporteur)

    return render(request, "core/modifier_carte_supporteur.html", {
        "form": form,
        "supporteur": supporteur
    })


@login_required(login_url="signin")
def supprimer_carte_supporteur(request, supporteur_id):
    supporteur = get_object_or_404(Supporteur, id=supporteur_id)

    # Vérifier que l'utilisateur connecté est le créateur
    if request.user != supporteur.cree_par:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette carte.")
        return redirect("profile")

    if request.method == "POST":
        supporteur.delete()
        messages.success(request, "Carte supporteur supprimée avec succès ✅")
        return redirect("profile")

    # GET : afficher confirmation
    return render(request, "core/confirmer_suppression_carte_supporteur.html", {
        "supporteur": supporteur
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.files import File
from io import BytesIO
import qrcode
from .models import Supporteur


@login_required(login_url="signin")
def supporteur_detail(request, pk):
    supporteur = get_object_or_404(Supporteur, pk=pk)

    # Générer QR code si pas déjà créé
    if not supporteur.qr_code:
        qr_img = qrcode.make(
            f"http://13.244.101.138/user/verifier_qr/?numero={supporteur.numero_supporteur}"
        )

        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")

        supporteur.qr_code.save(
            f"qr_{supporteur.numero_supporteur}.png",
            File(buffer),
            save=True
        )

    return render(request, "core/supporteur_detail.html", {
        "supporteur": supporteur
    })

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
import zipfile
from django.templatetags.static import static
from django.conf import settings

@login_required(login_url="signin")
def telecharger_carte_supporteur_image(request, supporteur_id):
    from weasyprint import HTML
    from pdf2image import convert_from_bytes
    supporteur = get_object_or_404(Supporteur, pk=supporteur_id)

    # Préparer toutes les URLs absolues pour les images statiques
    static_base = request.build_absolute_uri('/')[:-1]

    context = {
        "supporteur": supporteur,
        "fondudps": static_base + static("img/fondudps.jpg"),
        "logo_udps": static_base + static("img/lupopo.png"),
        "udps_logo": static_base + static("img/lupopo.png"),
        "coter": static_base + static("img/fondudps.jpg"),
        "signature": static_base + static("img/signature.jpg"),

        "MEDIA_URL": request.build_absolute_uri(settings.MEDIA_URL),
    }

    # Générer le HTML
    html_string = render_to_string(
        "core/carte_supporteur_pdf.html",
        context
    )

    # Créer le PDF depuis le HTML
    html = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    )

    pdf_bytes = html.write_pdf()

    # Convertir PDF → images
    images = convert_from_bytes(pdf_bytes)

    # Créer ZIP contenant les images
    zip_io = BytesIO()

    with zipfile.ZipFile(zip_io, mode="w") as zip_file:
        for i, image in enumerate(images, start=1):
            img_bytes_io = BytesIO()
            image.save(img_bytes_io, format='PNG')
            img_bytes_io.seek(0)

            zip_file.writestr(
                f"Carte_{supporteur.numero_supporteur}_page{i}.png",
                img_bytes_io.read()
            )

    zip_io.seek(0)

    response = HttpResponse(zip_io, content_type="application/zip")
    response['Content-Disposition'] = (
        f'attachment; filename=Carte_{supporteur.numero_supporteur}.zip'
    )

    return response


# core/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Supporteur

@login_required(login_url="signin")
def verifier_qr(request):
    """
    Vérification simple du QR code ou numéro supporteur entré par l'utilisateur
    """
    numero = request.GET.get("numero")
    supporteur = None
    statut = "inexistante"

    if numero:
        try:
            supporteur = Supporteur.objects.get(numero_supporteur=numero)
            if supporteur.statut_adhesion == "valid":  # adapte selon ton choix de champ
                statut = "valide"
            else:
                statut = "non_valide"
        except Supporteur.DoesNotExist:
            statut = "inexistante"

    return render(request, "core/verifier_qr.html", {
        "supporteur": supporteur,
        "statut": statut
    })


@login_required(login_url="signin")
def verifier_qr_ajax(request):
    """
    Vérification QR code en temps réel via JS
    """
    numero = request.GET.get("numero")
    if not numero:
        return JsonResponse({"statut": "inexistante"})

    try:
        supporteur = Supporteur.objects.get(numero_supporteur=numero)
        statut = "valide" if supporteur.statut_adhesion == "valid" else "non_valide"

        return JsonResponse({
            "statut": statut,
            "prenom": supporteur.prenom,
            "nom": supporteur.nom,
            "numero_supporteur": supporteur.numero_supporteur
        })
    except Supporteur.DoesNotExist:
        return JsonResponse({"statut": "inexistante"})


@login_required(login_url="signin")
def verifier_qr_scanner(request):
    """
    Page pour scanner le QR code en direct
    """
    return render(request, "core/verifier_qr_scanner.html")


from django.shortcuts import render
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Supporteur  # Modèle Supporteur
from django.shortcuts import render
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core.models import Supporteur

def liste_createurs_supporteur(request):
    query = request.GET.get("q", "").strip()

    # Base : utilisateurs qui ont créé au moins un supporteur
    users_qs = Supporteur.objects.exclude(cree_par__isnull=True).values(
    'cree_par__id',
    'cree_par__username',
    'cree_par__email',
    'cree_par__profile_pic',
    'cree_par__province',
    'cree_par__ville_ou_district'
    ).annotate(nb_supporteurs=Count('id')).order_by('-nb_supporteurs')

    # Filtrage par localisation
    filtre_active = None
    if query:
        users_qs = users_qs.filter(
            Q(cree_par__province__icontains=query) |
            Q(cree_par__ville_ou_district__icontains=query)
        )
        filtre_active = query

    # Stats globales
    total_users = users_qs.count()
    total_cartes = Supporteur.objects.count()

    # Pagination : 6 créateurs par page
    paginator = Paginator(users_qs, 6)
    page = request.GET.get("page")
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    # Stats filtrées
    total_users_filtre = users_qs.count()
    total_cartes_filtre = sum(u['nb_supporteurs'] for u in users_qs)

    context = {
        "users": users,
        "total_users": total_users,
        "total_cartes": total_cartes,
        "query": query,
        "filtre_active": filtre_active,
        "total_users_filtre": total_users_filtre,
        "total_cartes_filtre": total_cartes_filtre,
    }

    return render(request, "core/liste_createurs_supporteur.html", context)
# def liste_createurs_supporteur(request):
#     query = request.GET.get("q", "").strip()

#     # Base : utilisateurs qui ont créé au moins un supporteur
#     users_qs = Supporteur.objects.values('cree_par__id', 'cree_par__username', 'cree_par__email', 'cree_par__profile_pic',
#                                          'cree_par__province', 'cree_par__ville', 'cree_par__commune') \
#                                  .annotate(nb_supporteurs=Count('id')) \
#                                  .order_by('-nb_supporteurs')

#     # Filtrage par localisation
#     filtre_active = None
#     if query:
#         users_qs = users_qs.filter(
#             Q(cree_par__province__icontains=query) |
#             Q(cree_par__ville__icontains=query) |
#             Q(cree_par__commune__icontains=query)
#         )
#         filtre_active = query

#     # Stats globales
#     total_users = users_qs.count()
#     total_cartes = Supporteur.objects.count()

#     # Pagination : 6 créateurs par page
#     paginator = Paginator(users_qs, 6)
#     page = request.GET.get("page")
#     try:
#         users = paginator.page(page)
#     except PageNotAnInteger:
#         users = paginator.page(1)
#     except EmptyPage:
#         users = paginator.page(paginator.num_pages)

#     # Stats filtrées
#     total_users_filtre = users_qs.count()
#     total_cartes_filtre = sum(u['nb_supporteurs'] for u in users_qs)

#     context = {
#         "users": users,
#         "total_users": total_users,
#         "total_cartes": total_cartes,
#         "query": query,
#         "filtre_active": filtre_active,
#         "total_users_filtre": total_users_filtre,
#         "total_cartes_filtre": total_cartes_filtre,
#     }

#     return render(request, "core/liste_createurs_supporteur.html", context)



@login_required(login_url="signin")
def journal_list(request):
    query = request.GET.get("q")

    # Si on a recherché un utilisateur précis
    if query and '@' in query:
        # Vue détail utilisateur
        journaux_user = JournalAction.objects.filter(utilisateur__email=query).select_related("citoyen", "utilisateur")

        # Stats globales de l’utilisateur
        stats_qs = journaux_user.values('action').annotate(total=Count('id'))
        stats_utilisateur = {item['action']: item['total'] for item in stats_qs}

        # Pagination des journaux
        paginator = Paginator(journaux_user.order_by("-date_action"), 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "core/journal_detail_user.html", {
            "query": query,
            "page_obj": page_obj,
            "stats_utilisateur": stats_utilisateur
        })

    else:
        # Vue globale : liste des utilisateurs + nombre total d’actions
        users_stats = (
            JournalAction.objects
            .values("utilisateur__email")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return render(request, "core/journal_users.html", {
            "query": query,
            "users_stats": users_stats
        })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Supporteur

@login_required(login_url="signin")
def supporteurs_dashboard_stats(request):
    # Récupérer la valeur du filtre (province, ville, statut_adhesion, sexe)
    filtre = request.GET.get("filtre", "").strip()
    valeur = request.GET.get("valeur", "").strip()

    supporteurs_qs = Supporteur.objects.all()

    # Appliquer le filtre si défini
    if filtre and valeur:
        filter_kwargs = {f"{filtre}__icontains": valeur}
        supporteurs_qs = supporteurs_qs.filter(**filter_kwargs)

    # Comptage global par catégorie
    provinces_count = Supporteur.objects.values('province').annotate(total=Count('id')).order_by('-total')
    villes_count = Supporteur.objects.values('ville').annotate(total=Count('id')).order_by('-total')
    communes_count = Supporteur.objects.values('commune').annotate(total=Count('id')).order_by('-total')
    statut_adhesion_count = Supporteur.objects.values('statut_adhesion').annotate(total=Count('id')).order_by('-total')
    sexe_count = Supporteur.objects.values('sexe').annotate(total=Count('id')).order_by('-total')

    context = {
        "supporteurs_count": supporteurs_qs.count(),
        "provinces_count": provinces_count,
        "villes_count": villes_count,
        "statut_adhesion_count": statut_adhesion_count,
        "sexe_count": sexe_count,
        "filtre": filtre,
        "valeur": valeur,
        "communes_count": communes_count
    }
    return render(request, "core/supporteurs_stats.html", context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Supporteur

@login_required(login_url="signin")
def supporteurs_list(request):
    query = request.GET.get("q")
    supporteurs_qs = Supporteur.objects.all().order_by("-date_creation")

    # Filtrage par recherche textuelle
    if query:
        query = query.strip()
        terms = query.split()
        q_objects = Q()
        for term in terms:
            q_objects |= (
                Q(prenom__icontains=term) |
                Q(nom__icontains=term) |
                Q(telephone__icontains=term) |
                Q(numero_supporteur__icontains=term) |
                Q(numero_supporteur__endswith=term)
            )
        supporteurs_qs = supporteurs_qs.filter(q_objects)

    # Compteurs par province et ville
    provinces_count = supporteurs_qs.values('province').annotate(total=Count('id')).order_by('-total')
    villes_count = supporteurs_qs.values('ville').annotate(total=Count('id')).order_by('-total')

    # Pagination
    paginator = Paginator(supporteurs_qs, 6)
    page = request.GET.get("page")
    try:
        supporteurs = paginator.page(page)
    except PageNotAnInteger:
        supporteurs = paginator.page(1)
    except EmptyPage:
        supporteurs = paginator.page(paginator.num_pages)

    return render(
        request,
        "core/supporteurs_list.html",
        {
            "supporteurs": supporteurs,
            "query": query,
            "provinces_count": provinces_count,
            "villes_count": villes_count,
        },
    )
    

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import ContributionJour, PaiementContribution
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q


from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum

# @login_required
# def mes_contributions(request):
#     today = timezone.localdate()

#     # Marquer les anciennes contributions non payées comme manquées
#     ContributionJour.objects.filter(
#         user=request.user,
#         date__lt=today
#     ).exclude(
#         statut="paid"
#     ).update(statut="missed")

#     contributions = ContributionJour.objects.filter(
#         user=request.user
#     ).exclude(
#         statut="paid"
#     ).exclude(
#         paiements__statut="pending"
#     ).order_by("date").distinct()

#     # STATISTIQUES
#     total_contributions = ContributionJour.objects.filter(user=request.user).count()
#     total_payees = ContributionJour.objects.filter(
#         user=request.user,
#         statut="paid"
#     ).count()

#     progression = 0

#     if total_contributions > 0:
#         progression = round((total_payees / total_contributions) * 100)

#     if request.method == "POST":

#         contribution_ids = request.POST.getlist("contributions")

#         if not contribution_ids:
#             messages.error(request, "Veuillez sélectionner au moins une contribution.")
#             return redirect("mes_contributions")

#         contributions_valides = ContributionJour.objects.filter(
#             id__in=contribution_ids,
#             user=request.user
#         ).exclude(
#             statut="paid"
#         ).exclude(
#             paiements__statut="pending"
#         )

#         if not contributions_valides.exists():
#             messages.error(request, "Ces contributions ne peuvent pas être payées.")
#             return redirect("mes_contributions")

#         request.session["contributions_selectionnees"] = list(
#             contributions_valides.values_list("id", flat=True)
#         )

#         return redirect("paiement_contribution")
#     # TOTAL PAYE
#     montant_total_paye = PaiementContribution.objects.filter(
#         user=request.user,
#         statut="validated"
#     ).aggregate(total=Sum("montant_total"))["total"] or 0
    
#     total_manque = contributions.filter(statut="missed").count()
#     total_pending = contributions.filter(statut="pending").count()

#     montant_total_global = sum(
#         c.montant or Decimal("0") for c in contributions
#     )

#     context = {
#         "contributions": contributions,
#         "total_manque": total_manque,
#         "total_pending": total_pending,
#         "montant_total_global": montant_total_global,
#         "total_contributions": total_contributions,
#         "total_payees": total_payees,
#         "progression": progression,
#         "montant_total_paye": montant_total_paye,
#     }

#     return render(request, "core/mes_contributions.html", context)


@login_required
def mes_contributions(request):

    # 🔥 Générer automatiquement la contribution du jour
    request.user.creer_contribution_du_jour()

    today = timezone.localdate()

    # Marquer les anciennes contributions non payées comme manquées
    ContributionJour.objects.filter(
        user=request.user,
        date__lt=today,
        statut="pending"
    ).update(statut="missed")

    contributions = ContributionJour.objects.filter(
        user=request.user
    ).exclude(
        statut="paid"
    ).exclude(
        paiements__statut="pending"
    ).order_by("date").distinct()

    # 📊 STATISTIQUES
    total_contributions = ContributionJour.objects.filter(
        user=request.user
    ).count()

    total_payees = ContributionJour.objects.filter(
        user=request.user,
        statut="paid"
    ).count()

    progression = 0
    if total_contributions > 0:
        progression = round((total_payees / total_contributions) * 100)

    # 💰 TOTAL PAYÉ
    montant_total_paye = PaiementContribution.objects.filter(
        user=request.user,
        statut="validated"
    ).aggregate(total=Sum("montant_total"))["total"] or 0

    if request.method == "POST":

        contribution_ids = request.POST.getlist("contributions")

        if not contribution_ids:
            messages.error(request, "Veuillez sélectionner au moins une contribution.")
            return redirect("mes_contributions")

        contributions_valides = ContributionJour.objects.filter(
            id__in=contribution_ids,
            user=request.user
        ).exclude(
            statut="paid"
        ).exclude(
            paiements__statut="pending"
        )

        if not contributions_valides.exists():
            messages.error(request, "Ces contributions ne peuvent pas être payées.")
            return redirect("mes_contributions")

        request.session["contributions_selectionnees"] = list(
            contributions_valides.values_list("id", flat=True)
        )

        return redirect("paiement_contribution")

    total_manque = contributions.filter(statut="missed").count()
    total_pending = contributions.filter(statut="pending").count()

    montant_total_global = sum(
        c.montant or Decimal("0") for c in contributions
    )

    context = {
        "contributions": contributions,
        "total_manque": total_manque,
        "total_pending": total_pending,
        "montant_total_global": montant_total_global,
        "total_contributions": total_contributions,
        "total_payees": total_payees,
        "progression": progression,
        "montant_total_paye": montant_total_paye,
    }

    return render(request, "core/mes_contributions.html", context)
# @login_required
# def mes_contributions(request):
#     today = timezone.localdate()

#     # Marquer automatiquement les contributions passées comme manquées
#     ContributionJour.objects.filter(
#         user=request.user,
#         date__lt=today
#     ).exclude(
#         statut="paid"
#     ).update(statut="missed")

#     # Exclure les contributions déjà payées ou déjà dans un paiement pending
#     contributions = ContributionJour.objects.filter(
#         user=request.user
#     ).exclude(
#         statut="paid"
#     ).exclude(
#         paiements__statut="pending"
#     ).order_by("date").distinct()

#     if request.method == "POST":

#         contribution_ids = request.POST.getlist("contributions")

#         if not contribution_ids:
#             messages.error(request, "Veuillez sélectionner au moins une contribution.")
#             return redirect("mes_contributions")

#         # Sécurisation : vérifier que les contributions appartiennent bien à l'utilisateur
#         contributions_valides = ContributionJour.objects.filter(
#             id__in=contribution_ids,
#             user=request.user
#         ).exclude(
#             statut="paid"
#         ).exclude(
#             paiements__statut="pending"
#         )

#         if not contributions_valides.exists():
#             messages.error(request, "Ces contributions ne peuvent pas être payées.")
#             return redirect("mes_contributions")

#         request.session["contributions_selectionnees"] = list(contributions_valides.values_list("id", flat=True))

#         return redirect("paiement_contribution")

#     total_manque = contributions.filter(statut="missed").count()
#     total_pending = contributions.filter(statut="pending").count()

#     montant_total_global = sum(
#         c.montant or Decimal("0") for c in contributions
#     )

#     context = {
#         "contributions": contributions,
#         "total_manque": total_manque,
#         "total_pending": total_pending,
#         "montant_total_global": montant_total_global,
#     }

#     return render(request, "core/mes_contributions.html", context)


@login_required
def paiement_contribution(request):

    contribution_ids = request.session.get("contributions_selectionnees")

    if not contribution_ids:
        messages.error(request, "Aucune contribution sélectionnée.")
        return redirect("mes_contributions")

    # Vérifier que les contributions sont toujours valides
    contributions = ContributionJour.objects.filter(
        id__in=contribution_ids,
        user=request.user
    ).exclude(
        statut="paid"
    ).exclude(
        paiements__statut="pending"
    ).distinct()

    if not contributions.exists():
        messages.error(request, "Ces contributions sont déjà en cours de paiement ou payées.")
        return redirect("mes_contributions")

    montant_total = sum(
        c.montant or Decimal("0") for c in contributions
    )

    if request.method == "POST":

        form = PaiementContributionForm(request.POST)

        if form.is_valid():

            paiement = form.save(commit=False)
            paiement.user = request.user
            paiement.statut = "pending"
            paiement.save()

            paiement.contributions.set(contributions)

            # Marquer les contributions comme en attente
            contributions.update(statut="pending")

            # Nettoyer la session
            if "contributions_selectionnees" in request.session:
                del request.session["contributions_selectionnees"]

            messages.success(
                request,
                "Votre paiement a été envoyé et sera vérifié par l'administrateur."
            )

            return redirect("mes_contributions")

    else:
        form = PaiementContributionForm(
            initial={"montant_total": montant_total}
        )

    context = {
        "form": form,
        "contributions": contributions,
        "montant_total": montant_total,
    }

    return render(request, "core/paiement_contribution.html", context)


@login_required
def mes_paiements_contributions(request):

    paiements_qs = PaiementContribution.objects.filter(
        user=request.user
    ).order_by("-date_paiement")

    # Pagination : 6 paiements par page
    paginator = Paginator(paiements_qs, 6)
    page = request.GET.get("page")

    try:
        paiements = paginator.page(page)
    except PageNotAnInteger:
        paiements = paginator.page(1)
    except EmptyPage:
        paiements = paginator.page(paginator.num_pages)

    context = {
        "paiements": paiements
    }

    return render(
        request,
        "core/mes_paiements_contributions.html",
        context
    )


from django.core.paginator import Paginator
from .models import PaiementContribution

def liste_paiements_contributions(request):

    paiements = PaiementContribution.objects.filter(
        statut="validated"
    ).select_related("user").order_by("-date_paiement")

    paginator = Paginator(paiements, 9)
    page = request.GET.get("page")
    paiements = paginator.get_page(page)

    context = {
        "paiements": paiements
    }

    return render(
        request,
        "core/liste_paiements.html",
        context
    )

from django.core.paginator import Paginator
from .models import Depense

def liste_depenses(request):

    depenses = Depense.objects.select_related(
        "rubrique"
    ).order_by("-date_depense")

    paginator = Paginator(depenses, 9)
    page = request.GET.get("page")
    depenses = paginator.get_page(page)

    context = {
        "depenses": depenses
    }

    return render(
        request,
        "core/liste_depenses.html",
        context
    )

from django.shortcuts import render, get_object_or_404
from .models import Depense

def detail_depense(request, depense_id):

    depense = get_object_or_404(
        Depense,
        id=depense_id
    )

    context = {
        "depense": depense
    }

    return render(
        request,
        "core/detail_depense.html",
        context
    )
    
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import News, Comment, ReplyComment
from .forms import CommentForm, ReplyCommentForm


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import News, Comment, ReplyComment
from .forms import CommentForm, ReplyCommentForm

@login_required
def detail_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    comments_list = Comment.objects.filter(news=news, is_active=True).order_by('-created_at')

    # Pagination commentaires
    paginator = Paginator(comments_list, 6)
    page = request.GET.get("page")
    comments = paginator.get_page(page)

    reply_open = request.GET.get("reply_open")  # ID du commentaire dont le formulaire doit être ouvert

    # Gérer POST commentaire ou réponse
    if request.method == "POST":
        if "comment_submit" in request.POST:
            content = request.POST.get("content")
            if content:
                Comment.objects.create(news=news, author=request.user, content=content)
                return redirect(f"{request.path}#comments")
        elif "reply_submit" in request.POST:
            content = request.POST.get("content")
            reply_to_id = request.POST.get("reply_to")
            if content and reply_to_id:
                parent_comment = Comment.objects.get(id=reply_to_id)
                ReplyComment.objects.create(comment=parent_comment, author=request.user, content=content)
                return redirect(f"{request.path}?reply_open={reply_to_id}#comments")

        elif "like_news" in request.POST:
            if request.user in news.likes.all():
                news.likes.remove(request.user)
            else:
                news.likes.add(request.user)
            return redirect(f"{request.path}#comments")

    context = {
        "news": news,
        "comments": comments,
        "reply_open": reply_open,
    }
    return render(request, "core/detail_news.html", context)

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News

def news_list(request):
    # 3 dernières news pour la section "récentes"
    recent_news = News.objects.filter(is_active=True).select_related('author').order_by('-created_at')[:3]

    # Toutes les news actives pour la liste principale
    all_news = News.objects.filter(is_active=True).select_related('author').order_by('-created_at')

    # Pagination : 6 news par page
    paginator = Paginator(all_news, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recent_news': recent_news,
        'page_obj': page_obj,
    }
    return render(request, 'core/news_list.html', context)
# @login_required
# def detail_news(request, news_id):
#     news = get_object_or_404(News, id=news_id, is_active=True)

#     # --- Like / Unlike ---
#     if request.method == "POST" and "like_news" in request.POST:
#         if request.user in news.likes.all():
#             news.likes.remove(request.user)
#         else:
#             news.likes.add(request.user)
#         return redirect("detail_news", news_id=news.id)

#     # --- Nouveau commentaire ---
#     if request.method == "POST" and "comment_submit" in request.POST:
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.news = news
#             comment.author = request.user
#             comment.save()
#             return redirect("detail_news", news_id=news.id)
#     else:
#         comment_form = CommentForm()

#     # --- Réponse à un commentaire ---
#     if request.method == "POST" and "reply_submit" in request.POST:
#         reply_id = request.POST.get("reply_to")
#         parent_comment = get_object_or_404(Comment, id=reply_id)
#         reply_form = ReplyCommentForm(request.POST)
#         if reply_form.is_valid():
#             reply = reply_form.save(commit=False)
#             reply.comment = parent_comment
#             reply.author = request.user
#             reply.save()
#             return redirect("detail_news", news_id=news.id)
#     else:
#         reply_form = ReplyCommentForm()

#     comments = news.comments.filter(is_active=True).select_related('author').prefetch_related('replies__author')

#     context = {
#         "news": news,
#         "comments": comments,
#         "comment_form": comment_form,
#         "reply_form": reply_form,
#     }

#     return render(request, "core/detail_news.html", context)

# @login_required
# def mes_paiements_contributions(request):

#     paiements = PaiementContribution.objects.filter(
#         user=request.user
#     ).order_by("-date_paiement")

#     context = {
#         "paiements": paiements
#     }

#     return render(
#         request,
#         "core/mes_paiements_contributions.html",
#         context
#     )
# @login_required
# def mes_contributions(request):
#     today = timezone.localdate()

#     ContributionJour.objects.filter(
#         user=request.user,
#         date__lt=today
#     ).exclude(
#         statut="paid"
#     ).update(statut="missed")

#     contributions = ContributionJour.objects.filter(
#         user=request.user
#     ).exclude(
#         statut="paid"
#     ).order_by("date")

#     if request.method == "POST":

#         contribution_ids = request.POST.getlist("contributions")

#         if not contribution_ids:
#             messages.error(request, "Veuillez sélectionner au moins une contribution.")
#             return redirect("mes_contributions")

#         request.session["contributions_selectionnees"] = contribution_ids

#         return redirect("paiement_contribution")

#     total_manque = contributions.filter(statut="missed").count()
#     total_pending = contributions.filter(statut="pending").count()

#     montant_total_global = sum(
#         c.montant or Decimal("0") for c in contributions
#     )

#     context = {
#         "contributions": contributions,
#         "total_manque": total_manque,
#         "total_pending": total_pending,
#         "montant_total_global": montant_total_global,
#     }

#     return render(request, "core/mes_contributions.html", context)



# @login_required
# def paiement_contribution(request):

#     contribution_ids = request.session.get("contributions_selectionnees")

#     if not contribution_ids:
#         messages.error(request, "Aucune contribution sélectionnée.")
#         return redirect("mes_contributions")

#     contributions = ContributionJour.objects.filter(
#         id__in=contribution_ids,
#         user=request.user
#     ).exclude(statut="paid")

#     montant_total = sum(
#         c.montant or Decimal("0") for c in contributions
#     )

#     if request.method == "POST":

#         form = PaiementContributionForm(request.POST)

#         if form.is_valid():

#             paiement = form.save(commit=False)
#             paiement.user = request.user
#             paiement.statut = "pending"
#             paiement.save()

#             paiement.contributions.set(contributions)

#             del request.session["contributions_selectionnees"]

#             messages.success(
#                 request,
#                 "Votre paiement a été envoyé et sera vérifié par l'administrateur."
#             )

#             return redirect("mes_contributions")

#     else:
#         form = PaiementContributionForm(
#             initial={"montant_total": montant_total}
#         )

#     context = {
#         "form": form,
#         "contributions": contributions,
#         "montant_total": montant_total,
#     }

#     return render(request, "core/paiement_contribution.html", context)
# @login_required
# def mes_contributions(request):
#     today = timezone.localdate()

#     # Marquer automatiquement les anciennes contributions non payées comme manquées
#     ContributionJour.objects.filter(
#         user=request.user,
#         date__lt=today
#     ).exclude(
#         statut="paid"
#     ).update(statut="missed")

#     # On n'affiche pas les contributions déjà payées
#     contributions = ContributionJour.objects.filter(
#         user=request.user
#     ).exclude(
#         statut="paid"
#     ).order_by("date")

#     if request.method == "POST":
#         contribution_ids = request.POST.getlist("contributions")
#         phone_number = request.POST.get("phone_number")
#         id_transaction = request.POST.get("id_transaction")

#         if not contribution_ids:
#             messages.error(request, "Veuillez sélectionner au moins une contribution.")
#             return redirect("mes_contributions")

#         contributions_selectionnees = ContributionJour.objects.filter(
#             id__in=contribution_ids,
#             user=request.user
#         ).exclude(statut="paid")

#         if not contributions_selectionnees.exists():
#             messages.error(request, "Aucune contribution valide sélectionnée.")
#             return redirect("mes_contributions")

#         montant_total = sum(
#             contribution.montant or Decimal("0")
#             for contribution in contributions_selectionnees
#         )

#         paiement = PaiementContribution.objects.create(
#             user=request.user,
#             montant_total=montant_total,
#             phone_number=phone_number,
#             id_transaction=id_transaction,
#             statut="pending"
#         )

#         paiement.contributions.set(contributions_selectionnees)

#         messages.success(
#             request,
#             "Votre demande de paiement a été envoyée avec succès."
#         )
#         return redirect("mes_contributions")

#     total_manque = contributions.filter(statut="missed").count()
#     total_pending = contributions.filter(statut="pending").count()
#     montant_total_global = sum(
#         contribution.montant or Decimal("0") for contribution in contributions
#     )

#     context = {
#         "contributions": contributions,
#         "total_manque": total_manque,
#         "total_pending": total_pending,
#         "montant_total_global": montant_total_global,
#     }
#     return render(request, "core/mes_contributions.html", context)