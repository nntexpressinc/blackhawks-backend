# from django.conf import settings
# from django.db import models
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey

# class AuditLog(models.Model):
#     ACTION_CHOICES = (
#         ('create', 'Create'),
#         ('update', 'Update'),
#         ('delete', 'Delete'),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='audit_logs'
#     )
#     action = models.CharField(max_length=20, choices=ACTION_CHOICES)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     timestamp = models.DateTimeField(auto_now_add=True)
#     details = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.email} - {self.action} - {self.content_type} - {self.timestamp}"