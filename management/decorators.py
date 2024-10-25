from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from functools import wraps

from management.models import Laptop


# Decorator per le FBV
def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'seller':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Accesso riservato ai fornitori")
    return _wrapped_view

# Mixin per le CBV
#Controlla sia che lo user sia un seller, sia che il seller corrente sia colui che ha aggiunto il laptop
class SellerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        laptop = get_object_or_404(Laptop, pk=kwargs['pk'])
        if request.user.is_authenticated and request.user.user_type == 'seller':
            if laptop.seller_id == request.user.id:
                return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Accesso riservato ai fornitori oppure fornitore corrente diverso dal fornitore che ha aggiunto questo laptop")