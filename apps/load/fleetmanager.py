from django.db import models

class FleetManager(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='fleet_manager_records'
    )

    