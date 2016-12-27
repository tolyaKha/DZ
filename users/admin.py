from django.contrib import admin
from users.models import *

admin.site.register(User)
admin.site.register(Bet)
admin.site.register(Fight)
admin.site.register(Boxer)