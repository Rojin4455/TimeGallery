from django.shortcuts import redirect
from django.urls import reverse_lazy
from functools import wraps

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Modify this logic as needed
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('admin_app:admin_login'))
    
    return wrapped_view
