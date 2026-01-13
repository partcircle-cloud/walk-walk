const API_URL = 'http://192.168.25.56:8000';

export const api = {
  // 날씨
  async getWeather() {
    const res = await fetch(`${API_URL}/weather`);
    if (!res.ok) throw new Error('날씨 로드 실패');
    return res.json();
  },

  // 산책 기록 저장
  async saveWalk(data) {
    const res = await fetch(`${API_URL}/walks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('저장 실패');
    return res.json();
  },

  // 전체 기록
  async getWalks() {
    const res = await fetch(`${API_URL}/walks`);
    if (!res.ok) throw new Error('기록 로드 실패');
    return res.json();
  },

  // 최근 기록
  async getRecentWalk() {
    const res = await fetch(`${API_URL}/walks/recent`);
    if (res.status === 404) return null;
    if (!res.ok) throw new Error('최근 기록 로드 실패');
    return res.json();
  },

  // 기록 삭제
  async deleteWalk(id) {
    const res = await fetch(`${API_URL}/walks/${id}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error('삭제 실패');
    return res.json();
  }
};