from rest_framework import permissions

class IsAuthorOrModerator(permissions.BasePermission):
    """
    Permette la modifica/cancellazione solo all'autore del contenuto o a un moderatore.
    La lettura (GET) è permessa a tutti gli utenti autenticati.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
    
        is_author = (obj.author == request.user)
        is_moderator = (request.user.role == 'moderator')
        
        return is_author or is_moderator