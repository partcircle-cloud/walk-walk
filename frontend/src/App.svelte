<script>
  import MapCard from './components/MapCard.svelte';
  import WeatherCard from './components/WeatherCard.svelte';
  import RecordSummary from './components/RecordSummary.svelte';
  import WeeklyView from './components/WeeklyView.svelte';
  import { api } from './lib/api.js';
  import { onMount } from 'svelte';

  let language = 'ko';

  const texts = {
    ko: {
      title: '산책 산책 🐾',
      mapTitle: '🗺️ 지도',
      mapPreview: '📍 산책 지도 확인하기',
      recentWalkTitle: '최근 산책 기록',
      noRecord: '아직 기록된 산책이 없어요!',
      viewAll: '전체 기록 보기 →',
      during: '동안',
      walked: '걸었어요',
      steps: '걸음',
      warningBanner: '📱 데모 버전: 산책 중에는 화면을 켜두세요',
      footerDemo: '이 버전은 데모입니다.',
      copyright: '© 2026 partcircle. All rights reserved.',
      close: '닫기'
    },
    en: {
      title: 'WALK WALK 🐾',
      mapTitle: '🗺️ Map',
      mapPreview: '📍 View Walk Map',
      recentWalkTitle: 'Recent Walk',
      noRecord: 'No walk records yet!',
      viewAll: 'View All →',
      during: 'for',
      walked: 'walked',
      steps: 'steps',
      warningBanner: '📱 Demo Version: Keep screen on during walk',
      footerDemo: 'This version is a demo.',
      copyright: '© 2026 partcircle. All rights reserved.',
      close: 'Close'
    }
  };

  $: t = texts[language];

  let showWeeklyView = false;
  let showMapView = false;
  let recentWalk = null;
  let walkExpanded = false;

  onMount(async () => {
    await loadRecentWalk();
  });

  async function loadRecentWalk() {
    try {
      recentWalk = await api.getRecentWalk();
    } catch (e) {
      console.log('최근 기록 없음');
    }
  }

  function openMapView() { showMapView = true; }
  function closeMapView() { showMapView = false; }
  function openWeeklyView() { showWeeklyView = true; }
  function closeWeeklyView() {
    showWeeklyView = false;
    loadRecentWalk();
  }
  function handleWalkSaved() { loadRecentWalk(); }

  function handleWalkStatusChange(event) {
    // 산책 상태 변경 시 처리 (필요시)
  }

  function formatTime(sec) {
    const m = Math.floor(sec / 60);
    return language === 'ko' ? `${m}분` : `${m}min`;
  }
</script>

<!-- 언어 전환 버튼 -->
<div class="language-toggle">
  <button 
    class:active={language === 'ko'} 
    on:click={() => language = 'ko'}
  >
    KO
  </button>
  <button 
    class:active={language === 'en'} 
    on:click={() => language = 'en'}
  >
    EN
  </button>
</div>

{#if showWeeklyView}
  <WeeklyView on:close={closeWeeklyView} {language} />
{:else if showMapView}
  <div class="map-fullscreen">
    <div class="map-header">
      <h2>{t.mapTitle}</h2>
      <button class="close-btn" on:click={closeMapView}>{t.close}</button>
    </div>
    <MapCard {language} />
  </div>
{:else}
  <main class="app-container">
    <header class="app-header">
      <h1 class="sidebar-label">{t.title}</h1>
    </header>

    <section class="main-content">
      <WeatherCard {language} />

      <div class="map-card-small card" on:click={openMapView}>
        <div class="map-preview">{t.mapPreview}</div>
      </div>

      <RecordSummary 
        bind:expanded={walkExpanded} 
        on:walkSaved={handleWalkSaved}
        on:walkStatusChange={handleWalkStatusChange}
        {language}
      />

      <div class="card history-card" on:click={openWeeklyView}>
        <h3 class="card-header">{t.recentWalkTitle}</h3>
        {#if recentWalk}
          <div class="recent-walk-box">
            <span class="icon">🐶</span>
            <div class="walk-info">
              <span class="walk-detail">
                {formatTime(recentWalk.duration)} {t.during}
              </span>
              <span class="walk-detail">
                {recentWalk.distance.toFixed(2)}km {t.walked}
              </span>
              <span class="walk-detail">({recentWalk.steps}{t.steps})</span>
            </div>
          </div>
        {:else}
          <div class="no-record">{t.noRecord}</div>
        {/if}
        <div class="view-all">{t.viewAll}</div>
      </div>
    </section>
  </main>
{/if}

<!-- 하단 고정 배너 -->
<div class="warning-banner">
  {t.warningBanner}
</div>

<!-- 푸터 -->
<footer class="app-footer">
  <p>{t.footerDemo}</p>
  <p class="copyright">{t.copyright}</p>
</footer>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

  :global(body) {
    margin: 0;
    padding: 0;
    background-color: #F9F5EB;
    font-family: 'Poppins', sans-serif;
    color: #4A3F35;
    display: flex;
    justify-content: center;
  }

  /* 언어 전환 버튼 */
  .language-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    display: flex;
    gap: 8px;
    z-index: 1000;
  }

  .language-toggle button {
    padding: 10px 20px;
    border: 2px solid #EEE3CB;
    border-radius: 12px;
    background: #FFFBF0;
    color: #A69080;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Poppins', sans-serif;
  }

  .language-toggle button.active {
    background: #A4BE7B;
    color: white;
    border-color: #A4BE7B;
    box-shadow: 0 4px 0 #8DA869;
  }

  .language-toggle button:active {
    transform: translateY(2px);
    box-shadow: 0 2px 0 #8DA869;
  }

  .app-container {
    width: 100%;
    max-width: 400px;
    min-height: 100vh;
    padding: 24px 16px 200px 16px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .app-header {
    text-align: center;
    margin-bottom: 8px;
  }

  .sidebar-label {
    font-size: 1.4rem;
    font-weight: 700;
    color: #8D7B68;
    margin: 0;
  }

  .main-content {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  :global(.card) {
    background: #FFFBF0 !important;
    border: 3px solid #EEE3CB !important;
    border-radius: 28px !important;
    padding: 20px;
    box-shadow: 0 8px 0 #EEE3CB !important;
    position: relative;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
    box-sizing: border-box;
  }

  :global(.card:active) {
    transform: translateY(4px);
    box-shadow: 0 4px 0 #EEE3CB !important;
  }

  :global(.card::before) { display: none !important; }

  .card-header {
    font-size: 1.2rem;
    font-weight: 600;
    color: #8D7B68;
    margin: 0 0 12px 0;
  }

  .recent-walk-box {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #FDF6E3;
    padding: 12px 16px;
    border-radius: 18px;
    margin-bottom: 12px;
  }

  .walk-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .walk-detail {
    font-size: 0.95rem;
    font-weight: 400;
  }

  .no-record {
    text-align: center;
    padding: 20px;
    color: #A69080;
    font-style: italic;
  }

  .view-all {
    text-align: right;
    font-size: 0.9rem;
    color: #A4BE7B;
    font-weight: 600;
  }

  .map-card-small {
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F0EAD6 !important;
  }

  .map-preview {
    font-weight: 600;
    color: #8D7B68;
  }

  /* 지도 전체화면 */
  .map-fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #F9F5EB;
    z-index: 2000;
    padding: 20px;
    box-sizing: border-box;
  }

  .map-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 400px;
    margin: 0 auto 20px;
  }

  .map-header h2 {
    font-weight: 700;
    color: #8D7B68;
    margin: 0;
  }

  .close-btn {
    background: #FFFBF0;
    border: 3px solid #EEE3CB;
    border-radius: 20px;
    padding: 12px 24px;
    cursor: pointer;
    font-weight: 700;
    font-size: 1rem;
    color: #8D7B68;
    box-shadow: 0 4px 0 #EEE3CB;
    font-family: 'Poppins', sans-serif;
    transition: all 0.2s;
  }

  .close-btn:active {
    transform: translateY(2px);
    box-shadow: 0 2px 0 #EEE3CB;
  }

  /* 하단 고정 배너 - 카드 너비에 맞춤 */
  .warning-banner {
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 400px;
    width: calc(100% - 32px);
    background: #FEF3C7;
    border: 3px solid #F59E0B;
    border-radius: 20px;
    padding: 12px 20px;
    text-align: center;
    font-weight: 600;
    color: #92400E;
    z-index: 900;
    font-family: 'Poppins', sans-serif;
    box-sizing: border-box;
  }

  /* 푸터 */
  .app-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #FFFBF0;
    border-top: 3px solid #EEE3CB;
    padding: 16px 20px;
    text-align: center;
    z-index: 900;
  }

  .app-footer p {
    margin: 4px 0;
    color: #8D7B68;
    font-size: 0.9rem;
  }

  .app-footer .copyright {
    font-size: 0.8rem;
    color: #A69080;
  }

  @media (max-width: 768px) {
    .language-toggle {
      top: 10px;
      right: 10px;
    }

    .language-toggle button {
      padding: 8px 16px;
      font-size: 0.85rem;
    }

    .warning-banner {
      font-size: 0.85rem;
      padding: 10px 16px;
    }
  }
</style>