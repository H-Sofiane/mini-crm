from django import forms
from .models import Contact, Note, PieceJointe

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["nom", "prenom", "email", "photo", "entreprise"]



from .models import Entreprise

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ["nom", "adresse", "ville", "pays", "site_web", "logo"]



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["contenu"]
        widgets = {
            "contenu": forms.Textarea(attrs={"rows": 3})
        }


class PieceJointeForm(forms.ModelForm):
    class Meta:
        model = PieceJointe
        fields = ["fichier", "nom"]

