from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название продукта')
    description = models.CharField(max_length=150, verbose_name='Описание продукта')
    picture = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Картинка продукта",
                                max_length=900)
    creation_date = models.DateTimeField(null=True, verbose_name='Дата создания продукта')
    price = models.IntegerField(verbose_name="Цена продукта")

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ['id', 'title']


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, blank=True, null=True, related_name='supplier', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['id', 'name']


class Discount(models.Model):
    discount = models.IntegerField()
    product = models.ForeignKey(Product, blank=True, null=True, related_name='discount', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.discount)

    class Meta:
        unique_together = ['id', 'discount']


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    description = models.CharField(max_length=150, verbose_name='Описание категории')
    product = models.ForeignKey(Product, blank=True, null=True, related_name='category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ['id', 'title']


class Cart(models.Model):
    session_key = models.CharField(max_length=999, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_cost = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user}{self.session_key}'

    def get_total(self):
        items = CartContent.objects.filter(cart=self.id)
        total = 0
        for item in items:
            total += item.product.price * item.qty
        return total

    def get_cart_content(self):
        items = CartContent.objects.all()
        return items


class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

