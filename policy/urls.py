#policy/urls.py

#importaciones de rest_framework
from rest_framework.routers import DefaultRouter

#importaciones de views
from .views import PolicyViewSet

#crear router
router = DefaultRouter()

#registrar viewset
router.register(r'policy', PolicyViewSet, basename='policy')

#urls
urlpatterns = router.urls
