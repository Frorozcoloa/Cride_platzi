"""Circle models."""


#Django
from django.db import models

#utilities
from cride.utils.models import CRideModel

class Circle(CRideModel):
    """
    Circle model.
    """

    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)

    #Stat 
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        "verified circle",
        help_text="Verified circles are also known as official communities",
        default=False
        )

    is_public = models.BooleanField(
        default=True,
        help_text="Public circles are listed in the main page so everyone know about their existence.",
    )

    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text="Limited circles can grow up to fixed number of members"
    )

    members_limit = models.PositiveIntegerField(
        default=0,
        help_text="If circles is limited, this will be the limit on the number of members",
    )

    def __str__(self):
        """Return circle name."""
        return self.name
    
    class Meta(CRideModel.Meta):
        """Meta class."""
        ordering = ['-rides_taken', '-rides_offered']

        ordering = ['-rides_taken', '-rides_offered']
