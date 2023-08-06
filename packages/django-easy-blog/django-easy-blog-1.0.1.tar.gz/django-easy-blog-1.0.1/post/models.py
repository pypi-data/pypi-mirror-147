from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = RichTextUploadingField(null=False, blank=False)
    thumbnail = models.ImageField(upload_to='post/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, )
    updated_date = models.DateTimeField(auto_now=True)
    keywords = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=158, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.meta_description = self.content[:155] + "..."
        return super().save(*args, **kwargs)
