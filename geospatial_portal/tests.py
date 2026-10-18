from django.test import TestCase, Client
from django.urls import reverse
import json
from geospatial_portal.models import Profile, Metric, Service, Project, TimelineItem, MapNode

class GeospatialPortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.create(
            full_name="Muhammad Arshad Javed",
            current_role="Lead WebGIS Developer",
            email="test@example.com"
        )
        self.service = Service.objects.create(
            service_code="01 / WEBGIS",
            title="WebGIS Platforms",
            icon="🗺️",
            description="High throughput WMS/WFS",
            tags="OpenLayers, GeoServer",
            order=1
        )
        self.project = Project.objects.create(
            title="PCBDDA 3D GIS Metaverse",
            category="webgis_3d",
            category_label="WEBGIS & 3D",
            year="2024",
            tech_stack="Django · OpenLayers",
            order=1
        )
        self.map_node = MapNode.objects.create(
            name="PCBDDA 3D GIS Metaverse",
            description="Centralized Spatial Data Center",
            latitude=31.5204,
            longitude=74.3587,
            category="WebGIS & 3D",
            status="LIVE",
            city="Lahore",
            order=1
        )

    def test_index_page_status_code(self):
        response = self.client.get(reverse('geospatial_portal:index'))
        self.assertEqual(response.status_code, 200)

    def test_templates_used(self):
        response = self.client.get(reverse('geospatial_portal:index'))
        self.assertTemplateUsed(response, 'geospatial_portal/index.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'geospatial_portal/components/_map_console.html')

    def test_static_asset_references_in_html(self):
        response = self.client.get(reverse('geospatial_portal:index'))
        content = response.content.decode('utf-8')
        # Core theme assets
        self.assertIn('/static/css/theme.css', content)
        self.assertIn('/static/js/tailwind-config.js', content)
        self.assertIn('/static/js/main.js', content)
        # CesiumJS WebGL assets
        self.assertIn('cesium.com/downloads/cesiumjs/releases/1.120/Build/Cesium/Widgets/widgets.css', content)
        self.assertIn('cesium.com/downloads/cesiumjs/releases/1.120/Build/Cesium/Cesium.js', content)
        self.assertIn('/static/css/map-style.css', content)
        self.assertIn('/static/js/map-console.js', content)

    def test_map_console_markup(self):
        response = self.client.get(reverse('geospatial_portal:index'))
        content = response.content.decode('utf-8')
        self.assertIn('id="cesiumContainer"', content)
        self.assertIn('id="btn-toggle-dimension"', content)
        self.assertIn('id="map-search-input"', content)
        self.assertIn('id="cesium-popup-card"', content)

    def test_dynamic_content_rendered(self):
        response = self.client.get(reverse('geospatial_portal:index'))
        content = response.content.decode('utf-8')
        self.assertIn("Muhammad Arshad Javed", content)
        self.assertIn("PCBDDA 3D GIS Metaverse", content)
        self.assertIn("WebGIS Platforms", content)

    def test_api_nodes_endpoint(self):
        response = self.client.get(reverse('geospatial_portal:api_map_nodes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        first_node = data[0]
        self.assertEqual(first_node['name'], 'PCBDDA 3D GIS Metaverse')
        self.assertAlmostEqual(first_node['latitude'], 31.5204)
        self.assertAlmostEqual(first_node['longitude'], 74.3587)
        self.assertEqual(first_node['category'], 'WebGIS & 3D')
        self.assertEqual(first_node['status'], 'LIVE')
        self.assertEqual(first_node['city'], 'Lahore')
        self.assertIn('description', first_node)
