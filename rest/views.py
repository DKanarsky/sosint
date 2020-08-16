from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest.serializers import FlagSerializer
from django.db.models import Q

from ctf.models import Flag, FlagChain, Submit

class FlagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows flags to be viewed.
    """
    serializer_class = FlagSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user

        flags = Flag.objects \
            .filter( 
                    Q(chain__parent__in= \
                        Flag.objects \
                            .filter(
                                submit__captured__exact=True
                            ) \
                            .filter(
                                submit__user__exact=user
                            )
                    ) |
                    Q(chain__parent__exact=None)
            ).order_by('score')

        return flags
