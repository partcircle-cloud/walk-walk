<script>
  import { onMount, onDestroy } from 'svelte';
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';

  export let language = 'ko';

  const texts = {
    ko: {
      label: '지도',
      myLocation: '나의 현재 위치예요!',
      gpsError: '위치 가져오기 실패'
    },
    en: {
      label: 'Map',
      myLocation: 'My current location!',
      gpsError: 'Failed to get location'
    }
  };

  $: t = texts[language];

  let mapContainer;
  let map;
  let userMarker;

  onMount(() => {
    map = L.map(mapContainer, {
      zoomControl: false
    }).setView([37.5665, 126.9780], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(map);

    setTimeout(() => {
      map.invalidateSize();
    }, 100);

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;
          map.setView([lat, lng], 15);

          const icon = L.divIcon({
            html: '<div style="font-size:32px">📍</div>',
            className: 'leaflet-div-icon',
            iconSize: [40, 40]
          });

          userMarker = L.marker([lat, lng], { icon })
            .addTo(map)
            .bindPopup(t.myLocation);
        },
        (error) => {
          console.error(t.gpsError, error);
        }
      );
    }
  });

  onDestroy(() => {
    if (map) {
      map.remove();
    }
  });
</script>

<div class="map-card card">
  <div bind:this={mapContainer} class="map-container"></div>
  <div class="map-label">{t.label}</div>
</div>

<style>
  .map-card {
    width: 100%;
    padding: 12px !important;
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-sizing: border-box;
  }

  .map-container {
    width: 100%;
    aspect-ratio: 16 / 9;
    border-radius: 20px;
    border: 2px solid #EEE3CB;
    overflow: hidden;
    z-index: 1;
  }

  @media (max-width: 768px) {
    .map-container {
      aspect-ratio: 4 / 3;
      max-height: 50vh;
    }
  }

  @media (max-width: 375px) {
    .map-container {
      aspect-ratio: 1 / 1;
      max-height: 40vh;
    }
  }

  .map-label {
    font-family: 'Poppins', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #8D7B68;
    text-align: center;
  }

  :global(.leaflet-div-icon) {
    background: none !important;
    border: none !important;
  }

  :global(.leaflet-popup-content-wrapper) {
    background-color: #FFFBF0 !important;
    color: #4A3F35 !important;
    font-family: 'Poppins', sans-serif !important;
    border-radius: 12px !important;
    border: 2px solid #EEE3CB !important;
  }

  :global(.leaflet-popup-tip) {
    background-color: #FFFBF0 !important;
    border: 2px solid #EEE3CB !important;
  }
</style>