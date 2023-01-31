from django.db import models
from django.contrib.auth.models import User

class Scan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path_file = models.FileField(upload_to='files/', null=True)
    path_result = models.FileField(upload_to='ready_files/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


