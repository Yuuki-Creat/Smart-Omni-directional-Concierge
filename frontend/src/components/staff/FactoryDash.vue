<!-- Factory Dashboard Component -->
<template>
    <div class="card dashboard-card">
        <h2>【工場管理者】ダッシュボード</h2>

        <!-- ローディング状態 -->
        <div v-if="loading" class="loading-spinner">
            データを取得中...
        </div>

        <!-- エラー状態 -->
        <div v-else-if="error" class="error-msg">
            {{ error }}
        </div>

        <!-- データ表示 -->
        <div v-else-if="schedule" class="dashboard-content">
            <div class="status-badge" :class="schedule.status">
                システム状態: {{ schedule.status === 'stable' ? '安定' : '警告' }}
            </div>

            <div class="stats-grid">
                <div class="stat-box primary">
                    <span class="stat-label">現在のベースロード</span>
                    <span class="stat-value">{{ schedule.base_load }}<small>枠</small></span>
                </div>
                <div class="stat-box success">
                    <span class="stat-label">個人充当可能スロット</span>
                    <span class="stat-value">{{ schedule.available_slots }}<small>枠</small></span>
                </div>
                <div class="stat-box warning">
                    <span class="stat-label">待機中の個人案件</span>
                    <span class="stat-value">{{ schedule.b2c_pending }}<small>件</small></span>
                </div>
            </div>
        </div>

        <button class="btn-refresh" @click="loadSchedule" :disabled="loading">
            稼働率を再計算
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchFactorySchedule } from '../../api/apiClient';

const schedule = ref(null);
const loading = ref(false);
const error = ref(null);

const loadSchedule = async () => {
    loading.value = true;
    error.value = null;
    try {
        const res = await fetchFactorySchedule();
        if (res && res.data) {
            schedule.value = res.data;
        } else {
            throw new Error("データのフォーマットが不正です");
        }
    } catch (err) {
        error.value = "スケジュールの取得に失敗しました。";
        console.error(err);
    } finally {
        loading.value = false;
    }
};

onMounted(loadSchedule);
</script>

<style scoped>
.dashboard-card {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    padding: 24px;
    transition: all 0.3s ease;
}

.loading-spinner {
    text-align: center;
    color: #666;
    padding: 20px 0;
    font-weight: bold;
}

.error-msg {
    color: #dc3545;
    background: #f8d7da;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
}

.status-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9em;
    margin-bottom: 20px;
}
.status-badge.stable { background: #d4edda; color: #155724; }

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.stat-box {
    padding: 16px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid #eee;
}
.stat-box.primary { border-left: 4px solid #007bff; }
.stat-box.success { border-left: 4px solid #28a745; }
.stat-box.warning { border-left: 4px solid #ffc107; }

.stat-label {
    font-size: 0.85em;
    color: #666;
    margin-bottom: 8px;
}
.stat-value {
    font-size: 1.8em;
    font-weight: bold;
    color: #333;
}
.stat-value small { font-size: 0.5em; color: #888; }

.btn-refresh {
    width: 100%;
    padding: 12px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
}
.btn-refresh:hover:not(:disabled) { background: #0056b3; }
.btn-refresh:disabled { background: #ccc; cursor: not-allowed; }
</style>