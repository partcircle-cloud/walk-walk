<script>
  import { onMount } from 'svelte';

  export let language = 'ko';

  const API_KEY = import.meta.env.VITE_WEATHER_API_KEY || 'YOUR_API_KEY_HERE';

  const texts = {
    ko: {
      loading: '오늘의 날씨를 물어보고 있어요...',
      todayWeather: '오늘의 날씨는',
      is: '이에요',
      error: '날씨 정보를 불러올 수 없어요',
      clear: '맑음',
      clouds: '흐림',
      rain: '비',
      drizzle: '이슬비',
      thunderstorm: '뇌우',
      snow: '눈',
      mist: '안개',
      smoke: '연무',
      haze: '실안개',
      dust: '먼지',
      fog: '안개',
      sand: '모래바람',
      ash: '화산재',
      squall: '돌풍',
      tornado: '토네이도'
    },
    en: {
      loading: 'Checking today\'s weather...',
      todayWeather: 'Today\'s weather is',
      is: '',
      error: 'Unable to load weather',
      clear: 'Clear',
      clouds: 'Cloudy',
      rain: 'Rainy',
      drizzle: 'Drizzle',
      thunderstorm: 'Thunderstorm',
      snow: 'Snowy',
      mist: 'Misty',
      smoke: 'Smoke',
      haze: 'Haze',
      dust: 'Dust',
      fog: 'Foggy',
      sand: 'Sand',
      ash: 'Ash',
      squall: 'Squall',
      tornado: 'Tornado'
    }
  };

  $: t = texts[language];

  let weather = null;
  let loading = true;
  let error = false;

  onMount(async () => {
    await fetchWeather();
  });

  async function fetchWeather() {
    try {
      // GPS 지원 여부 확인
      if (!('geolocation' in navigator)) {
        console.error('❌ Geolocation not supported');
        alert('❌ GPS를 지원하지 않는 브라우저입니다');
        setDefaultWeather();
        return;
      }

      console.log('✅ Geolocation supported, requesting permission...');
      
      // 사용자의 현재 위치 가져오기
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          console.log('✅ GPS 권한 허용됨!');
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          console.log(`📍 위치: ${lat}, ${lon}`);

          // OpenWeatherMap API 호출
          const lang = language === 'ko' ? 'kr' : 'en';
          const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=${lang}`;

          console.log('🌤️ 날씨 API 호출 중...');
          const response = await fetch(url);
          
          if (response.ok) {
            console.log('✅ 날씨 API 성공!');
            const data = await response.json();
            
            // 날씨 아이콘 매핑
            const iconMap = {
              '01d': '☀️', '01n': '🌙',
              '02d': '⛅', '02n': '☁️',
              '03d': '☁️', '03n': '☁️',
              '04d': '☁️', '04n': '☁️',
              '09d': '🌧️', '09n': '🌧️',
              '10d': '🌦️', '10n': '🌧️',
              '11d': '⛈️', '11n': '⛈️',
              '13d': '❄️', '13n': '❄️',
              '50d': '🌫️', '50n': '🌫️'
            };

            weather = {
              temp: data.main.temp,
              condition: translateCondition(data.weather[0].main),
              icon: iconMap[data.weather[0].icon] || '🌤️',
              description: data.weather[0].description
            };
            
            loading = false;
          } else {
            console.error('❌ 날씨 API 실패:', response.status);
            throw new Error('API 응답 실패');
          }
        },
        (err) => {
          console.error('❌ GPS 권한 거부:', err);
          alert(`❌ GPS 에러: ${err.message}\n코드: ${err.code}`);
          setDefaultWeather();
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    } catch (e) {
      console.error('날씨 로드 실패:', e);
      setDefaultWeather();
    }
  }

  function setDefaultWeather() {
    error = true;
    loading = false;
    weather = {
      temp: 18,
      condition: t.clear,
      icon: '☀️'
    };
  }

  function translateCondition(condition) {
    const conditionLower = condition.toLowerCase();
    
    if (conditionLower === 'clear') return t.clear;
    if (conditionLower === 'clouds') return t.clouds;
    if (conditionLower === 'rain') return t.rain;
    if (conditionLower === 'drizzle') return t.drizzle;
    if (conditionLower === 'thunderstorm') return t.thunderstorm;
    if (conditionLower === 'snow') return t.snow;
    if (conditionLower === 'mist') return t.mist;
    if (conditionLower === 'smoke') return t.smoke;
    if (conditionLower === 'haze') return t.haze;
    if (conditionLower === 'dust') return t.dust;
    if (conditionLower === 'fog') return t.fog;
    if (conditionLower === 'sand') return t.sand;
    if (conditionLower === 'ash') return t.ash;
    if (conditionLower === 'squall') return t.squall;
    if (conditionLower === 'tornado') return t.tornado;
    
    return condition;
  }

  // 언어 변경 시 날씨 다시 불러오기
  $: if (language) {
    loading = true;
    fetchWeather();
  }
</script>

<div class="weather-card card" class:loading>
  {#if loading}
    <div class="status-content">
      <span class="icon animate-spin">🍃</span>
      <span>{t.loading}</span>
    </div>
  {:else if weather}
    <div class="weather-content">
      <div class="main-info">
        <span class="icon">{weather.icon}</span>
        <span class="temp">{Math.round(weather.temp)}°C</span>
      </div>
      <div class="divider"></div>
      <div class="sub-info">
        {#if language === 'ko'}
          <span class="condition">{t.todayWeather} <strong>{weather.condition}</strong>{t.is}</span>
        {:else}
          <span class="condition">{t.todayWeather} <strong>{weather.condition}</strong></span>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .weather-card {
    width: 100%; 
    padding: 16px 24px !important;
    display: flex;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
    min-height: 80px;
  }

  .weather-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    gap: 15px;
  }

  .main-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .icon {
    font-size: 2.2rem;
  }

  .temp {
    font-size: 1.5rem;
    font-weight: 700;
    color: #8D7B68;
  }

  .divider {
    width: 2px;
    height: 30px;
    background-color: #EEE3CB;
  }

  .sub-info {
    flex: 1;
    font-family: 'Poppins', sans-serif;
    color: #A69080;
    font-size: 0.95rem;
  }

  .condition strong {
    color: #8D7B68;
    font-weight: 600;
  }

  .status-content {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #A69080;
    font-size: 0.9rem;
  }

  .loading {
    opacity: 0.7;
  }

  .animate-spin {
    display: inline-block;
    animation: rotate 2s linear infinite;
  }

  @keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  @media (max-width: 380px) {
    .temp { font-size: 1.2rem; }
    .sub-info { font-size: 0.85rem; }
  }
</style>