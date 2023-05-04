from django.db import models


class LawyerCategory(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    order = models.IntegerField(null=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

