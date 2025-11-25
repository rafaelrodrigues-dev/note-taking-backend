from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.NoteViewSet,'note')

urlpatterns = router.urls