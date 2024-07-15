from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Assignment
import os

@receiver(post_delete, sender=Assignment)
def delete_assignment_file(sender, instance, **kwargs):
    if instance.file_assignment:
        if os.path.isfile(instance.file_assignment.path):
            os.remove(instance.file_assignment.path)
