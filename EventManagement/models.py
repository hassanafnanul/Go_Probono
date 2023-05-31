from django.db import models

class Event(models.Model):
    name = models.CharField(default='', max_length=101)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='event_thumbnail/')
    image_text = models.CharField(default='', max_length=101)
    order = models.IntegerField(default=0)
    slug = models.CharField(default='', max_length=101)
    description = models.TextField(default='')
    brief_description = models.CharField(default='', max_length=543)
    location = models.CharField(max_length=255)
    start_time = models.DateField()
    end_time = models.DateField()
    organizer = models.CharField(max_length=255)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

# name, thumbnail, image_text, order, slug, description, brief_description, location, start_time, end_time, organizer, is_archived, created_at

