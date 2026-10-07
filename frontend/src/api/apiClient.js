// Connection Module to the backend API
// ホスティングサービス(Render)のURL バックエンドAPI
const API_BASE_URL = 'https://smart-omni-directional-concierge.onrender.com/api';

// 個人チェックイン情報をサーバーに送信
export const submitIndividualCheckin = async (data) => {
    const res = await fetch(`${API_BASE_URL}/individual/checkin`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // JSON形式に変換して送信内容をbodyにセット
        body: JSON.stringify(data),
    });
    return res.json();
};

// 指定の法人IDの現在のステータスをサーバーから取得(データ内容はデモ用)
export const fetchCorporateStatus = async (corpId) => {
    const res = await fetch(`${API_BASE_URL}/corporate/status/${corpId}`);
    return res.json();
};

// 工場の稼働スケジュールをサーバーから取得
export const fetchFactorySchedule = async () => {
    const res = await fetch(`${API_BASE_URL}/factory/schedule`);
    return res.json();
};

// 店舗での受付情報をサーバーに送信
export const submitStoreReception = async (ticketId) => {
    const res = await fetch(`${API_BASE_URL}/store/reception`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticket_id: ticketId }),
    });
    return res.json();
};
