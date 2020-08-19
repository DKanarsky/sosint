from django.db.models import Q

from .models import Flag, Submit

def is_captured(flag, user):
    return Submit.objects \
        .filter(
            user=user, 
            flag=flag, 
            captured=True) \
        .exists()


def available_flags(user, order_by='score'):
    if user.is_superuser:
        # admin see everything
        flags = Flag.objects.all()
    else:
        parent_captured = Q(chain__parent__in= \
            Flag.objects.filter(
                Q(submit__captured=True) & Q(submit__user=user)
                ))
        no_parent = Q(chain__isnull=True)
        parent_disabled = Q(chain__parent__enabled=False)
        chain_enabled = Q(chain__enabled=True)
        flags = Flag.objects \
            .filter(
                Q(((parent_captured | parent_disabled) & chain_enabled) | no_parent)
            ) \
            .filter(
                enabled=True
            )
    # exclude disabled groups
    flags.exclude(group__enabled=False)
    flags.order_by(order_by)
    return flags


def save_submit(user, flag, submit_value):
    error = False
    messages = []
    try:
        if is_captured(flag, user):
            messages.append("Данный флаг уже захвачен")
            error = True
    except Exception:
        messages.append("Непредвиденная ошибка")
        error = True
    finally:
        if not error:
            submit = Submit(flag=flag, user=user, value=submit_value)
            submit.save()
            if not submit.captured and not error:
                messages.append("Ответ невереный")
        return (error, messages)