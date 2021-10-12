from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(questions)
admin.site.register(myForm)
admin.site.register(choice)
admin.site.register(mcq)
admin.site.register(submission)
