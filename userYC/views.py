#userYC/views.py

#importaciones de django
from django.db import transaction, IntegrityError, OperationalError
from django.views.generic.base import TemplateView

#importaciones de rest_framework

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView    
#importaciones internas
from .serializer import UserYCSerializer
from userYC.models import User
from .serializer import ( 
                         DetailUserYCSerializer, 
                         ListUserYCSerializer)
class RegisterView(TemplateView):
    template_name = "userYC/register.html"  

class SaveUserView(APIView):
    serializer_class = UserYCSerializer
    permission_classes = [AllowAny] # 
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        
        try: 

            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
        
        except serializers.ValidationError as ve:
            return Response({"error": str(ve)}, status=400) 
        except IntegrityError as ie:
            return Response({"error": "Integrity error: " + str(ie)}, status=409)
        except OperationalError as oe:
            return Response({"error": "Database unavailable: " + str(oe)}, status=503)
        except transaction.TransactionManagementError as te:
            return Response({"error": "Database transaction error: " + str(te)}, status=500)
        except Exception:
            return Response({"error": "Internal server error"}, status=500)
        return Response(serializer.data, status=201)
    
    # Permitir acceso sin autenticación
#vista de template para la manipulacion 
class UserYCProfileTemplateView(TemplateView):
    template_name = "userYC/userYC.html"
#vista de manipular los datos basicos del usuario
class UserYCViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
       return User.objects.all()
    def get_serializer_class(self):
        #crear
        if self.action == 'create':
            return UserYCSerializer
        #editar
        elif self.action in ['update', 'partial_update']:
            return UserYCSerializer
        #detalle
        elif self.action == 'retrieve':
            return DetailUserYCSerializer
        #borrar (no necesitas ejecutar destroy aquí, solo retornar un serializer por defecto)
        elif self.action == 'destroy':
            return UserYCSerializer
        #lista
        return ListUserYCSerializer

#se programa mas tarde
class Error404View(TemplateView):
    template_name = "userYC/404.html"
class LoginView(TemplateView):
    template_name = "userYC/login.html"
