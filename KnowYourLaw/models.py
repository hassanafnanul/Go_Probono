from django.db import models
from LawManagement.models import Law

 
class KnowYourLaw(models.Model):
    law = models.ForeignKey(Law, on_delete=models.SET_NULL, null=True, blank=True)
    
    question = models.CharField(max_length=60)
    eng_answer = models.TextField(default="")
    ban_answer = models.TextField(default="")
    tags = models.CharField(max_length=60)
    rating = models.IntegerField(default=0)

    is_archived = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.law.name) + '->' + str(self.question)


