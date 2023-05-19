from django.db import models

# Create your models here.
class account(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32, null=True)
    pass_fail_num=models.IntegerField(default=0)
    lock=models.BooleanField(default=False)
    unlock_time=models.DateTimeField(null=True)

    # date = models.DateField()
    # num = models.IntegerField(null=True)
    # file = models.CharField(max_length=30)
    # commit = models.TextField(max_length=200)
    # important = models.CharField(max_length=30, blank=True)
    # complete = models.BooleanField(default=False)
    # file_path = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = "account"