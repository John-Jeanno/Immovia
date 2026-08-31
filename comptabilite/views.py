from django.http import HttpResponse


def tableau_bord(request):
    return HttpResponse("Comptabilité - tableau de bord")


def creer_operation(request):
    return HttpResponse("Comptabilité - création d'une opération")
