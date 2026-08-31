from django.http import HttpResponse


def campagne_list(request):
    return HttpResponse("Marketing - campagnes")


def creer_campagne(request):
    return HttpResponse("Marketing - créer une campagne")
