from django.db import models

class Record(models.Model):
    user        = models.ForeignKey("users.User", on_delete=models.CASCADE)
    start_at    = models.DateTimeField(auto_now_add=True)
    end_at      = models.DateTimeField(auto_now=True)
    oneday_time = models.IntegerField(null=True)

    class Meta:
        db_table = "records"

class MessageType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "message_types"

    def __str__(self):
        return self.name

class Message(models.Model):
    message_type = models.ForeignKey("MessageType", on_delete=models.CASCADE)
    content      = models.CharField(max_length=50)

    class Meta:
        db_table = "messages"

    def __str__(self):
        return self.name