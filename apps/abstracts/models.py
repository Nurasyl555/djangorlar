from django.utils import timezone
from django.db import models
from django.db.models import QuerySet, Manager


class AbstractBaseModel(models.Model):
    """
    Abstract base model with created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(Manager):
    """
    Custom manager for soft-deletable models.

    Provides methods to easily query for active or deleted objects.
    The default manager `objects` will show all items (including deleted),
    which is useful for the admin panel.
    """
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def active(self) -> QuerySet:
        return self.get_queryset().filter(deleted_at__isnull=True)

    def deleted(self) -> QuerySet:
        return self.get_queryset().filter(deleted_at__isnull=False)


class AbstractSoftDeletableModel(AbstractBaseModel):
    """
    Abstract model implementing soft-deletion via a `deleted_at` timestamp.
    """
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name="Deleted At",
    )

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft-delete: set deleted_at instead of removing the row."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        """Restore a soft-deleted object."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])

    def is_deleted(self) -> bool:
        return self.deleted_at is not None
    is_deleted.boolean = True
    is_deleted.short_description = "Deleted"