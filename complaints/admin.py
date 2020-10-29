""" Complaint admin"""

# Django
from django.contrib import admin

# Models
from complaints.models import Complaint

@admin.register(Complaint)
class  ComplaintAdmin(admin.ModelAdmin):
    """ Complaint model Admin"""

    list_display = (
        'user',
        'station',
        'description',
        'link_evidence',
        'type_complaint',
        'date',
        'actual_price',
        'offered_price',
    )

    list_filter = (
        'user',
        'station',
        'type_complaint',
        'date',
    )