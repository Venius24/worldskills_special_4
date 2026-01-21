from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)
    preferred_delivery = models.CharField(
        max_length=10,
        choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')],
        default='delivery'
    )
    security_question = models.ForeignKey(
        'SecurityQuestion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    security_answer = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class SecurityQuestion(models.Model):
    question = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Kazakhstan')
    is_preferred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def save(self, *args, **kwargs):
        if self.is_preferred:
            Address.objects.filter(user=self.user, is_preferred=True).update(is_preferred=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} - {self.user.email}"