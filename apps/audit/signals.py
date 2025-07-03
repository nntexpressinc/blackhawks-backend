# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.contrib.contenttypes.models import ContentType
# from apps.audit.models import AuditLog
# from django.conf import settings

# @receiver(post_save)
# def log_save(sender, instance, created, **kwargs):
#     if sender == settings.AUTH_USER_MODEL or not hasattr(instance, '_request'):
#         return

#     user = getattr(instance, '_request').user if hasattr(instance, '_request') else None
#     if user and user.is_authenticated:
#         action = 'create' if created else 'update'
#         AuditLog.objects.create(
#             user=user,
#             action=action,
#             content_type=ContentType.objects.get_for_model(sender),
#             object_id=instance.pk,
#             details=f"{action.capitalize()} {sender.__name__} with id {instance.pk}"
#         )

# @receiver(post_delete)
# def log_delete(sender, instance, **kwargs):
#     if sender == settings.AUTH_USER_MODEL or not hasattr(instance, '_request'):
#         return

#     user = getattr(instance, '_request').user if hasattr(instance, '_request') else None
#     if user and user.is_authenticated:
#         AuditLog.objects.create(
#             user=user,
#             action='delete',
#             content_type=ContentType.objects.get_for_model(sender),
#             object_id=instance.pk,
#             details=f"Deleted {sender.__name__} with id {instance.pk}"
#         )