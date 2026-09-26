<!-- Corporate Status Check UI -->
<template>
    <div class="card">
        <h2>【法人のお客様】ステータス確認</h2>
        <div v-if="statusData">
            <p>工場お預かり中（洗浄中）:<strong>{{ statusData.uniforms_in_factory }}着</strong></p>
            <p>次回納品予定日: <strong>{{ statusData.next_delivery_date }}</strong></p>
        </div>
        <button @click="loadStatus">最新情報を取得</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { fetchCorporateStatus } from '../../api/apiClient';

const statusData = ref(null);

const loadStatus = async () => {
    const res = await fetchCorporateStatus('CORP_001');
    statusData.value = res.data;
};
</script>
