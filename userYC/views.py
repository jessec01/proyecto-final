from django.views.generic.base import TemplateView
from rest_framework.views import APIView    
from .serializer import UserYCSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from django.db import transaction
class RegisterView(TemplateView):
    template_name = "userYC/register.html"  

class SaveUserView(APIView):
    serializer_class = UserYCSerializer
    permission_classes = [AllowAny] # 
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        
        try: 

            serializer.is_valid(raise_exception=True)   
            serializer.save()
        
        except serializers.ValidationError as ve:
            return Response({"error": str(ve)}, status=400) 
        except transaction.TransactionManagementError as te:
            return Response({"error": "Database transaction error: " + str(te)}, status=500) 
        return Response(serializer.data, status=201)
    
    # Permitir acceso sin autenticación
#se programa mas tarde
class Error404View(TemplateView):
    template_name = "userYC/404.html"
class LoginView(TemplateView):
    template_name = "userYC/login.html"
