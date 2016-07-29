from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from discussion.models import Tag
from login.models import UserProfile
from UCP.functions import get_time_elapsed_string, get_file_size_string


# Create your models here.
class News(models.Model):
    """(News description)"""
    title = models.CharField(blank=True, max_length=100)
    description = HTMLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    posted_at = models.DateTimeField(blank=True, default=timezone.now)
        
    def time_elapsed(self):
        return get_time_elapsed_string(self.posted_at)
        
    def short_description(self):
        return self.description[:200]+ "..."
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title


class Event(models.Model):
    """(Event description)"""
    title = models.CharField(blank=True, max_length=100)
    description = HTMLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    posted_at = models.DateTimeField(blank=True, default=timezone.now)
    posted_by = models.ForeignKey(UserProfile,null =True)
        
    def time_elapsed(self):
        return get_time_elapsed_string(self.posted_at)
        
    def short_description(self):
        return self.description[:200]+ "..."
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title