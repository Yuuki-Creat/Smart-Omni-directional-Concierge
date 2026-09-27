<!-- Factory Dashboard Component -->
<template>
    <div class="card">
        <h2>【工場管理者】ダッシュボード</h2>
        <div v-if="schedule">
            <div class="alert">
                現在のベースロード（法人固定枠）: <strong>{{ schedule.base_load }}枠</strong>
            </div>
            <div class="info">
                個人（保管）充当可能スロット: <strong>{{ schedule.available_slots }}枠</strong>
                <br>
                待機中の個人案件: {{ schedule.b2c_pending }}件
            </div>
            <p>システム状態: {{ schedule.status === 'stable' ? '安定' : '警告' }}</p>
        </div>
        <button @click="loadSchedule">稼働率を再計算</button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchFactorySchedule } from '../../api/apiClient';

const schedule = ref(null);
const loadSchedule = async () => {
    const res = await fetchFactorySchedule();
    schedule.value = res.data;
};

onMounted(loadSchedule);

</script>