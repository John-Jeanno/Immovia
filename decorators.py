from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def admin_required(view_func):
    """Décorateur pour protéger les vues - accès admin seulement"""
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

class AdminRequiredMixin:
    """Mixin pour protéger les vues basées sur les classes"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
