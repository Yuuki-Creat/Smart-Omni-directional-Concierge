<!-- Individual Check-in UI -->
<template>
    <div class="card">
        <h2>【個人のお客様】事前カルテ発行</h2>
        <form @submit.prevent="handleSubmit" v-if="!ticketId">
            <label>ご来店予定 </label>
            <select v-model="form.visit_time">
                <option value="混雑">通常（土日・夕方）</option>
                <option value="オフピーク">平日 13:00~15:00（500pt還元）</option>
            </select>
            <button type="submit" :disabled="loading">QRコード発行</button>
        </form>
        <div v-else class="success-box">
            <h3>受付QRコード</h3>
            <div class="qr-mock">{{ ticketId }}</div>
            <p>店舗でこの画面をご提示ください。</p>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { submitIndividualCheckin } from '../../api/apiClient';

const form = reactive({
    visit_time: '混雑',
});
const loading = ref(false);
const ticketId = ref('');

const handleSubmit = async () => {
    loading.value = true;
    const res = await submitIndividualCheckin(form);
    if(res.status === 'success') ticketId.value = res.ticket_id;
    loading.value = false;
};
</script>
