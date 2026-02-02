from django.db import models

class Contact(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to="photos_contacts/", blank=True, null=True)
    entreprise = models.ForeignKey("Entreprise", on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

        return f"{self.prenom} {self.nom}"




class Entreprise(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    adresse = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    pays = models.CharField(max_length=100, blank=True)
    site_web = models.URLField(blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.nom



class Note(models.Model):
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE, related_name="notes")
    auteur = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note de {self.auteur} pour {self.contact}"



class PieceJointe(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="pieces_jointes")
    fichier = models.FileField(upload_to="pieces_jointes/")
    nom = models.CharField(max_length=255, blank=True)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom or self.fichier.name


