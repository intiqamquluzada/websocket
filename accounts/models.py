from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError("İstifadəçinin elektron-poçtu olmalıdır")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=120, unique=True)
    name = models.CharField(max_length=40, verbose_name="Istifadəçi adı", blank=True, null=True)
    surname = models.CharField(max_length=40, verbose_name="Istifadəçi soyadı", blank=True, null=True)
    activation_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password_reset_code = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        if self.surname:
            return '%s %s' % (self.name, self.surname)
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


