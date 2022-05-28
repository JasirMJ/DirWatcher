from re import T
from django.db import models
# Create your models here.

# Model for watch directory
class DirectoryRecords(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'directory_records'
        verbose_name = 'Directory Record'
        verbose_name_plural = 'Directory Records'

    # def __str__(self):
    #     return self.name

# Models for monitoring a directory files
class DirFiles(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    record = models.ForeignKey(DirectoryRecords,on_delete=models.CASCADE,null=True,blank=True)