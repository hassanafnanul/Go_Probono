from django.db import models

class Law(models.Model):
    name = models.CharField(default='', max_length=101)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='law_thumbnail/')
    image_text = models.CharField(default='', max_length=101)
    order = models.IntegerField(default=0)
    slug = models.CharField(default='', max_length=101)
    description = models.TextField(default='')
    headline = models.CharField(default='', max_length=543)
    home_law = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


