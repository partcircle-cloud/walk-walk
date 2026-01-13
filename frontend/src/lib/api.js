// localStorage 기반 API
export const api = {
  // 산책 기록 저장
  async saveWalk(data) {
    const walks = JSON.parse(localStorage.getItem('walks') || '[]');
    const newWalk = {
      id: Date.now(),
      date: new Date().toISOString(),
      duration: data.duration,
      distance: data.distance,
      steps: data.steps
    };
    walks.push(newWalk);
    localStorage.setItem('walks', JSON.stringify(walks));
    return newWalk;
  },

  // 전체 기록 가져오기
  async getWalks() {
    const walks = JSON.parse(localStorage.getItem('walks') || '[]');
    return walks.sort((a, b) => new Date(b.date) - new Date(a.date));
  },

  // 최근 기록
  async getRecentWalk() {
    const walks = await this.getWalks();
    return walks[0] || null;
  },

  // 기록 삭제
  async deleteWalk(id) {
    const walks = JSON.parse(localStorage.getItem('walks') || '[]');
    const filtered = walks.filter(w => w.id !== id);
    localStorage.setItem('walks', JSON.stringify(filtered));
    return { success: true };
  },

  // 날씨는 WeatherCard에서 직접 처리
  async getWeather() {
    return null;
  }
};