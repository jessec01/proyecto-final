#packages/urls.py

#importaciones de rest_framework
from rest_framework.routers import DefaultRouter

#importaciones de views
from .views import PackageViewSet

#crear router
router = DefaultRouter()

#registrar viewset
router.register(r'packages', PackageViewSet, basename='package')

#urls
urlpatterns = router.urLS