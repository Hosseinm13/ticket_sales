from django.contrib import admin
from .models import Concert, Ticket

admin.site.register(Concert)
admin.site.register(Ticket)