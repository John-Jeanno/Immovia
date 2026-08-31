from django.http import HttpResponse


def bail_list(request):
    return HttpResponse("Location - liste des baux")


def creer_bail(request):
    return HttpResponse("Location - créer un bail")
