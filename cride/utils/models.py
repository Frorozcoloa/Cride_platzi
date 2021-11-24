"""Django models utilities."""

from django.db import models

class CRideModel(models.Model):
    """CRide base model.

    All CRide's models should inherit from this one.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the model was created.'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        )
    
    class Meta:
        abstract = True
        get_latest_by  ='created'
        ordering = ['-created', '-modified']