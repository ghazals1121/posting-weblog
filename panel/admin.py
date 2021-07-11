from django.contrib import admin

# Register your models here.
from panel.models import *

admin.site.register(MyUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
