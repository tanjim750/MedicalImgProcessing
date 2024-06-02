from django.db import models

# Create your models here.
class ProcessedImage(models.Model):
    input = models.FileField(upload_to="images")
    output = models.FileField(upload_to="images",null=True)