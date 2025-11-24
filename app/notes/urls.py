from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('notes', views.NoteViewSet,'note')

urlpatterns = router.urls