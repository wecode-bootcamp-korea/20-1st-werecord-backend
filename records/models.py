from django.db import models

class Record(models.Model):
    user        = models.ForeignKey("users.User", on_delete=models.CASCADE)
    start_at    = models.DateTimeField(auto_now=False)
    end_at      = models.DateTimeField(auto_now=False, null=True)
    oneday_time = models.IntegerField(null=True)

    class Meta:
        db_table = "records"

class Message(models.Model):
    content = models.CharField(max_length=500)

    class Meta:
        db_table = "messages"

    def __str__(self):
        return self.name