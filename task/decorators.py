from django.http import HttpResponse
from django.shortcuts import redirect
import sweetify

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                sweetify.warning(request, title='Warning', text='You have to log out first to access that page', icon='warning', button='Ok')
                return redirect('dashboard')
            else:
                sweetify.warning(request, title='Warning', text='You have to log out first to access that page', icon='warning', button='Ok')
                return redirect('user-page')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                sweetify.warning(request, title='Warning', text='You are not authorized to view that page', icon='warning', button='Ok')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'worker':
            sweetify.warning(request, title='Warning', text='You are not authorized to view that page', icon='warning', button='Ok')
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
