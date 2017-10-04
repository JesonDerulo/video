from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
# Create your models here.
from courses.fields import PositionField
from courses.utils import create_slug
from django.db.models import Count
from videos.models import Video


class CategoryQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all(
        ).active().annotate(
            courses_length=Count('primary_category') + Count("secondary_category")
        ).prefetch_related('primary_category', 'secondary_category')

class Category(models.Model):
    title       = models.CharField(max_length=120)
    video       = models.ForeignKey(Video, null=True, blank=True)
    slug        = models.SlugField(blank=True)
    order       = PositionField(blank=True)
    description = models.TextField()
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)


    objects = CategoryManager()

    def get_absolute_url(self):
        return reverse("categories:detail", kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_category_receiver, sender=Category)
