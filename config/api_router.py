from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from core.blogs.api.views import BlogViewSet
from core.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("blogs", BlogViewSet, basename="blogs")


app_name = "api"
urlpatterns = router.urls
