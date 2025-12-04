from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class Note(models.Model):
    title = models.CharField(_("Note"), max_length=255)
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created_at"), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)

    def __str__(self):
        return self.title