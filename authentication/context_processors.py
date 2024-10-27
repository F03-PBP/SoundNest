from django.contrib.auth.models import User

def user_context(request): # Passing user yang sedang login
    return {
        'last_login': request.COOKIES.get('last_login', 'Unknown'),
        'current_user': request.user if request.user.is_authenticated else None
    }