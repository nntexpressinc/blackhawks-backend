from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255)
    dispatchers = models.ManyToManyField('Dispatcher', related_name='dispatchers', blank=True)
    unit_id = models.ManyToManyField('Unit', related_name='unit_id', blank=True)
    telegram_token = models.CharField(max_length=255, blank=True, null=True)
    telegram_channel_id = models.CharField(max_length=255, blank=True, null=True)
    telegram_group_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name