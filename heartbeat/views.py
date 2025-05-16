from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth.models import User
from .models import Heartbeat
from .serializers import HeartbeatSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


# Logout current refresh token (blacklist)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Logout all user sessions (blacklist all tokens)
class LogoutAllView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=token)
            except:
                continue
        return Response({"detail": "All sessions logged out."}, status=status.HTTP_205_RESET_CONTENT)


# Register user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


# List/Create Heartbeat records for authenticated user
class HeartbeatListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        heartbeats = Heartbeat.objects.filter(user=request.user).order_by('-timestamp')
        serializer = HeartbeatSerializer(heartbeats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HeartbeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
