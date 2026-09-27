<!-- Corporate Status Check UI -->
<template>
    <div class="card corporate-card">
        <h2>【法人のお客様】ステータス確認</h2>
        <p class="corp-id-label">法人ID: <strong>{{ currentCorpId }}</strong></p>

        <!-- 状態に応じた画面の出し分け -->
        <div v-if="loading" class="loading-state">
            最新の情報を取得しています...
        </div>

        <div v-else-if="error" class="error-msg">
            {{ error }}
        </div>

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

        <button @click="loadStatus" class="btn-refresh" :disabled="loading">
            {{ loading ? '更新中...' : '最新情報を取得' }}
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchCorporateStatus } from '../../api/apiClient';

const currentCorpId = 'CORP_001'; // デモ用に固定（本来はログイン情報などから取得）
const statusData = ref(null);
const loading = ref(false);
const error = ref('');

const loadStatus = async () => {
    loading.value = true;
    error.value = '';

    try {
        const res = await fetchCorporateStatus(currentCorpId);
        // バックエンドからの返し方によって、resの中身か、res.dataの中身かを取り出す
        statusData.value = res.data || res;
    } catch (err) {
        console.error("法人データ取得エラー:", err);
        error.value = "情報の取得に失敗しました。時間をおいて再試行してください。";
    } finally {
        loading.value = false;
    }
};

onMounted(loadStatus);
</script>

<style scoped>
.corporate-card {
    background: #ffffff; border-radius: 12px; padding: 24px;
    box-shadow: 0 4px 15px rgba(91, 167, 122, 0.08);
}
.corp-id-label {
    color: #666; font-size: 14px; margin-bottom: 20px;
    border-bottom: 1px solid #e0e8e3; padding-bottom: 10px;
}
.loading-state { text-align: center; padding: 30px 0; color: #5ba77a; font-weight: bold; }
.error-msg { background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 8px; margin-bottom: 20px; text-align: center; }

.status-dashboard { display: flex; flex-direction: column; gap: 15px; margin-bottom: 24px; }
.status-box {
    background: #f8f9fa; border-left: 5px solid #a4b3a9;
    padding: 20px; border-radius: 8px; display: flex; flex-direction: column;
}
.status-box.highlight {
    border-left-color: #5ba77a;
    background: #eaf5ee;
}
.box-title { font-size: 14px; color: #555; margin-bottom: 8px; font-weight: bold; }
.box-value { font-size: 32px; font-weight: bold; color: #222; }
.box-value small { font-size: 16px; color: #666; margin-left: 4px; }
.box-value.date { color: #5ba77a; }

.btn-refresh {
    width: 100%; padding: 12px; background-color: #f4f8f5; color: #333;
    border: 1px solid #c9d8ce; border-radius: 8px; font-weight: bold;
    cursor: pointer; transition: all 0.2s;
}
.btn-refresh:hover:not(:disabled) { background-color: #e0eee4; }
.btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }
</style>