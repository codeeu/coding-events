__author__ = 'svetka'

from django.db import models


class EventSelectorManager(models.Manager):
    """
    We overwrite the standard manager for Event model to fetch only the entries with PENDING status
    """

    def __init__(self, status, *args, **kwargs):
        self.status = status
        super(EventSelectorManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super(
            EventSelectorManager,
            self).get_queryset().filter(
            status=self.status)
