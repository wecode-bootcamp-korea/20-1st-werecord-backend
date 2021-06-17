from django.contrib import admin
from users.models import User, Batch

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Batch)
class UserBatch(admin.ModelAdmin):
    pass