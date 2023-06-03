from django.db import models
from django.contrib.auth.models import User

class Competition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    def __str__(self):
        return self.title + "\n" + self.description
    
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    project_desc = models.TextField(default="no")
    video = models.FileField(blank=True, null=True)
    




# Create your models here.
