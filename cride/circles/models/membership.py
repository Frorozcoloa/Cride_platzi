"""Membeship models."""


#Django
from django.db import models
from cride.circles.models import circles

#Utilites
from cride.utils.models import CRideModel

class Membreship(CRideModel):
    """ Membership model.
        A membership is the table that holds the relationship betweenn
        a user and circle.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile =  models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circles =  models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        'circle admin',
        default=False,
        help_text="Circle admins can update the circle's data and manage its members"
    )


    #Invitations
    used_invitations = models.PositiveIntegerField(default=0)
    remaninig_invitation =models.ForeignKey(
            "users.User", 
            null=True, 
            on_delete=models.SET_NULL,
            related_name="invited_by")

    
    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offerd = models.PositiveIntegerField(default=0)

    #status

    is_active = models.BooleanField(
        'activate status',
        default=True,
        help_text="Only activate users are allowed to interact in the circle"
    )

    def __str__(self):
        """Retun username and circle"""

        return f'@{self.user.username} at #{self.circle.slug_name}'