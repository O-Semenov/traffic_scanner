from django.db import models
from django.contrib.auth.models import User


class Scan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path_file = models.FileField(upload_to='files/', null=True)
    path_result = models.FileField(upload_to='ready_files/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    request = models.CharField(max_length=15, default='-')

    def getById(self, scanId):
        return Scan.objects.filter(id=scanId)

    def getByUser(self, userId):
        return Scan.objects.filter(user=userId)

    def updateScan(self, scanId, status=0, request='', file=''):
        Scan.objects.filter(id=scanId).update(status=status, path_result=file, request=request)
    def __str__(self):
        return self.id
