from django.core.management.base import BaseCommand
from geospatial_portal.models import Profile, Metric, Service, Project, TimelineItem, MapNode

class Command(BaseCommand):
    help = "Populate the database with initial portfolio data from Stitch design export"

    def handle(self, *args, **options):
        self.stdout.write("Seeding portfolio data...")

        # Profile
        profile, created = Profile.objects.get_or_create(
            full_name="Muhammad Arshad Javed",
            defaults={
            'initials': 'Portfolio',
            'badge_title': 'Lead Full-Stack App Developer',
            'current_role': 'Senior GIS Analyst · Lead Full-Stack App Developer at NESPAK',
            'availability_badge': 'Executive Consulting',
            'location': 'Lahore, Pakistan',
            'affiliation': 'NESPAK Lead',
            'headline': 'Crafting enterprise spatial intelligence, WebGIS platforms & resilient spatial data infrastructure.',
            'bio': 'Senior GIS Analyst & Lead WebGIS Developer at NESPAK. Specializing in high-performance cloud & on-premise spatial platforms, OGC web services, GeoAI, UAV photogrammetry, and  remote sensing monitoring.',
            'email': 'iarshadjaved04@gmail.com',
            'phone': '+92 310 0856544',
            'github_url': 'https://github.com/MuhammadArshadJaved',
            'cv_download_url': '#contact',
            'contact_cta_heading': 'Need enterprise spatial data architecture, WebGIS solutions, or GeoAI models?',
            'contact_cta_text': 'Available for enterprise WebGIS engineering, spatial cloud migrations (PostGIS/GeoServer), UAV photogrammetric pipelines, and geospatial advisory.',
        }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  Created Profile"))

        # Metrics
        metrics_data = [
            {"value": "8", "suffix": "+", "label": "Years of Exp.", "order": 1},
            {"value": "40", "suffix": "+", "label": "Mission Projects", "order": 2},
            {"value": "16", "suffix": "+", "label": "Municipal Cities", "order": 3},
            {"value": "30", "suffix": "Yrs", "label": "Satellite RS Data", "order": 4},
        ]
        for m in metrics_data:
            Metric.objects.get_or_create(label=m["label"], defaults=m)
        self.stdout.write(self.style.SUCCESS("  Metrics configured"))

        # Services
        services_data = [
            {
                "service_code": "01 / WEBGIS PLATFORMS",
                "title": "WebGIS & Spatial Cloud Platforms",
                "icon": "🗺️",
                "description": "Custom map portals with OpenLayers, Leaflet, MapLibre GL, Python-Django, GeoServer, and PostGIS handling high-throughput WMS, WFS, and WCS OGC pipelines.",
                "tags": "OpenLayers, GeoServer, PostGIS / Django",
                "order": 1
            },
            {
                "service_code": "02 / GEO-AI & SATELLITE",
                "title": "GeoAI & Earth Observation",
                "icon": "🛰️",
                "description": "Multi-temporal satellite monitoring (Google Earth Engine, Landsat, Sentinel-2), PySEBAL crop water modeling, NDVI classification, and 30+ year river morphology timelapses.",
                "tags": "GEE, PySEBAL, Sentinel / Landsat",
                "order": 2
            },
            {
                "service_code": "03 / UAV PHOTOGRAMMETRY & 3D",
                "title": "Drone Photogrammetry & 3D GIS",
                "icon": "🚁",
                "description": "High-precision UAV photogrammetry, Agisoft Metashape processing, DSM/DTM surface extraction, 3D architectural CAD/BIM integration, and QField mobile field validation.",
                "tags": "UAV Surveys, Metashape / DSM, QField / CAD",
                "order": 3
            },
        ]
        for s in services_data:
            Service.objects.get_or_create(service_code=s["service_code"], defaults=s)
        self.stdout.write(self.style.SUCCESS("  Services configured"))

        # Projects
        projects_data = [
            {
                "title": "PCBDDA 3D GIS Metaverse & Spatial Data Center",
                "category": "webgis_3d",
                "category_label": "WEBGIS & 3D",
                "year": "2024",
                "badges": "UAV Orthomosaic, 360° Street View",
                "card_info_title": "CBD Central Spatial Data Center",
                "card_info_detail": "3D BIM / CAD",
                "description": "Centralized Spatial Data Center integrating high-resolution drone orthomosaics, 360° street views, and 3D CAD/BIM models with temporal change detection.",
                "tech_stack": "Django · OpenLayers · GeoServer",
                "link_url": "#map-section",
                "order": 1
            },
            {
                "title": "WASA Lahore Real-Time Monitoring Portal",
                "category": "municipal",
                "category_label": "MUNICIPAL WEBGIS",
                "year": "2023",
                "badges": "",
                "card_info_title": "Hydraulic Pipe Invert Profiling",
                "card_info_detail": "Flow: 24.6 m³/s · Slope 0.002",
                "description": "Executive web portal and field dashboard with interactive hydraulic profiling, attribute filtering, elevation profiling, and mobile ground-truth sync.",
                "tech_stack": "Leaflet · PostGIS · Python · QField",
                "link_url": "#map-section",
                "order": 2
            },
            {
                "title": "LESCO Enterprise Management System (EMS)",
                "category": "municipal",
                "category_label": "UTILITY GIS",
                "year": "2023",
                "badges": "",
                "card_info_title": "132kV / 11kV Feeder Tracing",
                "card_info_detail": "218,000+ Poles",
                "description": "High-concurrency spatial platform for power utility grid tracing, pole/transformer indexing, consumer load mapping, and automated PDF map generator.",
                "tech_stack": "ArcGIS Server · JS API · SQL Server",
                "link_url": "#map-section",
                "order": 3
            },
            {
                "title": "Khyber Pass Economic Corridor (KPEC)",
                "category": "regional",
                "category_label": "REGIONAL PLANNING",
                "year": "WORLD BANK",
                "badges": "",
                "card_info_title": "mcda_pipeline:",
                "card_info_detail": "slope_wt(0.35) + proximity(0.40)",
                "description": "Automated Python geoprocessing pipelines for Multi-Criteria Decision Analysis (MCDA) siting industrial hubs, trade logistics corridors, and UAV surveys.",
                "tech_stack": "Python · QGIS · QField · UAV",
                "link_url": "#map-section",
                "order": 4
            },
            {
                "title": "Land Use Reclassification & Master Plan",
                "category": "regional",
                "category_label": "URBAN MCDSS",
                "year": "2023",
                "badges": "",
                "card_info_title": "Cadastral LOP Integration",
                "card_info_detail": "48+ Zones",
                "description": "Dynamic Multi-Criteria Decision Support System evaluating urban zoning scenarios with weighted accessibility criteria and cadastral LOP integration.",
                "tech_stack": "Spatial MCDSS · PostGIS · Python",
                "link_url": "#map-section",
                "order": 5
            },
            {
                "title": "IDSS Satellite Remote Sensing (Irrigation Dept)",
                "category": "remote_sensing",
                "category_label": "EARTH OBSERVATION",
                "year": "ADB",
                "badges": "",
                "card_info_title": "PySEBAL Actual ET + Kriging Groundwater Map",
                "card_info_detail": "",
                "description": "Multi-temporal NDVI crop classification, actual evapotranspiration modeling (PySEBAL), and groundwater table interpolation across canal commands.",
                "tech_stack": "GEE · Landsat-8 · Sentinel-2",
                "link_url": "#map-section",
                "order": 6
            },
        ]
        for p in projects_data:
            Project.objects.get_or_create(title=p["title"], defaults=p)
        self.stdout.write(self.style.SUCCESS("  Projects configured"))

        # Timeline
        timeline_data = [
            {
                "period": "2017–2018",
                "role": "GIS Digitizer & Surveyor",
                "organization": "PMDFC",
                "description": "PMDFC · Municipal Asset Mapping, field GPS ground-truthing, and road cadastre digitalization.",
                "is_current": False,
                "order": 1
            },
            {
                "period": "2018–2019",
                "role": "GIS Research Assistant",
                "organization": "Irrigation Dept / ADB",
                "description": "Irrigation Dept / ADB · Remote Sensing IDSS, multi-spectral satellite indices, and PySEBAL ET modeling.",
                "is_current": False,
                "order": 2
            },
            {
                "period": "2019–2021",
                "role": "GIS Analyst & Developer",
                "organization": "SMEC International",
                "description": "SMEC International · NHA network-wide GIS integration, Salang Tunnel Afghanistan DEM, and flood schemes.",
                "is_current": False,
                "order": 3
            },
            {
                "period": "2021–2022",
                "role": "Deputy Manager GIS",
                "organization": "PMDFC / World Bank",
                "description": "PMDFC / World Bank · Architected centralized municipal geodatabases across 16 Secondary Cities in Punjab.",
                "is_current": False,
                "order": 4
            },
            {
                "period": "2022–Present",
                "role": "Senior GIS Analyst & Lead WebGIS",
                "organization": "NESPAK",
                "description": "NESPAK · Directing national spatial megaprojects, PCBDDA Metaverse, WASA, LESCO, and KPEC platforms.",
                "is_current": True,
                "order": 5
            },
        ]
        for t in timeline_data:
            TimelineItem.objects.get_or_create(period=t["period"], defaults=t)
        self.stdout.write(self.style.SUCCESS("  Timeline configured"))

        # Map Nodes
        MapNode.objects.all().delete()
        nodes_data = [
            {
                "name": "PCBDDA 3D GIS Metaverse",
                "description": "Centralized Spatial Data Center integrating high-resolution drone orthomosaics, 360° street views, and 3D CAD/BIM models with temporal change detection.",
                "latitude": 31.5204,
                "longitude": 74.3587,
                "category": "WebGIS & 3D",
                "status": "LIVE",
                "city": "Lahore",
                "region": "Punjab",
                "is_primary": True,
                "order": 1
            },
            {
                "name": "Lyari Transformation Project (LTP)",
                "description": "Multi-sector urban infrastructure mapping, stormwater drainage modeling, and road network rehabilitation tracking across Karachi's dense Lyari district.",
                "latitude": 24.8607,
                "longitude": 67.0011,
                "category": "Utility & Municipal",
                "status": "Operational",
                "city": "Karachi",
                "region": "Karachi",
                "is_primary": False,
                "order": 2
            },
            {
                "name": "KPEC Economic Corridor Logistics",
                "description": "World Bank-funded spatial decision support system for the Khyber Pass Economic Corridor, integrating MCDA site suitability and trade route telematics.",
                "latitude": 34.0151,
                "longitude": 71.5249,
                "category": "Regional Planning",
                "status": "In Progress",
                "city": "Peshawar",
                "region": "KPK",
                "is_primary": False,
                "order": 3
            },
            {
                "name": "PMDFC 16 Cities Enterprise GIS",
                "description": "Centralized municipal spatial database infrastructure connecting 16 secondary cities in Punjab for water utility, tax cadastre, and asset management.",
                "latitude": 31.4504,
                "longitude": 73.1350,
                "category": "Enterprise Geodatabase",
                "status": "Production",
                "city": "Faisalabad",
                "region": "Punjab",
                "is_primary": False,
                "order": 4
            },
            {
                "name": "WASA Lahore Real-Time Monitoring Portal",
                "description": "Executive web portal and field dashboard with interactive hydraulic profiling, attribute filtering, elevation profiling, and mobile ground-truth sync.",
                "latitude": 31.5820,
                "longitude": 74.3294,
                "category": "Utility & Municipal",
                "status": "Active",
                "city": "Lahore",
                "region": "Punjab",
                "is_primary": False,
                "order": 5
            },
            {
                "name": "IDSS Satellite Remote Sensing (Irrigation)",
                "description": "Multi-temporal NDVI crop classification, actual evapotranspiration modeling (PySEBAL), and groundwater table interpolation across canal commands.",
                "latitude": 30.1575,
                "longitude": 71.5249,
                "category": "Earth Observation",
                "status": "Completed",
                "city": "Multan",
                "region": "Punjab",
                "is_primary": False,
                "order": 6
            },
        ]
        for node in nodes_data:
            MapNode.objects.create(**node)
        self.stdout.write(self.style.SUCCESS("  Map nodes configured"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded all portfolio data!"))

