from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.created_by_id:
            # Set the created_by field to the ID of the currently authenticated user
            self.created_by_id = getattr(settings, 'CURRENT_USER_ID', None)
        super().save(*args, **kwargs)
