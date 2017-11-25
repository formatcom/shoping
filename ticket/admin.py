from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('pk', 'total', 'status',)
    list_filter = ('status',)
    filter_horizontal = ('items',)
