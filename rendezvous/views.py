from django.http import HttpResponse


def calendrier(request):
    return HttpResponse("Rendez-vous - calendrier")


def creer_creneau(request):
    return HttpResponse("Rendez-vous - créer un créneau")
