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