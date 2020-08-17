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
    return Flag.objects \
        .filter( 
            Q(chain__parent__in= \
                Flag.objects \
                    .filter(
                        submit__captured=True
                    ) \
                    .filter(
                        submit__user=user
                    )
            ) |
            Q(chain__parent__exact=None)
        ).order_by(order_by)


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