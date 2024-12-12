from django.db import models

class Word(models.Model):
    word = models.CharField(verbose_name="Word",max_length=255, unique=True, blank=False, null=False)
    translation = models.CharField(verbose_name="Translation",max_length=255, blank=False, null=False)
    
    def __str__(self):
        return f"{self.word} - {self.translation}"
# Create your models here.
