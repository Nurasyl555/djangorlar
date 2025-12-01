from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

# Custom manager to handle soft-deleted records
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

# Abstract model implementing soft delete
class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    objects = SoftDeleteManager()  # Default manager
    all_objects = models.Manager()  # Manager to access all records including soft-deleted

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    
    class Meta:
        abstract = True
    
class Course(SoftDeleteModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(SoftDeleteModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    indentation = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.pk and self.order == Decimal('0.00'):
            min_order = Lesson.objects.filter(course=self.course).aggregate(models.Min('order'))['order__min']
            if min_order is not None:
                self.order = min_order - Decimal('1.00')
            else:
                self.order = Decimal('0.00')
        
        if self.indentation > 5:
            self.indentation = 5
            
        super().save(*args, **kwargs)