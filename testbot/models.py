from django.db import models

# Create your models here.

class Testbot(models.Model):
    pass
    text_id = models.AutoField(primary_key=True)
    is_bot = models.IntegerField()
    text = models.CharField(max_length=200,null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)