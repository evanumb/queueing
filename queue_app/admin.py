from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('day', 'number', 'status', 'created_at', 'called_at', 'served_at')
    list_filter = ('day', 'status')
    search_fields = ('number',)
