import uuid

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone

from reunion.exception import ValidationException
from social_app.models import Follow
from social_app.models import User


@transaction.atomic
def user_signup(*, first_name: str, last_name: str, email: str, password: str) -> User:

    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = make_password(password)
    user.save()
    return user


def user_detail(*, user: User):
    return user


@transaction.atomic
def follow_user(*, user: User, follow_user_id: User) -> None:
    follower = _valdiate_and_get_user(id=follow_user_id)
    _validate_follow_request(user=user, follower=follower)
    _save_follow_request(user=user, follower=follower)


@transaction.atomic
def unfollow_user(*, user: User, unfollow_user_id: User) -> None:
    follower = _valdiate_and_get_user(id=unfollow_user_id)
    _validate_unfollow_request(user=user, follower=follower)
    print("Unfollowing")
    follow_obj = _get_follow_obj(user=user, follower=follower)
    follow_obj.deleted_by_user = user
    follow_obj.deleted_datetime = timezone.now()
    print(follow_obj.deleted_datetime)
    follow_obj.save()


def _get_follow_obj(*, user: User, follower: User) -> Follow:
    return Follow.objects.get(
        user=user, follower=follower, deleted_datetime__isnull=True
    )


def _valdiate_and_get_user(*, id: uuid) -> User:
    return User.objects.get(user_id=id)


def _validate_follow_request(*, user: User, follower: User) -> None:
    if user == follower:
        raise ValidationException("You can't follow yourself")

    if Follow.objects.filter(
        user=user, follower=follower, deleted_datetime__isnull=True
    ).exists():
        raise ValidationException(f"You're already following {follower.name}")


def _validate_unfollow_request(*, user: User, follower: User) -> None:
    if user == follower:
        raise ValidationException("User and follower can't be the same")

    if not Follow.objects.filter(
        user=user, follower=follower, deleted_datetime__isnull=True
    ).exists():
        raise ValidationException(f"You're not following {follower.name}")


def _save_follow_request(*, user: User, follower: User) -> None:
    follow = Follow()
    follow.user = user
    follow.follower = follower
    follow.save()
