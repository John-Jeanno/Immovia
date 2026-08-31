from django.http import HttpResponse


def liste_biens(request):
    return HttpResponse("Biens - liste")


def ajouter_bien(request):
    return HttpResponse("Biens - ajouter")
