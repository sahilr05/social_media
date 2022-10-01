import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from .exception import BadRequestException
from .exception import ValidationException


def custom_exception_handler(exc, context):
    # exception_handler(exc, context)
    # exception_class = exc.__class__.__name__  ,if class name required

    exc_type, exc_value, exc_traceback = sys.exc_info()
    trace = traceback.format_tb(exc_traceback)

    response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, ObjectDoesNotExist):
        response_status = status.HTTP_404_NOT_FOUND
    if isinstance(exc, PermissionDenied):
        response_status = status.HTTP_403_FORBIDDEN
    if (
        isinstance(exc, BadRequestException)
        or isinstance(exc, ValidationException)
        or isinstance(exc, ValidationError)
    ):
        # trace = traceback.format_exc().splitlines()
        response_status = status.HTTP_400_BAD_REQUEST
    return Response(
        data={"ErrorCode": str(exc), "Cause": trace},
        status=response_status,
    )
