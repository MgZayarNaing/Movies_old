import uuid
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers
from .models import CustomUser
from .serializers import CustomUserSerializer
from .pagination import CustomUserPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_approved:
            raise serializers.ValidationError('Your account is not approved yet.')
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = CustomUser.objects.all().order_by('uuid')  # Ensure the queryset is ordered by UUID
    paginator = CustomUserPagination()
    paginated_users = paginator.paginate_queryset(users, request)
    serializer = CustomUserSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([AllowAny])  # Allow any user to access this endpoint
def user_create(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = CustomUser.objects.get(uuid=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def user_update(request, pk):
    try:
        user = CustomUser.objects.get(uuid=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CustomUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def user_delete(request, pk):
    try:
        user = CustomUser.objects.get(uuid=pk)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def update_user_approval(request, pk):
    try:
        user = CustomUser.objects.get(uuid=pk)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    user.is_approved = True
    user.save()
    return Response({"detail": "User approved successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def not_approved(request):
    return Response({"detail": "Your account is pending approval by an admin."}, status=status.HTTP_403_FORBIDDEN)


# Update user password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Password has been changed successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Token generator
class TokenGenerator(PasswordResetTokenGenerator):
    pass

token_generator = TokenGenerator()

# Custom token obtain pair serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_approved:
            raise serializers.ValidationError('Your account is not approved yet.')

        return data

# Custom token obtain pair view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Password reset request
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def password_reset_request(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user:
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('password-reset-confirm', args=[uid, token]))

            subject = "Password Reset Request"
            message = f"Hi {user.email},\n\nPlease click the link below to reset your password:\n{reset_link}\n\nThank you."
            
            send_mail(
                subject,
                message,
                'zayarnaing101120@gmail.com',  # DEFAULT_FROM_EMAIL
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No user found with that email address."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField()

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def password_reset_confirm(request, uidb64, token):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(CustomUser, pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)