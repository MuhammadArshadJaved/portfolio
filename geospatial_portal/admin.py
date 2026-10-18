from django.contrib import admin
from .models import Profile, Metric, Service, Project, TimelineItem, MapNode

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'current_role', 'location', 'email', 'phone')

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('value', 'suffix', 'label', 'order')
    list_editable = ('order',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_code', 'title', 'icon', 'order')
    list_editable = ('order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'tech_stack', 'order')
    list_filter = ('category', 'year')
    search_fields = ('title', 'description', 'tech_stack')
    list_editable = ('order',)

@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ('period', 'role', 'organization', 'is_current', 'order')
    list_editable = ('order',)

@admin.register(MapNode)
class MapNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'category', 'status', 'latitude', 'longitude', 'is_primary', 'order')
    list_filter = ('category', 'status', 'region', 'city')
    search_fields = ('name', 'description', 'city', 'region')
    list_editable = ('order', 'status')
