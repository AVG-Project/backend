from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone, password):
        if not email or not phone:
            raise ValueError('Введи E-Mail и номер телефона')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_verified = True
        user.save(using=self._db)
        return user






    # def _create_user(self, email=None, phone=None,
    #                  password=None, **extra_fields):
    #     """
    #     Creates and saves a User with the given email and password.
    #     """
    #     if not email or not phone:
    #         raise ValueError('Поля email и телефон обязательны.')
    #
    #     email = self.normalize_email(email)
    #     email = email.lower()
    #
    #     user = self.model(
    #         email=email,
    #         phone=phone,
    #         **extra_fields
    #     )
    #
    #     # проверяем является ли пользователь
    #     # суперпользователем
    #     if extra_fields.get('is_admin'):
    #         user = self.model(
    #             email=email,
    #             phone=phone,
    #             **extra_fields
    #         )
    #
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    #
    # def create_user(self, email, phone, password=None, **extra_fields):
    #     extra_fields.setdefault('is_admin', False)
    #     return self._create_user(email=email, phone=phone, password=password, **extra_fields)
    #
    # def create_superuser(self, email, phone, password, **extra_fields):
    #     extra_fields.setdefault('is_admin', True)
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_active', True)
    #
    #     if extra_fields.get('is_admin') is not True:
    #         raise ValueError('Админ должен иметь is_admin=True.')
    #
    #     return self._create_user(
    #         email=email,
    #         phone=phone,
    #         password=password,
    #         **extra_fields
    #     )
