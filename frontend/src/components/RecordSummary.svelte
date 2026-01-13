<script>
  import { createEventDispatcher } from 'svelte';
  import { api } from '../lib/api.js';

  export let expanded = false;
  export let language = 'ko';

  const dispatch = createEventDispatcher();

  const texts = {
    ko: {
      startWalk: '산책 시작하기',
      timeTitle: '함께 산책한 시간',
      distance: '산책 거리',
      steps: '걸음 수',
      messageWalking: '오늘도 즐겁게 걸어봐요! ✨',
      messageReady: '산책 갈 준비가 되었나요?',
      buttonStart: '지금 출발하기!',
      buttonStop: '산책 종료하기 🏠',
      alertTitle: '산책을 무사히 마쳤어요!',
      alertTime: '시간',
      alertDistance: '거리',
      alertSteps: '걸음',
      saveError: '기록을 저장하지 못했어요.',
      unitKm: 'km',
      unitSteps: '보'
    },
    en: {
      startWalk: 'Start Walking',
      timeTitle: 'Walk Time',
      distance: 'Distance',
      steps: 'Steps',
      messageWalking: 'Let\'s enjoy the walk! ✨',
      messageReady: 'Ready for a walk?',
      buttonStart: 'Start Now!',
      buttonStop: 'Finish Walk 🏠',
      alertTitle: 'Walk completed!',
      alertTime: 'Time',
      alertDistance: 'Distance',
      alertSteps: 'Steps',
      saveError: 'Failed to save record.',
      unitKm: 'km',
      unitSteps: 'steps'
    }
  };

  $: t = texts[language];

  let isWalking = false;
  let walkStartTime = null;
  let duration = 0;
  let steps = 0;
  let distance = 0;
  let intervalId = null;
  let watchId = null;
  let lastPosition = null;

  function toggleExpand() {
    if (!expanded && !isWalking) {
      expanded = true;
    }
  }

  function startWalk() {
    isWalking = true;
    walkStartTime = Date.now();
    duration = 0;
    steps = 0;
    distance = 0;
    lastPosition = null;

    dispatch('walkStatusChange', { isWalking: true });

    // 시간 업데이트
    intervalId = setInterval(() => {
      duration = Math.floor((Date.now() - walkStartTime) / 1000);
    }, 1000);

    // GPS 추적 시작
    if ('geolocation' in navigator) {
      watchId = navigator.geolocation.watchPosition(
        (position) => {
          const { latitude, longitude } = position.coords;

          if (lastPosition) {
            // 이전 위치와 현재 위치 사이 거리 계산
            const dist = calculateDistance(
              lastPosition.latitude,
              lastPosition.longitude,
              latitude,
              longitude
            );

            // 최소 5m 이상 이동했을 때만 반영 (GPS 오차 방지)
            if (dist >= 0.005) {
              distance += dist;
              // 걸음수 = 거리(km) × 1300 (1km당 평균 걸음수)
              steps = Math.round(distance * 1300);
            }
          }

          lastPosition = { latitude, longitude };
        },
        (error) => {
          console.error('GPS 추적 실패:', error);
        },
        {
          enableHighAccuracy: true,
          maximumAge: 0,
          timeout: 5000
        }
      );
    }
  }

  async function stopWalk() {
    if (!isWalking) return;
    isWalking = false;
    clearInterval(intervalId);
    
    if (watchId !== null) {
      navigator.geolocation.clearWatch(watchId);
    }

    dispatch('walkStatusChange', { isWalking: false });

    try {
      await api.saveWalk({
        duration,
        distance: parseFloat(distance.toFixed(3)),
        steps
      });
      
      const message = language === 'ko' 
        ? `${t.alertTitle}\n${t.alertTime}: ${formatTime(duration)}\n${t.alertDistance}: ${distance.toFixed(2)}km\n${t.alertSteps}: ${steps}${t.unitSteps}`
        : `${t.alertTitle}\n${t.alertTime}: ${formatTime(duration)}\n${t.alertDistance}: ${distance.toFixed(2)}km\n${t.alertSteps}: ${steps} ${t.unitSteps}`;
      
      alert(message);
      dispatch('walkSaved');
      duration = 0;
      steps = 0;
      distance = 0;
      lastPosition = null;
    } catch (e) {
      console.error('저장 실패:', e);
      alert(t.saveError);
    }
  }

  // Haversine 공식: 두 GPS 좌표 사이의 거리 계산 (km)
  function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // 지구 반지름 (km)
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  function toRad(deg) {
    return deg * (Math.PI / 180);
  }

  function formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }
</script>

<div class="walk-card card {expanded ? 'expanded' : 'collapsed'}" on:click={toggleExpand}>
  <div class="card-header">
    {#if expanded}
      <span class="timer-title">{t.timeTitle}</span>
    {:else}
      <span>{t.startWalk}</span>
    {/if}
  </div>

  {#if expanded}
    <div class="walk-content" on:click|stopPropagation>
      <div class="timer-display">
        <span class="timer-icon">⏰</span>
        <span class="timer-text">{formatTime(duration)}</span>
      </div>

      <div class="walk-stats">
        <div class="stat-box">
          <div class="icon">📍</div>
          <div class="label">{t.distance}</div>
          <div class="value">{distance.toFixed(2)}<small>{t.unitKm}</small></div>
        </div>
        <div class="stat-box">
          <div class="icon">👟</div>
          <div class="label">{t.steps}</div>
          <div class="value">{steps}<small>{t.unitSteps}</small></div>
        </div>
      </div>

      <div class="character-area">
        <!-- 강아지 Waddle (산책 중일 때만) -->
        {#if isWalking}
          <div class="dog-waddle">🐕</div>
        {:else}
          <div class="dog-static">🐕</div>
        {/if}
        
        <div class="message">
          {#if isWalking}
            {t.messageWalking}
          {:else}
            {t.messageReady}
          {/if}
        </div>
      </div>

      <button class="walk-button {isWalking ? 'stop' : 'start'}" on:click={isWalking ? stopWalk : startWalk}>
        {isWalking ? t.buttonStop : t.buttonStart}
      </button>
    </div>
  {/if}
</div>

<style>
  .walk-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .collapsed {
    text-align: center;
    padding: 24px !important;
  }

  .card-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #8D7B68;
  }

  .timer-title {
    font-size: 1rem;
    color: #A69080;
  }

  .timer-display {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 15px 0;
  }

  .timer-text {
    font-size: 2.5rem;
    font-weight: 700;
    color: #8D7B68;
  }

  .walk-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 20px;
  }

  .stat-box {
    background: #FDF6E3;
    border: 2px solid #EEE3CB;
    border-radius: 20px;
    padding: 12px 5px;
    text-align: center;
  }

  .stat-box .label {
    font-size: 0.75rem;
    color: #A69080;
    margin: 4px 0;
  }

  .stat-box .value {
    font-size: 1.2rem;
    font-weight: 700;
    color: #8D7B68;
  }

  .stat-box .value small {
    font-size: 0.7rem;
    margin-left: 2px;
  }

  .character-area {
    margin: 20px 0;
    text-align: center;
  }

  /* 강아지 Waddle 애니메이션 */
  .dog-waddle {
    font-size: 3rem;
    animation: waddle 1.5s ease-in-out infinite;
  }

  .dog-static {
    font-size: 3rem;
  }

  @keyframes waddle {
    0%, 100% {
      transform: rotate(-10deg);
    }
    50% {
      transform: rotate(10deg);
    }
  }

  .message {
    font-size: 1.1rem;
    font-weight: 600;
    color: #8D7B68;
    margin-top: 10px;
  }

  .walk-button {
    width: 100%;
    padding: 18px;
    border-radius: 24px;
    border: none;
    font-size: 1.3rem;
    font-weight: 700;
    font-family: 'Poppins', sans-serif;
    color: white;
    cursor: pointer;
    transition: all 0.2s;
  }

  .start {
    background: #A4BE7B;
    box-shadow: 0 6px 0 #7E945D;
  }

  .stop {
    background: #E86A5F;
    box-shadow: 0 6px 0 #B94A40;
  }

  .walk-button:active {
    transform: translateY(4px);
    box-shadow: 0 2px 0 transparent;
  }

  @media (max-width: 400px) {
    .stat-box .value { font-size: 1rem; }
    .dog-waddle, .dog-static { font-size: 2.5rem; }
  }
</style>