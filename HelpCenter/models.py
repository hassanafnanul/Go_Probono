from django.db import models

class HelpCenter(models.Model):
    thumbnail = models.ImageField(null=True, blank=True, upload_to='help_line_rules/')
    image_text = models.CharField(default='', max_length=101)
    helpline = models.CharField(default='', max_length=101)
    rules = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
