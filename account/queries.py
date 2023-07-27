from django.contrib.auth import models as auth_models
from django.db.models import Exists, OuterRef

from account import models


def get_user_group(user_id: int):
    subquery = models.User.objects.filter(pk=user_id, groups=OuterRef("pk")).values(
        "id"
    )
    return auth_models.Group.objects.annotate(granted=Exists(subquery))
