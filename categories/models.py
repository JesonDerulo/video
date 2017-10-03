from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
# Create your models here.
from courses.fields import PositionField
from courses.utils import create_slug

class CategoryQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all().active()

class Category(models.Model):
    title       = models.CharField(max_length=120)
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
