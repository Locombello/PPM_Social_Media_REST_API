from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import CustomUser, Follow
from .serializers import RegisterSerializer, FollowSerializer, UserSerializer
from .permissions import IsFollowParticipantOrModerator

# ==========================================
# REGISTRAZIONE E LOGOUT
# ==========================================
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    """Invalida il Refresh Token in modo che non possa più essere usato."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({"error": "Devi fornire il refresh token."}, status=status.HTTP_400_BAD_REQUEST)
                
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"status": "Logout completato con successo."}, status=status.HTTP_205_RESET_CONTENT)
            
        except Exception as e:
            return Response({"error": "Token non valido o già scaduto."}, status=status.HTTP_400_BAD_REQUEST)

# ==========================================
# VISUALIZZAZIONE PROFILI
# ==========================================
class UserDetailView(generics.RetrieveAPIView):
    """Gestisce la visualizzazione del profilo di un utente cercandolo per username"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'
    lookup_url_kwarg = 'username'

# ==========================================
# SEZIONE SEGUITI
# ==========================================
class FollowedListView(generics.ListCreateAPIView):
    """Gestisce la visualizzazione della lista degli utenti seguiti dall'utente loggato"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsFollowParticipantOrModerator]

    def get_queryset(self):
        return CustomUser.objects.filter(followers__follower=self.request.user).order_by('-followers__created_at')
    
    def create(self, request, *args, **kwargs):
        user_id_da_seguire = request.data.get('user_id')
        
        if not user_id_da_seguire:
            return Response({"error": "Devi fornire 'user_id' nel body."}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(user_id_da_seguire) == request.user.id:
            return Response({"error": "Non puoi seguire te stesso."}, status=status.HTTP_400_BAD_REQUEST)
            
        utente_da_seguire = get_object_or_404(CustomUser, id=user_id_da_seguire)
        
        # get_or_create evita di creare duplicati nel database
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=utente_da_seguire)
        
        if not created:
            return Response({"detail": "Segui già questo utente."}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(utente_da_seguire)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FollowedDetailView(generics.RetrieveDestroyAPIView):
    """
    GET: Mostra i dettagli di un utente specifico SOLO se lo segui.
    DELETE: Smetti di seguire l'utente (Unfollow).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return CustomUser.objects.filter(followers__follower=self.request.user)

    def perform_destroy(self, instance):
        # instance è l'utente da smettere di seguire
        Follow.objects.filter(follower=self.request.user, followed=instance).delete()
    
# ==========================================
# SEZIONE FOLLOWERS
# ==========================================
class FollowerListView(generics.ListAPIView):
    """Gestisce la visualizzazione della lista degli utenti che seguono l'utente loggato"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsFollowParticipantOrModerator]

    def get_queryset(self):
        return CustomUser.objects.filter(following__followed=self.request.user).order_by('-following__created_at')
    
class FollowerDetailView(generics.RetrieveDestroyAPIView):
    """
    GET: Mostra i dettagli di un utente specifico SOLO se ti segue.
    DELETE: Rimuovi l'utente dai tuoi follower.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return CustomUser.objects.filter(following__followed=self.request.user)

    def perform_destroy(self, instance):
        # instance è il follower da rimuovere.
        Follow.objects.filter(follower=instance, followed=self.request.user).delete()