from django.db import models



SLIDER_TYPES = [
    ('Regular', 'Regular')
]

class Slider(models.Model):
    title = models.CharField(default='',max_length=100)
    image = models.FileField(null=True, blank=True, upload_to='slider/')
    mobile_image = models.FileField(null=True, blank=True, upload_to='slider/')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    button_url = models.CharField(default='',max_length=500)
    button_text = models.CharField(default='',max_length=55)
    slider_text = models.CharField(default='',max_length=500)
    order = models.IntegerField(default=0)    
    slider_type = models.CharField(choices=SLIDER_TYPES, max_length=100, default=SLIDER_TYPES[0][1])
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return 'Slider:'+str(self.id)+self.title

