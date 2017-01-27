from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    MAX_LENGTH = 128
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if (self.views < 0):
            self.views = 0
        if (self.likes < 0):
            self.likes = 0
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name


class Page(models.Model):
    MAX_LENGTH = 128
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title

