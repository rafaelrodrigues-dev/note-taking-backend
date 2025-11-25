from rest_framework.routers import SimpleRouter
from .views import UserModelViewSet

router = SimpleRouter()
router.register('', UserModelViewSet, 'user')

urlpatterns = router.urls