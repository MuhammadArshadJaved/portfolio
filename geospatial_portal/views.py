from django.shortcuts import render
from django.http import JsonResponse
from .models import Profile, Metric, Service, Project, TimelineItem, MapNode

def index(request):
    """
    Renders the dynamic geospatial portfolio landing page.
    Queries database models, falling back to rich structured default data if empty.
    """
    # Profile
    profile = Profile.objects.first()
    if not profile:
        profile = {
            'full_name': 'Muhammad Arshad Javed',
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

    # Metrics
    metrics_qs = Metric.objects.all()
    if metrics_qs.exists():
        metrics = metrics_qs
    else:
        metrics = [
            {'value': '8', 'suffix': '+', 'label': 'Years of Exp.'},
            {'value': '40', 'suffix': '+', 'label': 'Mission Projects'},
            {'value': '16', 'suffix': '+', 'label': 'Municipal Cities'},
            {'value': '30', 'suffix': 'Yrs', 'label': 'Satellite RS Data'},
        ]

    # Services
    services_qs = Service.objects.all()
    if services_qs.exists():
        services = services_qs
    else:
        services = [
            {
                'service_code': '01 / WEBGIS PLATFORMS',
                'title': 'WebGIS & Spatial Cloud Platforms',
                'icon': '🗺️',
                'description': 'Custom map portals with OpenLayers, Leaflet, MapLibre GL, Python-Django, GeoServer, and PostGIS handling high-throughput WMS, WFS, and WCS OGC pipelines.',
                'get_tag_list': ['OpenLayers', 'GeoServer', 'PostGIS / Django']
            },
            {
                'service_code': '02 / GEO-AI & SATELLITE',
                'title': 'GeoAI & Earth Observation',
                'icon': '🛰️',
                'description': 'Multi-temporal satellite monitoring (Google Earth Engine, Landsat, Sentinel-2), PySEBAL crop water modeling, NDVI classification, and 30+ year river morphology timelapses.',
                'get_tag_list': ['GEE', 'PySEBAL', 'Sentinel / Landsat']
            },
            {
                'service_code': '03 / UAV PHOTOGRAMMETRY & 3D',
                'title': 'Drone Photogrammetry & 3D GIS',
                'icon': '🚁',
                'description': 'High-precision UAV photogrammetry, Agisoft Metashape processing, DSM/DTM surface extraction, 3D architectural CAD/BIM integration, and QField mobile field validation.',
                'get_tag_list': ['UAV Surveys', 'Metashape / DSM', 'QField / CAD']
            },
        ]

    # Projects
    projects_qs = Project.objects.all()
    if projects_qs.exists():
        projects = projects_qs
    else:
        projects = [
            {
                'title': 'PCBDDA 3D GIS Metaverse & Spatial Data Center',
                'category': 'webgis_3d',
                'category_label': 'WEBGIS & 3D',
                'year': '2024',
                'get_badge_list': ['UAV Orthomosaic', '360° Street View'],
                'card_info_title': 'CBD Central Spatial Data Center',
                'card_info_detail': '3D BIM / CAD',
                'card_type': 'split',
                'description': 'Centralized Spatial Data Center integrating high-resolution drone orthomosaics, 360° street views, and 3D CAD/BIM models with temporal change detection.',
                'tech_stack': 'Django · OpenLayers · GeoServer',
                'link_url': '#map-section'
            },
            {
                'title': 'WASA Lahore Real-Time Monitoring Portal',
                'category': 'municipal',
                'category_label': 'MUNICIPAL WEBGIS',
                'year': '2023',
                'card_info_title': 'Hydraulic Pipe Invert Profiling',
                'card_info_detail': 'Flow: 24.6 m³/s · Slope 0.002',
                'card_type': 'indicator',
                'description': 'Executive web portal and field dashboard with interactive hydraulic profiling, attribute filtering, elevation profiling, and mobile ground-truth sync.',
                'tech_stack': 'Leaflet · PostGIS · Python · QField',
                'link_url': '#map-section'
            },
            {
                'title': 'LESCO Enterprise Management System (EMS)',
                'category': 'municipal',
                'category_label': 'UTILITY GIS',
                'year': '2023',
                'card_info_title': '132kV / 11kV Feeder Tracing',
                'card_info_detail': '218,000+ Poles',
                'card_info_extra': 'Automated High-Res PDF Cartographic Generator',
                'card_type': 'progress',
                'description': 'High-concurrency spatial platform for power utility grid tracing, pole/transformer indexing, consumer load mapping, and automated PDF map generator.',
                'tech_stack': 'ArcGIS Server · JS API · SQL Server',
                'link_url': '#map-section'
            },
            {
                'title': 'Khyber Pass Economic Corridor (KPEC)',
                'category': 'regional',
                'category_label': 'REGIONAL PLANNING',
                'year': 'WORLD BANK',
                'card_info_title': 'mcda_pipeline:',
                'card_info_detail': 'slope_wt(0.35) + proximity(0.40)',
                'card_type': 'code',
                'description': 'Automated Python geoprocessing pipelines for Multi-Criteria Decision Analysis (MCDA) siting industrial hubs, trade logistics corridors, and UAV surveys.',
                'tech_stack': 'Python · QGIS · QField · UAV',
                'link_url': '#map-section'
            },
            {
                'title': 'Land Use Reclassification & Master Plan',
                'category': 'regional',
                'category_label': 'URBAN MCDSS',
                'year': '2023',
                'card_info_title': 'Cadastral LOP Integration',
                'card_info_detail': '48+ Zones',
                'card_type': 'split',
                'description': 'Dynamic Multi-Criteria Decision Support System evaluating urban zoning scenarios with weighted accessibility criteria and cadastral LOP integration.',
                'tech_stack': 'Spatial MCDSS · PostGIS · Python',
                'link_url': '#map-section'
            },
            {
                'title': 'IDSS Satellite Remote Sensing (Irrigation Dept)',
                'category': 'remote_sensing',
                'category_label': 'EARTH OBSERVATION',
                'year': 'ADB',
                'card_info_title': 'PySEBAL Actual ET + Kriging Groundwater Map',
                'card_type': 'banner',
                'description': 'Multi-temporal NDVI crop classification, actual evapotranspiration modeling (PySEBAL), and groundwater table interpolation across canal commands.',
                'tech_stack': 'GEE · Landsat-8 · Sentinel-2',
                'link_url': '#map-section'
            },
        ]

    # Timeline Items
    timeline_qs = TimelineItem.objects.all()
    if timeline_qs.exists():
        timeline = timeline_qs
    else:
        timeline = [
            {
                'period': '2017–2018',
                'role': 'GIS Digitizer',
                'organization': 'PMDFC',
                'description': 'PMDFC · Municipal Asset Mapping, field GPS ground-truthing, and road cadastre digitalization.',
                'is_current': False
            },
            {
                'period': '2018–2019',
                'role': 'GIS Research Assistant',
                'organization': 'Irrigation Dept / ADB',
                'description': 'Irrigation Dept / ADB · Remote Sensing IDSS, multi-spectral satellite indices, and PySEBAL ET modeling.',
                'is_current': False
            },
            {
                'period': '2019–2021',
                'role': 'GIS Analyst & Developer',
                'organization': 'SMEC International',
                'description': 'SMEC International · NHA network-wide GIS integration, Salang Tunnel Afghanistan DEM, and flood schemes.',
                'is_current': False
            },
            {
                'period': '2021–2022',
                'role': 'Deputy Manager GIS',
                'organization': 'PMDFC / World Bank',
                'description': 'PMDFC / World Bank · Architected centralized municipal geodatabases across 16 Secondary Cities in Punjab.',
                'is_current': False
            },
            {
                'period': '2022–Present',
                'role': 'Senior GIS Analyst & Lead WebGIS',
                'organization': 'NESPAK',
                'description': 'NESPAK · Directing national spatial megaprojects, PCBDDA Metaverse, WASA, LESCO, and KPEC platforms.',
                'is_current': True
            },
        ]

    # Filter categories for projects
    project_categories = [
        {'id': 'all', 'label': 'All Projects (40+)'},
        {'id': 'webgis_3d', 'label': 'WebGIS & 3D'},
        {'id': 'municipal', 'label': 'Utility & Municipal'},
        {'id': 'regional', 'label': 'Regional Planning'},
        {'id': 'remote_sensing', 'label': 'Remote Sensing & AI'},
    ]

    context = {
        'profile': profile,
        'metrics': metrics,
        'services': services,
        'projects': projects,
        'timeline': timeline,
        'project_categories': project_categories,
    }

    return render(request, 'geospatial_portal/index.html', context)


def api_map_nodes(request):
    """
    Returns all project and map nodes as a clean JSON array for CesiumJS.
    Attributes include name, latitude, longitude, category, status, description, and city.
    """
    nodes = MapNode.objects.all().order_by('order', 'name')
    if nodes.exists():
        data = [node.to_dict() for node in nodes]
    else:
        data = [
            {
                "id": 1,
                "name": "PCBDDA 3D GIS Metaverse",
                "description": "Centralized Spatial Data Center integrating high-resolution drone orthomosaics, 360° street views, and 3D CAD/BIM models with temporal change detection.",
                "latitude": 31.5204,
                "longitude": 74.3587,
                "category": "WebGIS & 3D",
                "status": "LIVE",
                "city": "Lahore"
            },
            {
                "id": 2,
                "name": "Lyari Transformation Project (LTP)",
                "description": "Multi-sector urban infrastructure mapping, stormwater drainage modeling, and road network rehabilitation tracking across Karachi's dense Lyari district.",
                "latitude": 24.8607,
                "longitude": 67.0011,
                "category": "Utility & Municipal",
                "status": "Operational",
                "city": "Karachi"
            },
            {
                "id": 3,
                "name": "KPEC Economic Corridor Logistics",
                "description": "World Bank-funded spatial decision support system for the Khyber Pass Economic Corridor, integrating MCDA site suitability and trade route telematics.",
                "latitude": 34.0151,
                "longitude": 71.5249,
                "category": "Regional Planning",
                "status": "In Progress",
                "city": "Peshawar"
            },
            {
                "id": 4,
                "name": "PMDFC 16 Cities Enterprise GIS",
                "description": "Centralized municipal spatial database infrastructure connecting 16 secondary cities in Punjab for water utility, tax cadastre, and asset management.",
                "latitude": 31.4504,
                "longitude": 73.1350,
                "category": "Enterprise Geodatabase",
                "status": "Production",
                "city": "Faisalabad"
            },
            {
                "id": 5,
                "name": "WASA Lahore Real-Time Monitoring Portal",
                "description": "Executive web portal and field dashboard with interactive hydraulic profiling, attribute filtering, elevation profiling, and mobile ground-truth sync.",
                "latitude": 31.5820,
                "longitude": 74.3294,
                "category": "Utility & Municipal",
                "status": "Active",
                "city": "Lahore"
            },
            {
                "id": 6,
                "name": "IDSS Satellite Remote Sensing (Irrigation)",
                "description": "Multi-temporal NDVI crop classification, actual evapotranspiration modeling (PySEBAL), and groundwater table interpolation across canal commands.",
                "latitude": 30.1575,
                "longitude": 71.5249,
                "category": "Earth Observation",
                "status": "Completed",
                "city": "Multan"
            }
        ]
    return JsonResponse(data, safe=False)
