from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import MyUser as user


def is_email_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validate_mail(email):
    if user.objects.filter(**{'{}__iexact'.format(user.USERNAME_FIELD): email}).exists():
        raise ValidationError('User with this {} already exists'.format(user.USERNAME_FIELD))
    elif not is_email_valid(email):
        raise ValidationError('invalid {}'.format(user.USERNAME_FIELD))
    return email