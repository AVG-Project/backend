from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    ##t
    def update_user(self, **kwargs):
        print('\n UserManager update_user\n')
        print('\nkwargs = \n', kwargs)
    ##t

    def create_user(self, email, password=None, **kwargs):
        print('\n UserManager create_user\n')
        if not email:
            raise ValueError('Введи E-Mail.')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_verified = True
        user.save(using=self._db)
        return user

