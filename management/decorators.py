from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from functools import wraps

# Decorator per le FBV
def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'seller':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Accesso riservato ai fornitori")
    return _wrapped_view

# Mixin per le CBV
class SellerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'seller':
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Accesso riservato ai fornitori")
