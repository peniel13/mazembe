from django.db import models

# Create your models here.


from django.db import models

class PresidentClub(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, blank=True, null=True)

    image = models.ImageField(
        upload_to="presidents/",
        blank=True,
        null=True
    )

    biographie = models.TextField(blank=True, null=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"