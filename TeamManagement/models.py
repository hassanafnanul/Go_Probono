from django.db import models

class TeamMember(models.Model):
    name = models.CharField(default='', max_length=101)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='law_thumbnail/')
    image_text = models.CharField(default='', max_length=101)
    order = models.IntegerField(default=0)
    slug = models.CharField(default='', max_length=101)
    description = models.TextField(default='')
    designation = models.CharField(default='', max_length=543)
    portfolio_url = models.CharField(default='',max_length=250)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


