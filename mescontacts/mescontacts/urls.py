"""
URL configuration for mescontacts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from contacts import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Contacts
    path("contacts/", views.contact_list, name="contact_list"),
    path("contacts/create/", views.contact_create, name="contact_create"),
    path("contacts/<int:pk>/", views.contact_detail, name="contact_detail"),
    path("contacts/<int:pk>/update/", views.contact_update, name="contact_update"),
    path("contacts/<int:pk>/delete/", views.contact_delete, name="contact_delete"),
    path("contacts/<int:contact_id>/notes/add/", views.note_create, name="note_create"),

    path("contact/<int:contact_id>/piece-jointe/ajouter/", views.ajouter_piece_jointe, name="ajouter_piece_jointe"),



    # Entreprises
    path("entreprises/", views.entreprise_list, name="entreprise_list"),
    path("entreprises/create/", views.entreprise_create, name="entreprise_create"),
    path("entreprises/<int:pk>/", views.entreprise_detail, name="entreprise_detail"),
    path("entreprises/<int:pk>/update/", views.entreprise_update, name="entreprise_update"),
    path("entreprises/<int:pk>/delete/", views.entreprise_delete, name="entreprise_delete"),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    
]


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
