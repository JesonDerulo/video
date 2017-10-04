from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from .utils import create_slug, make_display_price
from videos.models import Video
from .fields import PositionField
from django.db.models import Prefetch
from categories.models import Category
# Create your models here.
class MyCourses(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL)
    courses     = models.ManyToManyField('Course',related_name='owned', blank=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.courses.all().count())

    class Meta:
        verbose_name = "My Courses"
        verbose_name_plural = "My courses"
def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        MyCourses.object.get_or_create(user=instance)

post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)





POS_CHOICES = (
    ('main', 'Main'),
    ('sec','Secondary'),
)

class CourseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def owned(self, user):
        if user.is_authenticated:
            return self.prefetch_related(
                        Prefetch( 'owned',
                                  queryset=MyCourses.objects.filter(user=user),
                                  to_attr='is_owner',
                        )
                )
        return self

class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all().active()

def handle_upload(instance,filename):
    if instance.slug:
        return "%s/images/%s" %(instance.slug, filename)
    return "unknown/images/%s" %(filename)

class Course(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True)
    image           = models.ImageField(upload_to= handle_upload,
                                        height_field='image_height',
                                        width_field='image_width',
                                        blank=True, null=True,)
    image_height    = models.IntegerField(blank=True, null=True)
    image_width     = models.IntegerField(blank=True, null=True)
    description     = models.TextField()
    # category        = models.CharField(max_length=120, choices=POS_CHOICES, default='main')
    category        = models.ForeignKey(Category, related_name='primary_category', null=True, blank=True)
    secondary       = models.ManyToManyField(Category, related_name='secondary_category', blank=True)
    order           = PositionField(collection='category')
    price           = models.DecimalField(decimal_places=2, max_digits=100)
    active          = models.BooleanField(default=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = CourseManager()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    def get_purchase_url(self):
        return reverse("courses:purchase", kwargs={"slug":self.slug})

    def display_price(self):
        return make_display_price(self.price)




class Lecture(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    video           = models.ForeignKey(Video, on_delete=models.SET_NULL, null= True)
    title           = models.CharField(max_length=120)
    order           = PositionField(collection='course')
    slug            = models.SlugField(blank=True)
    description     = models.TextField(blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('slug', 'course'),)
        ordering = ['order', 'title']

    @property
    def display_order(self):
        return self.order + 1




    def get_absolute_url(self):
        return reverse("courses:lecture-detail",
                kwargs={
                    "cslug": self.course.slug,
                    "lslug": self.slug
                })




def pre_save_video_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_video_receiver, sender=Course)

