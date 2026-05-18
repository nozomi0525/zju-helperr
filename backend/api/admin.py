from django.contrib import admin
from .models import User, Task, Order, Review, Message, Report, Blacklist

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Message)
admin.site.register(Report)
admin.site.register(Blacklist)
