from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
# from django.db.models import Q
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from core.models import Citoyen, DocumentJustificatif, Temoin
# from core.forms import CitoyenForm, DocumentJustificatifForm, TemoinForm

# from django.db.models import Q
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# def index(request):
#     query = request.GET.get("q", "").strip()
#     citoyens = None

#     if query:
#         mots = query.split()
#         q_objects = Q()

#         for mot in mots:
#             if mot.isdigit() and len(mot) <= 4:  
#                 # Recherche par les derniers chiffres de la carte
#                 q_objects |= Q(numero_identite__endswith=mot)
#             else:
#                 # Recherche par prénom, nom ou postnom
#                 q_objects |= (
#                     Q(prenom__icontains=mot) |
#                     Q(nom__icontains=mot) |
#                     Q(postnom__icontains=mot)
#                 )

#         citoyens_qs = Citoyen.objects.filter(q_objects).order_by("-date_creation")

#         # Pagination
#         paginator = Paginator(citoyens_qs, 6)
#         page = request.GET.get("page")
#         try:
#             citoyens = paginator.page(page)
#         except PageNotAnInteger:
#             citoyens = paginator.page(1)
#         except EmptyPage:
#             citoyens = paginator.page(paginator.num_pages)

#     return render(request, "base/index.html", {
#         "query": query,
#         "citoyens": citoyens,
#     })


from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core.models import Supporteur,PaiementContribution,Depense,News

def abbreviate_number(value):
    """
    Transforme un nombre en version courte lisible :
    1200 -> 1.2k, 1500000 -> 1.5M
    """
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M".rstrip("0").rstrip(".")
    elif value >= 1_000:
        return f"{value/1_000:.1f}k".rstrip("0").rstrip(".")
    else:
        return str(value)
    
from django.db.models import Sum
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render
from django.db.models import Sum, Q
from core.models import Supporteur, PaiementContribution, Depense, News

def index(request):
    query = request.GET.get("q", "").strip()
    supporteurs = None

    # Statistiques Supporteurs
    total_supporteurs = Supporteur.objects.filter(statut="valid").count()
    total_supporteurs_formate = abbreviate_number(total_supporteurs)
    total_valides = Supporteur.objects.filter(statut="valid").count()
    total_attente = Supporteur.objects.filter(statut="pending").count()

    # 3 derniers paiements validés
    recent_paiements = PaiementContribution.objects.filter(
        statut="validated"
    ).select_related("user").order_by("-date_paiement")[:3]

    # 3 dernières dépenses
    recent_depenses = Depense.objects.select_related(
        "rubrique"
    ).order_by("-date_depense")[:3]

    # 3 dernières news
    recent_news = News.objects.filter(is_active=True).select_related('author')[:3]

    # 💰 Total paiements contributions validés
    total_paiements = PaiementContribution.objects.filter(
        statut="validated"
    ).aggregate(total=Sum('montant_total'))['total'] or 0

    # 🧾 Total dépenses
    total_depenses = Depense.objects.aggregate(total=Sum('montant'))['total'] or 0

    # 🔹 Solde restant
    solde_rest = total_paiements - total_depenses

    # Recherche supporteurs
    if query:
        mots = query.split()
        q_objects = Q()
        for mot in mots:
            if mot.isdigit() and len(mot) <= 4:  
                q_objects |= Q(numero_supporteur__endswith=mot)
            else:
                q_objects |= Q(prenom__icontains=mot) | Q(nom__icontains=mot) | Q(postnom__icontains=mot)

        # supporteur_qs = Supporteur.objects.filter(q_objects).order_by("-date_creation")
        # 🔹 Filtrer uniquement les supporteurs validés
        supporteur_qs = Supporteur.objects.filter(q_objects, statut="valid").order_by("-date_creation")

        # Pagination
        paginator = Paginator(supporteur_qs, 6)
        page = request.GET.get("page")
        try:
            supporteurs = paginator.page(page)
        except PageNotAnInteger:
            supporteurs = paginator.page(1)
        except EmptyPage:
            supporteurs = paginator.page(paginator.num_pages)

    return render(request, "base/index.html", {
        "query": query,
        "supporteurs": supporteurs,
        # "total_supporteurs": total_supporteurs,
        "total_supporteurs": total_supporteurs_formate,
        "total_valides": total_valides,
        "total_attente": total_attente,
        "recent_paiements": recent_paiements,
        "recent_depenses": recent_depenses,
        "recent_news": recent_news,
        'total_paiements': total_paiements,
        'total_depenses': total_depenses,
        'solde_rest': solde_rest,
    })


from django.shortcuts import render
from .models import PresidentClub

def apropos(request):
    president = PresidentClub.objects.first()  # on prend le président actif

    context = {
        "president": president
    }

    return render(request, "base/apropos.html", context)
# def index(request):
#     query = request.GET.get("q", "").strip()
#     supporteurs = None
#     # 📊 Statistiques
#     total_supporteurs = Supporteur.objects.count()
#     total_valides = Supporteur.objects.filter(statut="valid").count()
#     total_attente = Supporteur.objects.filter(statut="pending").count()
#     # 💰 3 derniers paiements validés
#     recent_paiements = PaiementContribution.objects.filter(
#         statut="validated"
#     ).select_related("user").order_by("-date_paiement")[:3]
#     # 🧾 3 dernières dépenses
#     recent_depenses = Depense.objects.select_related(
#         "rubrique"
#     ).order_by("-date_depense")[:3]
#     # --- Récupérer les 3 dernières news actives ---
#     recent_news = News.objects.filter(is_active=True).select_related('author')[:3]
#     # Paiements contributions validés uniquement
#     total_paiements = PaiementContribution.objects.filter(statut="validated").aggregate(
#         total=Sum('montant_total')
#     )['total'] or 0

#     # Dépenses contributions
#     total_depenses = Depense.objects.aggregate(total=Sum('montant_total'))['total'] or 0

#     # Solde restant
#     solde_rest = total_paiements - total_depenses
    
#     if query:
#         mots = query.split()
#         q_objects = Q()

#         for mot in mots:
#             if mot.isdigit() and len(mot) <= 4:  
#                 # Recherche par les derniers chiffres de la carte
#                 q_objects |= Q(numero_supporteur__endswith=mot)
#             else:
#                 # Recherche par prénom, nom ou postnom
#                 q_objects |= (
#                     Q(prenom__icontains=mot) |
#                     Q(nom__icontains=mot) 
                    
#                 )

#         supporteur_qs = Supporteur.objects.filter(q_objects).order_by("-date_creation")

#         # Pagination
#         paginator = Paginator(supporteur_qs, 6)
#         page = request.GET.get("page")
#         try:
#             supporteurs = paginator.page(page)
#         except PageNotAnInteger:
#             supporteurs = paginator.page(1)
#         except EmptyPage:
#             supporteurs = paginator.page(paginator.num_pages)

#     return render(request, "base/index.html", {
#         "query": query,
#         "supporteurs":  supporteurs,
#         "total_supporteurs": total_supporteurs,
#         "total_valides": total_valides,
#         "total_attente": total_attente,
#         "recent_paiements": recent_paiements,
#         "recent_depenses": recent_depenses,
#         "recent_news": recent_news,
#         'total_paiements': total_paiements,
#         'total_depenses': total_depenses,
#         'solde_rest': solde_rest,
#     })
