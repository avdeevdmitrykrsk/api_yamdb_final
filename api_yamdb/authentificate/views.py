from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .utils import create_confirmation_code, send_confirmation_email
from .serializers import SignUpSerializer


User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = create_confirmation_code(user)
        send_confirmation_email(user, confirmation_code)
        return Response({'detail': 'Код подтверждения выслан!'}, status=status.HTTP_200_OK)
