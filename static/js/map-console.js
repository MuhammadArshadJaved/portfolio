/**
 * ==========================================================================
 * Geospatial Portal - CesiumJS Interactive Cartographic Console (map-console.js)
 * High-Performance WebGL 3D/2D Engine, Dynamic REST Node Integration,
 * Multi-Dimensional Morphing, Entity Picking & Client-Side Search Flight Animation
 * ==========================================================================
 */

let viewer = null;
let cachedNodes = [];
let nodeEntities = [];
let corridorEntities = [];
let is3D = true;
let activeNode = null;

document.addEventListener('DOMContentLoaded', () => {
  // Wait until Cesium library is loaded
  if (typeof Cesium === 'undefined') {
    console.error('CesiumJS library is not loaded. Please verify the CDN link.');
    return;
  }

  initCesiumViewer();
  initMapControls();
  fetchAndRenderNodes();
});

/**
 * Helper to generate crisp, high-DPI custom canvas pins with glowing radar rings
 */
function createPinIconCanvas(color = '#059669', isPrimary = false) {
  const canvas = document.createElement('canvas');
  canvas.width = 56;
  canvas.height = 56;
  const ctx = canvas.getContext('2d');

  // Outer ambient pulsing aura
  ctx.beginPath();
  ctx.arc(28, 24, isPrimary ? 22 : 18, 0, 2 * Math.PI);
  ctx.fillStyle = isPrimary ? 'rgba(16, 185, 129, 0.35)' : 'rgba(5, 150, 105, 0.22)';
  ctx.fill();

  // Thin outer radar ring
  ctx.beginPath();
  ctx.arc(28, 24, isPrimary ? 17 : 14, 0, 2 * Math.PI);
  ctx.strokeStyle = isPrimary ? '#34D399' : 'rgba(16, 185, 129, 0.7)';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // Pin circle body
  ctx.beginPath();
  ctx.arc(28, 24, 11, 0, 2 * Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = '#FFFFFF';
  ctx.stroke();

  // Pointer tip
  ctx.beginPath();
  ctx.moveTo(21, 30);
  ctx.lineTo(28, 46);
  ctx.lineTo(35, 30);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();

  // Inner center dot
  ctx.beginPath();
  ctx.arc(28, 24, 4, 0, 2 * Math.PI);
  ctx.fillStyle = '#FFFFFF';
  ctx.fill();

  return canvas;
}

/**
 * Initialize Cesium Viewer
 */
function initCesiumViewer() {
  const container = document.getElementById('cesiumContainer');
  if (!container) return;

  try {
    // Clean OpenStreetMap tiles (free, zero API key required, zero watermark)
    let baseLayer = null;
    try {
      baseLayer = new Cesium.ImageryLayer(
        new Cesium.OpenStreetMapImageryProvider({
          url: 'https://tile.openstreetmap.org/'
        })
      );
    } catch (e) {
      console.warn('Fallback default base layer:', e);
    }

    viewer = new Cesium.Viewer('cesiumContainer', {
      animation: false,
      baseLayerPicker: false,
      fullscreenButton: true,
      geocoder: false,
      homeButton: false,
      infoBox: false,
      sceneModePicker: false,
      selectionIndicator: false,
      timeline: false,
      navigationHelpButton: false,
      baseLayer: baseLayer,
      shouldAnimate: true
    });

    // Dark cosmos styling
    if (viewer.scene.skyBox) viewer.scene.skyBox.show = false;
    viewer.scene.backgroundColor = Cesium.Color.fromCssColorString('#0b0c10');
    if (viewer.scene.globe) {
      viewer.scene.globe.baseColor = Cesium.Color.fromCssColorString('#111317');
      viewer.scene.globe.depthTestAgainstTerrain = false;
    }

    // Set initial camera view centered over Pakistan
    viewer.camera.setView({
      destination: Cesium.Cartesian3.fromDegrees(69.8, 30.2, 2200000.0),
      orientation: {
        heading: Cesium.Math.toRadians(0.0),
        pitch: Cesium.Math.toRadians(-72.0),
        roll: 0.0
      }
    });

    // Bind interactive picking event
    setupEntityPicking();
    setupCoordinateHUD();

  } catch (error) {
    console.error('Failed to initialize Cesium Viewer:', error);
  }
}

/**
 * Live HUD Coordinates Tracking
 */
function setupCoordinateHUD() {
  const hudCoords = document.getElementById('hud-coordinates');
  if (!hudCoords || !viewer) return;

  viewer.camera.changed.addEventListener(() => {
    try {
      const carto = viewer.scene.globe.ellipsoid.cartesianToCartographic(viewer.camera.position);
      if (carto) {
        const lat = Cesium.Math.toDegrees(carto.latitude);
        const lon = Cesium.Math.toDegrees(carto.longitude);
        const heightKm = Math.round(carto.height / 1000);
        hudCoords.textContent = `${lat >= 0 ? '+' : ''}${lat.toFixed(2)}° N / ${lon.toFixed(2)}° E · ${heightKm}km`;
      }
    } catch (e) {
      // Ignore coordinate transform hiccups during scene morph
    }
  });
}

/**
 * Fetch and plot project nodes from Django JSON API
 */
async function fetchAndRenderNodes() {
  try {
    const response = await fetch('/api/nodes/');
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
    const data = await response.json();
    cachedNodes = data;

    plotNodes(data);
    drawNetworkCorridors(data);
  } catch (error) {
    console.error('Error fetching map nodes from /api/nodes/:', error);
  }
}

/**
 * Plot nodes as 3D billboard and label entities
 */
function plotNodes(nodes) {
  if (!viewer) return;

  // Clear existing node entities
  nodeEntities.forEach(ent => viewer.entities.remove(ent));
  nodeEntities = [];

  nodes.forEach((node, index) => {
    const isPrimary = node.is_primary || (node.status === 'LIVE');
    const pinColor = isPrimary ? '#059669' : '#047857';
    const pinCanvas = createPinIconCanvas(pinColor, isPrimary);

    const entity = viewer.entities.add({
      id: `map-node-${node.id || index}`,
      name: node.name,
      position: Cesium.Cartesian3.fromDegrees(node.longitude, node.latitude, 50.0),
      billboard: {
        image: pinCanvas,
        verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
        scale: 1.0,
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      },
      label: {
        text: node.name,
        font: '11px JetBrains Mono, monospace',
        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        fillColor: Cesium.Color.fromCssColorString('#F8FAFC'),
        outlineColor: Cesium.Color.fromCssColorString('#0B0C10'),
        outlineWidth: 3.5,
        verticalOrigin: Cesium.VerticalOrigin.TOP,
        pixelOffset: new Cesium.Cartesian2(0, 8),
        disableDepthTestDistance: Number.POSITIVE_INFINITY,
        distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0.0, 1900000.0)
      },
      properties: {
        nodeData: node
      }
    });

    nodeEntities.push(entity);
  });
}

/**
 * Draw Geodesic Network Corridors between Hubs
 */
function drawNetworkCorridors(nodes) {
  if (!viewer || nodes.length < 2) return;

  corridorEntities.forEach(e => viewer.entities.remove(e));
  corridorEntities = [];

  const lahoreHub = nodes.find(n => n.city === 'Lahore') || nodes[0];

  nodes.forEach(node => {
    if (node === lahoreHub) return;

    const corridor = viewer.entities.add({
      polyline: {
        positions: Cesium.Cartesian3.fromDegreesArray([
          lahoreHub.longitude, lahoreHub.latitude,
          node.longitude, node.latitude
        ]),
        width: 1.8,
        arcType: Cesium.ArcType.GEODESIC,
        material: new Cesium.PolylineGlowMaterialProperty({
          glowPower: 0.25,
          taperPower: 0.6,
          color: Cesium.Color.fromCssColorString('#10B981').withAlpha(0.45)
        }),
        distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0.0, 3000000.0)
      }
    });
    corridorEntities.push(corridor);
  });
}

/**
 * Setup Entity Picking (Click and Hover)
 */
function setupEntityPicking() {
  if (!viewer) return;

  const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);

  // Left click pick
  handler.setInputAction((movement) => {
    const pickedObject = viewer.scene.pick(movement.position);
    if (Cesium.defined(pickedObject) && pickedObject.id && pickedObject.id.properties) {
      const nodeData = pickedObject.id.properties.nodeData.getValue();
      openPopupCard(nodeData);
    }
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

  // Mouse move cursor styling
  handler.setInputAction((movement) => {
    const pickedObject = viewer.scene.pick(movement.endPosition);
    viewer.canvas.style.cursor = (Cesium.defined(pickedObject) && pickedObject.id) ? 'pointer' : 'default';
  }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
}

/**
 * Sleek Popup Info-Card Overlay Handlers
 */
function openPopupCard(node) {
  activeNode = node;
  const popup = document.getElementById('cesium-popup-card');
  if (!popup) return;

  const titleEl = document.getElementById('popup-node-title');
  const catEl = document.getElementById('popup-node-category');
  const statusEl = document.getElementById('popup-node-status');
  const cityEl = document.getElementById('popup-city-label');
  const descEl = document.getElementById('popup-node-desc');
  const coordsEl = document.getElementById('popup-coords-label');

  if (titleEl) titleEl.textContent = node.name || 'Spatial Project';
  if (catEl) catEl.textContent = node.category || 'WebGIS';
  if (statusEl) statusEl.textContent = node.status || 'Active';
  if (cityEl) cityEl.textContent = `${node.city || 'Punjab'}, Pakistan`;
  if (descEl) descEl.textContent = node.description || 'Enterprise spatial dataset.';
  if (coordsEl) coordsEl.textContent = `Lat: ${node.latitude.toFixed(4)} · Lon: ${node.longitude.toFixed(4)}`;

  popup.classList.remove('hidden');
  popup.classList.add('visible');
}

function closePopupCard() {
  const popup = document.getElementById('cesium-popup-card');
  if (popup) {
    popup.classList.remove('visible');
    popup.classList.add('hidden');
  }
}

/**
 * Smooth Flight Animation targeting coordinates
 */
function flyToNode(node) {
  if (!viewer) return;

  const targetHeight = is3D ? 45000.0 : 60000.0;
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(
      node.longitude,
      node.latitude - (is3D ? 0.12 : 0.0),
      targetHeight
    ),
    duration: 2.0,
    orientation: is3D ? {
      heading: Cesium.Math.toRadians(0.0),
      pitch: Cesium.Math.toRadians(-52.0),
      roll: 0.0
    } : undefined
  });
}

/**
 * UI Action Controls & Multi-Dimensional Morphing
 */
function initMapControls() {
  const toggleBtn = document.getElementById('btn-toggle-dimension');
  const dimensionIcon = document.getElementById('dimension-icon');
  const dimensionLabel = document.getElementById('dimension-label');
  const sceneIndicator = document.getElementById('map-scene-indicator');
  const resetBtn = document.getElementById('btn-reset-view');
  const searchInput = document.getElementById('map-search-input');
  const popupCloseBtn = document.getElementById('popup-close-btn');
  const popupFlytoBtn = document.getElementById('popup-flyto-btn');
  const regionFilters = document.querySelectorAll('#map-region-filters span');

  // Keyboard shortcut: Ctrl+K or Cmd+K
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchInput) searchInput.focus();
    }
  });

  // 2D / 3D Dimension Morph Toggle Button
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (!viewer) return;

      if (is3D) {
        // Morph to 2D
        viewer.scene.morphTo2D(1.0);
        is3D = false;
        toggleBtn.classList.add('mode-2d');
        if (dimensionIcon) dimensionIcon.textContent = '🗺️';
        if (dimensionLabel) dimensionLabel.textContent = '2D Map';
        if (sceneIndicator) sceneIndicator.textContent = '2D Flat Map';
      } else {
        // Morph to 3D
        viewer.scene.morphTo3D(1.0);
        is3D = true;
        toggleBtn.classList.remove('mode-2d');
        if (dimensionIcon) dimensionIcon.textContent = '🌐';
        if (dimensionLabel) dimensionLabel.textContent = '3D Globe';
        if (sceneIndicator) sceneIndicator.textContent = '3D Globe';
      }
    });
  }

  // Reset View to Pakistan Center
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (!viewer) return;
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(69.8, 30.2, 2200000.0),
        duration: 1.8,
        orientation: is3D ? {
          heading: Cesium.Math.toRadians(0.0),
          pitch: Cesium.Math.toRadians(-72.0),
          roll: 0.0
        } : undefined
      });
      closePopupCard();
    });
  }

  // Client-Side Search with Smooth Flight Animation
  if (searchInput) {
    let debounceTimer = null;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      const query = e.target.value.toLowerCase().trim();

      if (!query) {
        closePopupCard();
        return;
      }

      debounceTimer = setTimeout(() => {
        const match = cachedNodes.find(n => 
          n.name.toLowerCase().includes(query) || 
          (n.city && n.city.toLowerCase().includes(query)) ||
          (n.category && n.category.toLowerCase().includes(query)) ||
          (n.description && n.description.toLowerCase().includes(query))
        );

        if (match) {
          flyToNode(match);
          openPopupCard(match);
        }
      }, 300);
    });
  }

  // Close popup
  if (popupCloseBtn) {
    popupCloseBtn.addEventListener('click', closePopupCard);
  }

  // Popup "Focus Target" button
  if (popupFlytoBtn) {
    popupFlytoBtn.addEventListener('click', () => {
      if (activeNode) flyToNode(activeNode);
    });
  }

  // Region Filter Pills
  if (regionFilters.length) {
    regionFilters.forEach(pill => {
      pill.addEventListener('click', () => {
        regionFilters.forEach(p => {
          p.classList.remove('theme-btn-primary');
          p.classList.add('theme-tag');
        });
        pill.classList.remove('theme-tag');
        pill.classList.add('theme-btn-primary');

        const region = pill.getAttribute('data-region') || 'all';

        if (region === 'all') {
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(69.8, 30.2, 2200000.0),
            duration: 1.6
          });
        } else if (region === 'Punjab') {
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(73.5, 31.4, 550000.0),
            duration: 1.6,
            orientation: is3D ? {
              heading: Cesium.Math.toRadians(0.0),
              pitch: Cesium.Math.toRadians(-55.0),
              roll: 0.0
            } : undefined
          });
        } else if (region === 'Karachi') {
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(67.0, 24.9, 140000.0),
            duration: 1.6,
            orientation: is3D ? {
              heading: Cesium.Math.toRadians(0.0),
              pitch: Cesium.Math.toRadians(-55.0),
              roll: 0.0
            } : undefined
          });
        } else if (region === 'KPK') {
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(71.8, 34.0, 280000.0),
            duration: 1.6,
            orientation: is3D ? {
              heading: Cesium.Math.toRadians(0.0),
              pitch: Cesium.Math.toRadians(-55.0),
              roll: 0.0
            } : undefined
          });
        }
      });
    });
  }
}
