from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('signout',views.signout, name='signout'),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path('update_profile',views.update_profile, name='update_profile'),
    path("supporteur/create/", views.supporteur_create, name="supporteur_create"),
    path("payer-supporteurs/", views.payer_supporteurs, name="payer_supporteurs"),
    path(
    "supporteur/<int:pk>/",
    views.supporteur_detail,
    name="supporteur_detail"
    ),
    
    path(
    "supporteur/carte-image/<int:supporteur_id>/",
    views.telecharger_carte_supporteur_image,
    name="telecharger_carte_supporteur_image",
     ),
    path('supporteur/<int:supporteur_id>/modifier/', views.modifier_carte_supporteur, name='modifier_supporteur'),

    # Suppression d'une carte supporteur
    path('supporteur/<int:supporteur_id>/supprimer/', views.supprimer_carte_supporteur, name='supprimer_supporteur'),
    # Vérification QR code via formulaire
    path("supporteur/verifier-qr/", views.verifier_qr, name="verifier_qr"),

    # Vérification QR code en AJAX / temps réel
    path("supporteur/verifier-qr-ajax/", views.verifier_qr_ajax, name="verifier_qr_ajax"),

    # Page scanner QR code
    path("supporteur/scanner-qr/", views.verifier_qr_scanner, name="verifier_qr_scanner"),
    path("journal/", views.journal_list, name="journal_list"),
    path("createurs/", views. liste_createurs_supporteur, name="liste_createurs"),
    path(
        "supporteurs/stats/",
        views.supporteurs_dashboard_stats,
        name="supporteurs_dashboard_stats"
    ),
    path("supporteurs/", views.supporteurs_list, name="supporteurs_list"),
    path("paiements-supporteurs/", views.liste_paiements_supporteurs, name="mes_paiements_supporteurs"),
    path("paiements-supporteurs/<int:user_id>/", views.liste_paiements_supporteurs, name="paiements_supporteurs_user"),
    path("mes-contributions/", views.mes_contributions, name="mes_contributions"),
    path("paiement-contribution/", views.paiement_contribution, name="paiement_contribution"),
    path(
    "mes-paiements-contributions/",
    views.mes_paiements_contributions,
    name="mes_paiements_contributions"
    ),
    path(
    "paiements-contributions/",
    views.liste_paiements_contributions,
    name="liste_paiements_contributions"
     ),
    path(
    "depenses/",
    views.liste_depenses,
    name="liste_depenses"
    ),
    path(
    "depense/<int:depense_id>/",
    views.detail_depense,
    name="detail_depense"
    ),
    path('news/<int:news_id>/', views.detail_news, name='detail_news'),
    path('news/', views.news_list, name='news_list'),
    path("devenir-supporteur/", views.creer_supporteur_public, name="creer_supporteur_public"),
    path("payer-supporteur/", views.payer_supporteur_unique, name="payer_supporteur_unique"),
    
]