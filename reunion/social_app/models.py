from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid
# Create your models here.

class BaseModel(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    deleted_datetime = models.DateTimeField(null=True, blank=True)

    created_by_user = models.ForeignKey(
        to="social_app.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by_user_id",
    )
    modified_by_user = models.ForeignKey(
        to="social_app.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_modified_by_user_id",
    )
    deleted_by_user = models.ForeignKey(
        to="social_app.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_deleted_by_user_id",
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
