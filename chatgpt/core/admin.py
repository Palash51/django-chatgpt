from django.contrib import admin

# Register your models here.
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  list_display = ['first_term', 'second_term']
