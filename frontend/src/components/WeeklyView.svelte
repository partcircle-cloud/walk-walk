<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import { api } from '../lib/api.js';

  export let language = 'ko';

  const dispatch = createEventDispatcher();

  const texts = {
    ko: {
      title: '📊 산책 기록 저장소',
      loading: '기록을 찾아오고 있어요...',
      emptyTitle: '아직 기록된 산책이 없어요',
      emptyHint: '첫 산책을 시작해볼까요?',
      deleteConfirm: '이 기록을 정말 삭제할까요?',
      deleteError: '기록을 지우지 못했어요.',
      deleteTitle: '삭제',
      thisWeek: '이번 주 산책 기록',
      lastWeek: '지난 주 산책 기록',
      oldRecords: '오래전 산책 기록',
      hour: '시간',
      minute: '분',
      steps: '보',
      weekdays: ['일', '월', '화', '수', '목', '금', '토'],
      close: '닫기'
    },
    en: {
      title: '📊 Walk History',
      loading: 'Loading records...',
      emptyTitle: 'No walk records yet',
      emptyHint: 'Ready to start your first walk?',
      deleteConfirm: 'Are you sure you want to delete this record?',
      deleteError: 'Failed to delete record.',
      deleteTitle: 'Delete',
      thisWeek: 'This Week',
      lastWeek: 'Last Week',
      oldRecords: 'Old Records',
      hour: 'h',
      minute: 'min',
      steps: 'steps',
      weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      close: 'Close'
    }
  };

  $: t = texts[language];

  let walks = [];
  let loading = true;

  onMount(async () => {
    await loadWalks();
  });

  async function loadWalks() {
    try {
      walks = await api.getWalks();
      loading = false;
    } catch (e) {
      console.error('기록 로드 실패:', e);
      loading = false;
    }
  }

  async function deleteRecord(id) {
    if (!confirm(t.deleteConfirm)) return;

    try {
      await api.deleteWalk(id);
      walks = walks.filter(w => w.id !== id);
    } catch (e) {
      console.error('삭제 실패:', e);
      alert(t.deleteError);
    }
  }

  function close() {
    dispatch('close');
  }

  function formatTime(sec) {
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60);
    if (h > 0) {
      return language === 'ko' 
        ? `${h}${t.hour} ${m}${t.minute}` 
        : `${h}${t.hour} ${m}${t.minute}`;
    }
    return language === 'ko' ? `${m}${t.minute}` : `${m}${t.minute}`;
  }

  function formatDate(dateStr) {
    const d = new Date(dateStr);
    const weekdays = t.weekdays;
    
    if (language === 'ko') {
      return `${d.getMonth() + 1}월 ${d.getDate()}일 (${weekdays[d.getDay()]})`;
    } else {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return `${months[d.getMonth()]} ${d.getDate()} (${weekdays[d.getDay()]})`;
    }
  }

  function formatTime2(dateStr) {
    const d = new Date(dateStr);
    if (language === 'ko') {
      return d.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });
    } else {
      return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
    }
  }

  function getWeekLabel(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days < 7) return t.thisWeek;
    if (days < 14) return t.lastWeek;
    return t.oldRecords;
  }

  $: walksByWeek = walks.reduce((acc, walk) => {
    const week = getWeekLabel(walk.date);
    if (!acc[week]) acc[week] = [];
    acc[week].push(walk);
    return acc;
  }, {});
</script>

<div class="weekly-view">
  <div class="view-header">
    <h2>{t.title}</h2>
    <button class="close-btn" on:click={close}>{t.close}</button>
  </div>

  <div class="view-content">
    {#if loading}
      <div class="loading">
        <span class="loading-icon">🍃</span>
        <p>{t.loading}</p>
      </div>
    {:else if walks.length === 0}
      <div class="empty-state card">
        <div class="empty-icon">🐾</div>
        <p>{t.emptyTitle}</p>
        <p class="hint">{t.emptyHint}</p>
      </div>
    {:else}
      {#each Object.entries(walksByWeek) as [week, weekWalks]}
        <div class="week-section">
          <div class="week-label-box">{week}</div>
          <div class="walks-list">
            {#each weekWalks as walk}
              <div class="walk-item card">
                <div class="walk-info">
                  <div class="walk-date">
                    <span class="date-text">{formatDate(walk.date)}</span>
                    <span class="time-text">{formatTime2(walk.date)}</span>
                  </div>
                  <div class="walk-stats-grid">
                    <div class="stat-item">
                      <span class="stat-icon">⏱️</span>
                      <span>{formatTime(walk.duration)}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-icon">📍</span>
                      <span>{walk.distance.toFixed(2)}km</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-icon">👣</span>
                      <span>{walk.steps.toLocaleString()}{t.steps}</span>
                    </div>
                  </div>
                </div>
                <button 
                  class="delete-icon-btn" 
                  on:click={() => deleteRecord(walk.id)} 
                  title={t.deleteTitle}
                >
                  🗑️
                </button>
              </div>
            {/each}
          </div>
        </div>
      {/each}
    {/if}
  </div>
</div>

<style>
  .weekly-view {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #F9F5EB;
    z-index: 2000;
    padding: 24px 16px;
    overflow-y: auto;
    font-family: 'Poppins', sans-serif;
  }

  .view-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 400px;
    margin: 0 auto 24px;
  }

  .view-header h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #8D7B68;
    margin: 0;
  }

  .close-btn {
    background: #FFFBF0;
    border: 3px solid #EEE3CB;
    border-radius: 20px;
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    color: #8D7B68;
    box-shadow: 0 4px 0 #EEE3CB;
    font-family: 'Poppins', sans-serif;
    transition: all 0.2s;
  }

  .close-btn:active {
    transform: translateY(2px);
    box-shadow: 0 2px 0 #EEE3CB;
  }

  .view-content {
    max-width: 400px;
    margin: 0 auto;
  }

  .loading {
    text-align: center;
    padding: 60px 0;
    color: #A69080;
  }

  .loading-icon {
    font-size: 2.5rem;
    display: inline-block;
    animation: bounce 1s infinite;
  }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  .week-section {
    margin-bottom: 32px;
  }

  .week-label-box {
    display: inline-block;
    background: #A4BE7B;
    color: white;
    padding: 6px 16px;
    border-radius: 12px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 12px;
    box-shadow: 0 4px 0 #7E945D;
  }

  .walks-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .walk-item {
    position: relative;
    padding: 18px !important;
  }

  .walk-date {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 12px;
  }

  .date-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: #8D7B68;
  }

  .time-text {
    font-size: 0.85rem;
    color: #A69080;
  }

  .walk-stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    background: #FDF6E3;
    border-radius: 16px;
    padding: 12px;
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #8D7B68;
  }

  .stat-icon {
    font-size: 1.1rem;
  }

  .delete-icon-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    opacity: 0.6;
    transition: opacity 0.2s;
  }

  .delete-icon-btn:hover {
    opacity: 1;
  }

  .empty-state {
    text-align: center;
    padding: 40px 20px;
  }

  .empty-icon { 
    font-size: 3rem; 
    margin-bottom: 16px; 
  }

  .hint { 
    font-size: 0.9rem !important; 
    color: #A4BE7B !important; 
    font-weight: 600; 
  }
</style>