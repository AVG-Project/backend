from django.core.mail import send_mail
# from django.contrib.auth import get_user_model
# User = get_user_model()
from users.models import staff_email_list
from Istok.settings import SERVER_EMAIL, EMAIL_ADMIN


#todo включить перед запуском и тестами
def send_email_admin(subject, message):
    print('send_email_admin - ', SERVER_EMAIL)
    # send_mail(subject, message, SERVER_EMAIL, [EMAIL_ADMIN], fail_silently=True)
    pass


def send_email_staff(subject, message):
    print('send_email_staff - ', staff_email_list)
    # send_mail(subject, message, SERVER_EMAIL, staff_email_list)
    pass



def send_email_user(subject, message, user_email):
    print('send_email_user - ', user_email)
    # send_mail(subject, message, SERVER_EMAIL, [user_email], fail_silently=True)
    pass





