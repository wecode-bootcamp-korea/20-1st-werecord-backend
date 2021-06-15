from django.db import models

class User(models.Model):
    google_login_id   = models.CharField(max_length=250, unique=True)
    email             = models.EmailField(max_length=250)
    profile_image_url = models.URLField(max_length=2000)
    name              = models.CharField(max_length=50)
    user_type         = models.ForeignKey("UserType", on_delete=models.CASCADE)
    batch             = models.ForeignKey("Batch", on_delete=models.CASCADE, null=True)
    position          = models.ForeignKey("Position", on_delete=models.CASCADE, null=True)
    blog              = models.CharField(max_length=500, null=True)
    github            = models.CharField(max_length=500, null=True)
    birthday          = models.DateField(null=True)
    total_time        = models.IntegerField(default=0)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name

class UserType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "user_types"

    def __str__(self):
        return self.name

class Batch(models.Model):
    name      = models.IntegerField()
    start_day = models.DateField()
    end_day   = models.DateField()

    class Meta:
        db_table = "batches"

    # def __str__(self):
    #     return self.name

class Position(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "positions"

    def __str__(self):
        return self.name
    