from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm, NoteForm, PieceJointeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Entreprise
from .forms import EntrepriseForm

from django.core.paginator import Paginator

from django.db.models import Q



@login_required
def contact_create(request):
    form = ContactForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("contact_list")
    return render(request, "contacts/contact_form.html", {"form": form})

@permission_required('contacts.change_contact')
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, request.FILES or None, instance=contact)
    if form.is_valid():
        form.save()
        return redirect("contact_list")
    return render(request, "contacts/contact_form.html", {"form": form})

@permission_required('contacts.delete_contact')
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect("contact_list")
    return render(request, "contacts/contact_confirm_delete.html", {"contact": contact})




@login_required
def contact_list(request):
    # 1) Base queryset
    contacts = Contact.objects.all().order_by("nom")

    # 2) Restriction pour les utilisateurs non-staff
    if not request.user.is_staff:
        contacts = contacts.only("nom", "photo")

    # 3) Recherche
    query = request.GET.get("q")
    if query:
        contacts = contacts.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query)
        )

    # 4) Filtre entreprise
    entreprise_id = request.GET.get("entreprise")
    if entreprise_id:
        contacts = contacts.filter(entreprise_id=entreprise_id)

    entreprises = Entreprise.objects.all()


    sort = request.GET.get("sort", "nom")  # tri par défaut
    contacts = contacts.order_by(sort)



    # 4) Pagination
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 5) Render
    return render(request, "contacts/contact_list.html", 
                  {"page_obj": page_obj,
                   "entreprises": entreprises})



    

def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/contact_detail.html", {"contact": contact})


@login_required
def entreprise_list(request):
    entreprises = Entreprise.objects.all()
    return render(request, "entreprises/entreprise_list.html", {"entreprises": entreprises})


@permission_required("contacts.add_entreprise")
def entreprise_create(request):
    if request.method == "POST":
        form = EntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("entreprise_list")
    else:
        form = EntrepriseForm()

    return render(request, "entreprises/entreprise_form.html", {"form": form})


@login_required
def entreprise_detail(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    return render(request, "entreprises/entreprise_detail.html", {"entreprise": entreprise})


@permission_required("contacts.change_entreprise")
def entreprise_update(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)

    if request.method == "POST":
        form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect("entreprise_detail", pk=pk)
    else:
        form = EntrepriseForm(instance=entreprise)

    return render(request, "entreprises/entreprise_form.html", {"form": form})


@permission_required("contacts.delete_entreprise")
def entreprise_delete(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)

    if request.method == "POST":
        entreprise.delete()
        return redirect("entreprise_list")

    return render(request, "entreprises/entreprise_confirm_delete.html", {"entreprise": entreprise})



@login_required
def note_create(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.contact = contact
            note.auteur = request.user
            note.save()
            return redirect("contact_detail", pk=contact_id)
    else:
        form = NoteForm()

    return render(request, "notes/note_form.html", {"form": form, "contact": contact})



@login_required
def ajouter_piece_jointe(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == "POST":
        form = PieceJointeForm(request.POST, request.FILES)
        if form.is_valid():
            pj = form.save(commit=False)
            pj.contact = contact
            pj.save()
            return redirect("contact_detail", contact_id)
    else:
        form = PieceJointeForm()

    return render(request, "contacts/ajouter_piece_jointe.html", {"form": form, "contact": contact})



