import uuid
from typing import List

from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


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
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.created_by_user:
            self.created_by_user = user
        self.modified_by_user = user
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)
    username = None

    USERNAME_FIELD = "email"
    objects = UserManager()

    REQUIRED_FIELDS: List[str] = []

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def follower_count(self):
        return Follow.objects.filter(
            user_id=self.user_id, deleted_datetime__isnull=True
        ).count()

    @property
    def following_count(self):
        return Follow.objects.filter(
            follower_id=self.user_id, deleted_datetime__isnull=True
        ).count()


class Follow(BaseModel):
    follow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        to="social_app.User",
        on_delete=models.CASCADE,
        related_name="main_user",
    )
    follower = models.ForeignKey(
        to="social_app.User",
        on_delete=models.CASCADE,
        related_name="follower",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "follower"],
                condition=models.Q(deleted_datetime=None),
                name="unique_followers",
            )
        ]

    def __str__(self):
        return f"{self.user.first_name} is following {self.follower.first_name}"


class Post(BaseModel):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="post_user",
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return Like.objects.filter(post_id=self.post_id).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(
            post_id=self.post_id, deleted_datetime__isnull=True
        ).count()

    @property
    def comments(self):
        return Comment.objects.filter(
            post_id=self.post_id, deleted_datetime__isnull=True
        )


class Like(BaseModel):
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="like_user",
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="like_post",
    )


class Comment(BaseModel):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="comment_user",
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comment_post",
    )
    message = models.TextField(blank=True, null=True)
