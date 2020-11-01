""" Users admin"""

# Django
from django.contrib import admin

# Models
from users.models  import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin"""

    list_display = (
        'user',
        'phone_number',
    )
    list_filter =(
        'user',
    )
