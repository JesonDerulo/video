from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text  import slugify

from courses.utils import create_slug
# Create your models here.


class Video(models.Model):
    title      = models.CharField(max_length=120)
    embed_code = models.TextField()
    slug       = models.SlugField(blank=True)
    free       = models.BooleanField(default=True)
    member_required = models.BooleanField(default=False)
    updated    = models.DateTimeField(auto_now=True)
    timestamp  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "/videos/{slug_arg}/".format(slug_arg=self.slug)
        return reverse("videos:detail", kwargs={"slug": self.slug})


def pre_save_video_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_video_receiver, sender=Video)