from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users import models
# User = get_user_model()
######
User = models.CustomUser
########

from djoser.signals import user_activated, user_updated, user_registered



@receiver(user_registered)
def check_registration_by_code(user, request, **kwargs):
    code = user.registration_by_code
    if code:
        friend_user = models.Loyalty.objects.filter(code=code).first()
        if friend_user:
            friend_user.increase_bonus_from_reference()




