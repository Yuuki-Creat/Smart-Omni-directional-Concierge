<!-- Store Reception Component -->
<template>
    <div class="card store-card">
        <h2>スマート受付 🙍</h2>
        <p class="description">お客様の受付QRコード（番号）を入力してください。</p>

        <!-- 受付フォーム 画面の再読み込みを防いでhandleReceptionを実行 -->
        <form @submit.prevent="handleReception" class="reception-form">
            <!-- 入力フィールドとボタン(横並び) -->
            <div class="input-group">
                <!-- :disabled="loading" で通信中は入力をブロック -->
                <input 
                    v-model="ticketId" 
                    placeholder="例：IND-123456" 
                    required 
                    :disabled="loading"
                    class="form-input"
                >
                <!-- 受付完了ボタン　通信中などは押下不可 -->
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
import { submitStoreReception } from '../../api/apiClient'; // API通信関数をインポート

const ticketId = ref('');       // お客様の受付番号を入れる箱
const message = ref('');        // 画面に表示するメッセージを入れる箱
const messageType = ref('');    // 'success' または 'error' を入れる箱
const loading = ref(false);     // 通信中かどうかのフラグ

const handleReception = async () => {
    if (!ticketId.value) return; // 空の場合は何もしない（防御的措置）

    loading.value = true;   // 通信中フラグを立てる(ボタンと入力欄をロック)
    message.value = '';

    try {
        // バックエンドAPIに受付番号を送信して処理を実行
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
/* 全体のデザイン */
.store-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 24px;
    border: 12px solid #173f4e;
    max-width: 400px;
    margin: 0 auto;
}

/* タイトルの設定 */
.store-card h2 {
    font-size: 18px;
    color: #173f4e;
    margin-bottom: 20px;
    border-bottom: 2px dotted #008992;
    padding-bottom: 10px;
    display: inline-block;
}

/* 説明文のデザイン */
.description { color: #66786d; margin-bottom: 20px; font-size: 14px; }

/* 入力欄とボタンのデザイン(横並び) */
.input-group { display: flex; gap: 10px; }

/* 入力フィールドのデザイン */
.form-input {
    flex: 1; padding: 12px; border: 2px solid #c9d8ce;
    border-radius: 8px; font-size: 16px; outline: none; transition: border-color 0.2s;
}
.form-input:focus {
    border-color: #5ba77a;
}

/* ボタンのデザイン */
.btn-submit {
    width: 100%; 
    padding: 0 24px;
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
.btn-submit:hover:not(:disabled) { background-color: #006f77; }
.btn-submit:disabled { opacity: 0.7; cursor: not-allowed; }

/* 結果メッセージのデザイン */
.result-msg { margin-top: 20px; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; }
/* 成功メッセージのデザイン */
.result-msg.success { background-color: #eaf5ee; color: #2c4234; border: 1px solid #c9d8ce; }
/* エラーメッセージのデザイン */
.result-msg.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
</style>