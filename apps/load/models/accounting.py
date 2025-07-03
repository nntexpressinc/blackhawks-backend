from django.db import models

class Accounting(models.Model):

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='accounting_records'
    )
    