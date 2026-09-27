<!-- Store Reception Component -->
<template>
    <div class="card bg-light">
        <h2>【店舗スタッフ】スマート受付</h2>
        <form @submit.prevent="handleReception">
            <input v-model="ticketId" placeholder="QRデータ（例：IND-123456）" required>
            <button type="submit"> 受付完了</button>
        </form>
        <p v-if="message" class="result-msg">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { submitStoreReception } from '../../api/apiClient';

const ticketId = ref('');
const message = ref('');

const handleReception = async () => {
    const res = await submitStoreReception(ticketId.value);
    message.value = res.message;
    ticketId.value = '';
};
</script>