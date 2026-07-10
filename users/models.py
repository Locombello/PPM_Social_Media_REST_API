from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('standard', 'Standard User'),
        ('moderator', 'Moderator'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='standard')
    bio = models.TextField(blank=True, max_length=500)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Evita che un utente segua la stessa persona più volte
        unique_together = ('follower', 'followed')

        # Impedisce a livello di database che follower e followed siano uguali
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F('followed')),
                name='prevent_self_follow'
            )
        ]