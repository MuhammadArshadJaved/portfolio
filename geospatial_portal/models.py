from django.db import models

class Profile(models.Model):
    full_name = models.CharField(max_length=150)
    title = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)
    badge_title = models.CharField(max_length=100)
    current_role = models.CharField(max_length=200)
    availability_badge = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100)
    headline = models.TextField()
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    github_url = models.URLField()
    cv_download_url = models.CharField(max_length=200)
    contact_cta_heading = models.CharField(max_length=255)
    contact_cta_text = models.TextField()

    class Meta:
        verbose_name = "Geospatial Profile"
        verbose_name_plural = "Geospatial Profiles"

    def __str__(self):
        return self.full_name


class Metric(models.Model):
    value = models.CharField(max_length=20)
    suffix = models.CharField(max_length=10, blank=True, default="+")
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


class Service(models.Model):
    service_code = models.CharField(max_length=50, help_text="e.g. 01 / WEBGIS PLATFORMS")
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=20, default="🗺️")
    description = models.TextField()
    tags = models.CharField(max_length=255, help_text="Comma-separated tags e.g. OpenLayers, GeoServer, PostGIS / Django")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return self.title


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('all', 'All Projects'),
        ('webgis_3d', 'WebGIS & 3D'),
        ('municipal', 'Utility & Municipal'),
        ('regional', 'Regional Planning'),
        ('remote_sensing', 'Remote Sensing & AI'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='webgis_3d')
    category_label = models.CharField(max_length=100, default='WEBGIS & 3D')
    year = models.CharField(max_length=50, default='2024')
    badges = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags e.g. UAV Orthomosaic, 360° Street View")
    card_info_title = models.CharField(max_length=200, blank=True)
    card_info_detail = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255, help_text="e.g. Django · OpenLayers · GeoServer")
    link_url = models.CharField(max_length=200, default="#map-section")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_badge_list(self):
        return [b.strip() for b in self.badges.split(',') if b.strip()]

    def __str__(self):
        return self.title


class TimelineItem(models.Model):
    period = models.CharField(max_length=50, help_text="e.g. 2022–Present")
    role = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    description = models.TextField()
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.period} - {self.role} ({self.organization})"


class MapNode(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    latitude = models.FloatField(default=31.5204)
    longitude = models.FloatField(default=74.3587)
    category = models.CharField(max_length=100, default="WebGIS & 3D")
    status = models.CharField(max_length=50, default="Active")
    city = models.CharField(max_length=100, blank=True, default="Lahore")
    region = models.CharField(max_length=50, blank=True, default="Punjab")
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.city or self.region})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'category': self.category,
            'status': self.status,
            'description': self.description,
            'city': self.city,
        }
