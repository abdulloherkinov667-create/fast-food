from django.shortcuts import render


def profile_page(request):
    return render(request, "user_page/profil_page.html")