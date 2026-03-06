#promotion/urls.py

#importaciones de rest_framework
from rest_framework.routers import DefaultRouter

#importaciones de views
from .views import PromotionViewSet

#crear router
router = DefaultRouter()

#registrar viewset
router.register(r'promotion', PromotionViewSet, basename='promotion')

#urls
urlpatterns = router.urls