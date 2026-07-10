from rest_framework import permissions

class IsFollowParticipantOrModerator(permissions.BasePermission):
    """
    Permesso personalizzato: un follow può essere rimosso solo dal follower (chi segue),
    dal followed (chi è seguito) o da un moderatore.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == 'moderator':
            return True

        # Controllo se l'utente è uno dei due partecipanti alla relazione di following
        is_follower = (request.user == obj.follower)
        is_followed = (request.user == obj.followed)

        return is_follower or is_followed