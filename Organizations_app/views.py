from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.conf import settings
from .models import User, Organisation, Member, Role
from rest_framework.response import Response
from rest_framework import status
# from .utils import generate_jwt_tokens
from django.utils.encoding import force_bytes, force_str
import resend
from resend import Emails
from resend.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.http import JsonResponse
import json
import jwt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .utils import account_activation_token

from datetime import datetime, timedelta

def sign_up(request):
    return render(request,"sign_up.html")
def sign_in(request):
    return render(request,"sign_in.html")
def forgetpassword(request):
    return render(request,"reset.html")



def generate_jwt_tokens(user):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    refresh_expiration_time = datetime.utcnow() + timedelta(days=7)

    payload = {
        'user_id': user.id,
        'exp': expiration_time,
        'iat': datetime.utcnow(),
    }
    
    refresh_payload = {
        'user_id': user.id,
        'exp': refresh_expiration_time,
        'iat': datetime.utcnow(),
    }

    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access': access_token,
        'refresh': refresh_token
    }   
resend.api_key = "re_Wf46ahPk_CFMYenNvUf5wp8vYPrcMahvr"



@api_view(['POST'])
def SignInView(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    print(password,email)
    user = User.objects.get(email=email)
    if user.password == password:
        tokens = generate_jwt_tokens(user)
        params = {
                "from": "Acme <onboarding@resend.dev>",
                "to": [email],
                "subject": "Welcome!",
                "html": "<p>You have been signed In successfully.</p>"
            }

        email_response = resend.Emails.send(params)
        print(email_response)
        return Response(tokens, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
        
def SignUpView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            org_name = data.get('org_name')
            print(email, password, org_name)
            
            if not email or not password or not org_name:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'A user with this email already exists'}, status=400)

            user = User(
                email=email,
                password=password,
                created_at=int(timezone.now().timestamp()),
                updated_at=int(timezone.now().timestamp())
            )
            user.save()

            org = Organisation(
                name=org_name,
                created_at=int(timezone.now().timestamp()),
                updated_at=int(timezone.now().timestamp())
            )
            org.save()

            role = Role(
                name='Owner',
                org_id=org  
            )
            role.save()

            member = Member(
                user_id=user,
                org_id=org,  
                role_id=role,  
                created_at=int(timezone.now().timestamp()),
                updated_at=int(timezone.now().timestamp())
            )
            member.save()

            tokens = generate_jwt_tokens(user)

            params = {
                "from": "Acme <onboarding@resend.dev>",
                "to": [email],
                "subject": "Welcome!",
                "html": "<p>You have been signed up successfully.</p>"
            }

            email_response = resend.Emails.send(params)
            print(email_response)

            return JsonResponse(tokens, status=201)
        
        except resend.exceptions.ValidationError as e:
            print(f"Error sending email: {e}")
            return JsonResponse({'error': 'Failed to send email'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
def ResetPasswordRequest(request):
    data = json.loads(request.body)
    email = data.get('email')
    user = User.objects.filter(email=email).first()
    print(user, email)
    
    if not user:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    token = account_activation_token.make_token(user)
    print("Token:", token)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
    
    params = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [email],
        "subject": 'Password Reset Request',
        "html": f'Please use the following link to reset your password: {reset_link}'
    }

    email_response = resend.Emails.send(params)
    print(email_response)
    return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def ResetPasswordConfirm(request,uidb64,token):
    data = json.loads(request.body)
    new_password = data.get('password')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

    if default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password has been reset'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
