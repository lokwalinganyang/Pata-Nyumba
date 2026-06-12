from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def landlord_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to landlord login instead of admin login
            from django.shortcuts import redirect
            return redirect('manyumbavacant:landlord_login')
        if not hasattr(request.user, 'landlord'):
            raise PermissionDenied("You are not registered as a landlord.")
        return view_func(request, *args, **kwargs)
    return wrapper