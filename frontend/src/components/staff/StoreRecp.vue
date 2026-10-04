<!-- Store Reception Component -->
<template>
    <div class="card store-card">
        <h2>スマート受付 🙍</h2>
        <p class="description">お客様の受付QRコード（番号）を入力してください。</p>

        <form @submit.prevent="handleReception" class="reception-form">
            <div class="input-group">
                <!-- :disabled="loading" で通信中は入力をブロック -->
                <input 
                    v-model="ticketId" 
                    placeholder="例：IND-123456" 
                    required 
                    :disabled="loading"
                    class="form-input"
                >
                <button type="submit" class="btn-submit" :disabled="loading || !ticketId">
                    {{ loading ? '処理中...' : '受付完了' }}
                </button>
            </div>
        </form>

        <!-- メッセージの表示（成功時は緑、エラー時は赤になるようクラスを切り替え） -->
        <div v-if="message" class="result-msg" :class="messageType">
            {{ message }}
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { submitStoreReception } from '../../api/apiClient';

const ticketId = ref('');
const message = ref('');
const messageType = ref(''); // 'success' または 'error' を入れる箱
const loading = ref(false);  // 通信中かどうかのフラグ

const handleReception = async () => {
    if (!ticketId.value) return; // 空の場合は何もしない（防御的措置）

    loading.value = true;
    message.value = '';

    try {
        const res = await submitStoreReception(ticketId.value);

        messageType.value = 'success';
        message.value = res.message || `${ticketId.value} のお預かりを完了しました。`;
        ticketId.value = ''; // 次の人のために入力欄を空にする

    } catch (error) {
        // 例外（エラー）が発生した時の処理
        console.error("受付エラー:", error);
        messageType.value = 'error';
        message.value = "通信エラーが発生しました。番号を確認して再度お試しください。";
    } finally {
        // 必ず最後にローディング状態を解除する
        loading.value = false;
    }
};
</script>

<style scoped>
.store-card {
    background: #ffffff; border-radius: 12px; padding: 24px;
    box-shadow: 0 4px 15px rgba(91, 167, 122, 0.08);
}
.description { color: #66786d; margin-bottom: 20px; font-size: 14px; }

.input-group { display: flex; gap: 10px; }
.form-input {
    flex: 1; padding: 12px; border: 2px solid #c9d8ce;
    border-radius: 8px; font-size: 16px; outline: none; transition: border-color 0.2s;
}
.form-input:focus {
    border-color: #5ba77a;
}

.btn-submit {
    padding: 0 24px; background-color: #5ba77a; color: white;
    border: none; border-radius: 8px; font-weight: bold; cursor: pointer; white-space: nowrap;
}
.btn-submit:hover:not(:disabled) { background-color: #4a8e65; }
.btn-submit:disabled { background-color: #a8d1b8; cursor: not-allowed; }

.result-msg { margin-top: 20px; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; }
.result-msg.success { background-color: #eaf5ee; color: #2c4234; border: 1px solid #c9d8ce; }
.result-msg.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
</style>