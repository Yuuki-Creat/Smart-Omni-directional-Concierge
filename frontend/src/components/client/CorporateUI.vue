<!-- Corporate Status Check UI -->
<template>
    <div class="card corporate-card">
        <h2>法人のお客様：ステータス確認</h2>
        <!-- 法人ID表示(デモ用) -->
        <p class="corp-id-label">法人ID: <strong>{{ currentCorpId }}</strong></p>

        <!-- 状態に応じた画面の出し分け -->
        <!-- 通信中 -->
        <div v-if="loading" class="loading-state">
            最新の情報を取得しています...
        </div>
        <!-- エラー表示 -->
        <div v-else-if="error" class="error-msg">
            {{ error }}
        </div>

        <!-- ステータスデータ表示 -->
        <div v-else-if="statusData" class="status-dashboard">
            <div class="status-box">
                <span class="box-title">工場お預かり中（洗浄中）</span>
                <span class="box-value">{{ statusData.uniforms_in_factory }}<small>着</small></span>
            </div>
            <div class="status-box highlight">
                <span class="box-title">次回納品予定日</span>
                <span class="box-value date">{{ statusData.next_delivery_date }}</span>
            </div>
        </div>

        <!-- 最新情報の再取得 loading中は押下不可 -->
        <button @click="loadStatus" class="btn-refresh" :disabled="loading">
            {{ loading ? '更新中...' : '最新情報を取得' }}
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';   // Vueのデータ連動、画面表示自動実行
import { fetchCorporateStatus } from '../../api/apiClient'; // API通信関数をインポート

const currentCorpId = 'CORP_001'; // デモ用に固定（本来はログイン情報などから取得）
// ステータスデータ、通信中フラグ、エラーメッセージを入れる箱
const statusData = ref(null);
const loading = ref(false);
const error = ref('');

// 法人の最新ステータスを取得する関数
const loadStatus = async () => {
    loading.value = true;
    error.value = '';

    try {
        // バックエンドAPIから法人ステータスを取得
        const res = await fetchCorporateStatus(currentCorpId);
        // バックエンドからの返し方によって、resの中身か、res.dataの中身かを取り出す
        statusData.value = res.data || res;
    } catch (err) {
        // エラー処理
        console.error("法人データ取得エラー:", err);
        error.value = "情報の取得に失敗しました。時間をおいて再試行してください。";
    } finally {
        loading.value = false;
    }
};

// 初回表示時に自動でステータスを取得
onMounted(loadStatus);
</script>

<style scoped>
/* 全体のデザイン */
.corporate-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 24px;
    border: 12px solid #173f4e;
    max-width: 400px;
    margin: 0 auto;
}

/* タイトルの設定 */
.corporate-card h2 {
    font-size: 18px;
    color: #173f4e;
    margin-bottom: 20px;
    border-bottom: 2px dotted #008992;
    padding-bottom: 10px;
    display: inline-block;
}

/* 法人ID表示部分 */
.corp-id-label {
    color: #666; font-size: 14px; margin-bottom: 20px;
    border-bottom: 1px solid #e0e8e3; padding-bottom: 10px;
}

/* ローディング状態 */
.loading-state { text-align: center; padding: 30px 0; color: #5ba77a; font-weight: bold; }
.error-msg { background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 8px; margin-bottom: 20px; text-align: center; }

/* ステータス表示ダッシュボード */
.status-dashboard { display: flex; flex-direction: column; gap: 15px; margin-bottom: 24px; }
/* ステータスボックス */
.status-box {
    background: #f8f9fa; border-left: 5px solid #a4b3a9;
    padding: 20px; border-radius: 8px; display: flex; flex-direction: column;
}
.status-box.highlight {
    border-left-color: #5ba77a;
    background: #eaf5ee;
}
/* ボックス内の文字デザイン */
.box-title { font-size: 14px; color: #555; margin-bottom: 8px; font-weight: bold; }
.box-value { font-size: 32px; font-weight: bold; color: #222; }
.box-value small { font-size: 16px; color: #666; margin-left: 4px; }
.box-value.date { color: #5ba77a; }

/* 更新ボタンのデザイン */
.btn-refresh {
    width: 100%; 
    padding: 12px;
    margin-top: 10px;
    background-color: #008992;
    color: white; 
    border: none; 
    border-radius: 8px;
    font-size: 16px; 
    font-weight: bold; 
    cursor: pointer; 
    transition: background-color 0.3s;
}
.btn-refresh:hover:not(:disabled) { background-color: #006f77; }
.btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }
</style>