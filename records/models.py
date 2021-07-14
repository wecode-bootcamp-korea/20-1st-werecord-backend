from django.db import models

class Record(models.Model):
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    start_at       = models.DateTimeField(auto_now=False)
    end_at         = models.DateTimeField(auto_now=False, null=True)
    residence_time = models.IntegerField(null=True)

    class Meta:
        db_table = "records"

class DailyRecord(models.Model):
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE)
    date       = models.DateField()
    total_time = models.IntegerField()

    class Meta:
        db_table = "daily_records"

class Message(models.Model):
    content = models.CharField(max_length=500)

    class Meta:
        db_table = "messages"