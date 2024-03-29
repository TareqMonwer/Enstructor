import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .fields import OrderField
from .utils import generate_custom_course_banner


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    @staticmethod
    def ordered_active_subjects():
        return Subject.objects.annotate(
            count=Count('courses')
        ).filter(count__gt=0).order_by("-count")


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    banner = models.ImageField(upload_to='courses/banners/',
        blank=True, null=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # save the object first
        super().save(*args, **kwargs)
        
        if not self.banner:
            banner_location = generate_custom_course_banner(self.title)

            with open(banner_location, mode='rb') as f:
                img = f.read()
            
            img_name = os.path.basename(banner_location.split('/')[-1])
            self.banner.save(
                img_name,
                ContentFile(img)
            )
            print(self.banner)
            self.save()


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')}
                                     )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    content = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
