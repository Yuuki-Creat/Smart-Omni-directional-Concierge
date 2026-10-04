<!-- Factory Dashboard Component -->
<template>
    <div class="card dashboard-card">
        <h2>工場：平準化ダッシュボード</h2>
        <p calss="desc">固定需要を土台に、柔軟需要を「空き時間」に自動で差し込みます。</p>

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
            <div class="Overview">
                <h3 class="overview-title">本日の稼働状況</h3>
                <span class="stat-value">{{ schedule.status === 'stable' ? '安定' : '警告' }}</span>
                <p></p>
            </div>
            <div class="stats-grid">
                <div class="stat-box primary">
                    <span class="stat-label">B2B 固定需要</span>
                    <span class="stat-value">{{ schedule.base_load }}<small>枠</small></span>
                </div>
                <div class="stat-box info">
                    <span class="stat-label">B2C 柔軟需要</span>
                    <span class="stat-value">{{ schedule.b2c_pending }}<small>件</small></span>
                </div>
                <div class="stat-box success">
                    <span class="stat-label">空き枠</span>
                    <span class="stat-value">{{ schedule.available_slots }}<small>枠</small></span>
                </div>
            </div>

            <div class="tetris-chart">
                <h3 class="chart-title">テトリス型・平準化エンジン</h3>

                <div class="chart-container">
                    <div v-for="(slot, index) in schedule.hourly_schedule" :key="index" class="bar-group">
                        <div class="bar-wrapper">
                            <div class="bar b2c-bar"
                                :style="{ height: (slot.b2c_load / slot.capacity * 100) + '%' }"
                                :title="'B2C: ' + slot.b2c_load">
                            </div>
                            <div class="bar b2b-bar"
                                :style="{ height: (slot.b2b_load / slot.capacity * 100) + '%' }"
                                :title="'B2B: ' + slot.b2b_load">
                            </div>
                        </div>
                        <div class="time-label">{{ slot.time.split(':')[0] }}</div>
                    </div>
                </div>
                <div class="legend">
                    <span class="legend-item"><span class="color-box b2b-box"></span>B2B 固定需要</span>
                    <span class="legend-item"><span class="color-box b2c-box"></span>B2C おまかせ保管 柔軟需要</span>
                </div>
            </div>
        </div>
        <button class="btn-refresh" @click="loadSchedule" :disabled="loading">
            最新の稼働状況を取得
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
            console.log("スケジュールデータ:", schedule.value);
        } else {
            schedule.value = res;
        }
    } catch (err) {
        error.value = "スケジュールの取得に失敗しました。";
    } finally {
        loading.value = false;
    }
};

onMounted(loadSchedule);
</script>

<style scoped>
.dashboard-card {
    background: #ffffff; border-radius: 20px; padding: 30px;
    box-shadow: 0 8px 30px rgba(17, 43, 56, 0.1);
    border: 12px solid #113643;
    max-width: 600px;
}
.desc { color: #666; font-size: 14px; margin-bottom: 20px; }

/* 概要パネル */
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 30px; }
.stat-box {
    background: #f4f7f6; padding: 15px; border-radius: 8px; text-align: center;
}
.stat-label { display: block; font-size: 12px; color: #555; margin-bottom: 5px; font-weight: bold; }
.stat-value { font-size: 20px; font-weight: bold; color: #113643; }

/* テトリス型グラフ */
.tetris-chart { margin-top: 20px; padding: 20px; background: #fff; }
.chart-title { font-size: 18px; color: #113643; margin-bottom: 20px; text-align: center;}
.chart-container {
    display: flex; justify-content: space-between; align-items: flex-end;
    height: 150px; border-bottom: 1px solid #ddd; padding-bottom: 10px;
    margin-bottom: 15px;
}
.bar-group { display: flex; flex-direction: column; align-items: center; width: 8%; }
.bar-wrapper {
    width: 100%; height: 130px; display: flex; flex-direction: column; justify-content: flex-end;
}
.bar { width: 100%; transition: height 0.5s ease-in-out; border-radius: 2px; }
.b2c-bar { background-color: #008992; margin-bottom: 2px; }
.b2b-bar { background-color: #173f4e; }

.time-label { margin-top: 5px; font-size: 12px; color: #888; }

/* 凡例 */
.legend { display: flex; justify-content: center; gap: 20px; font-size: 12px; color: #555; }
.legend-item { display: flex; align-items: center; gap: 5px; }
.color-box { width: 12px; height: 12px; border-radius: 2px; }
.b2b-box { background-color: #173f4e; }
.b2c-box { background-color: #008992; }

.btn-refresh {
    width: 100%; padding: 15px; background: #007a82; color: white; margin-top: 20px;
    border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: background 0.2s;
}
.btn-refresh:hover:not(:disabled) { background: #005f66; }
</style>