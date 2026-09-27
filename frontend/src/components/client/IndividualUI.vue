<!-- Individual Check-in UI -->
<template>
    <div class="card">
        <h2>【個人のお客様】事前カルテ発行</h2>

        <!-- ticketId（受付番号）がない場合は入力フォームを表示 -->
        <form @submit.prevent="handleSubmit" v-if="!ticketId">
            <div class="form-group">
                <label>ご来店予定 </label>
                <select v-model="form.visit_time" class="form-select">
                    <option value="混雑">通常（土日・夕方）</option>
                    <option value="オフピーク">平日 13:00~15:00（500pt還元）</option>
                </select>
            </div>

            <!-- 通信エラーなどが起きた場合のメッセージ表示エリア -->
            <div v-if="errorMessage" class="error-msg">
                {{ errorMessage }}
            </div>

            <!-- loading中（通信中）はボタンを押せなくして、文字を変更する -->
            <button type="submit" class="btn-submit" :disabled="loading">
                {{ loading ? '通信中...' : 'QRコード発行' }}
            </button>
        </form>

        <!-- ticketId（受付番号）が取得できたら成功画面を表示 -->
        <div v-else class="success-box">
            <h3>受付完了</h3>
            <p>以下のコードを店舗でご提示ください。</p>

            <!-- QRコード風の見た目 -->
            <div class="qr-mock-container">
                <div class="qr-mock">
                    <span class="qr-text">{{ ticketId }}</span>
                </div>
            </div>

            <button @click="resetForm" class="btn-secondary">最初に戻る</button>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { submitIndividualCheckin } from '../../api/apiClient';

// 入力データを入れる箱（リアクティブ＝画面と連動する変数）
const form = reactive({
    visit_time: '混雑',
});

const loading = ref(false); // 通信中かどうかを判定するフラグ
const ticketId = ref('');   // 取得した受付番号を入れる箱
const errorMessage = ref(''); // エラーメッセージを入れる箱

const handleSubmit = async () => {
    loading.value = true;
    errorMessage.value = ''; // エラー表示をリセット

    try {
        // API（バックエンド）と通信
        const res = await submitIndividualCheckin(form);

        // 【デバッグ用】F12キーの開発者ツール（コンソール）で、実際のデータの中身を確認できます
        // console.log("バックエンドからのレスポンス:", res);

        // 例: res.ticket_id や res.data.ticket_id にデータが入っているかチェック
        const receivedTicketId = res.ticket_id || (res.data && res.data.ticket_id);

        if (receivedTicketId) {
            ticketId.value = receivedTicketId; // 番号をセット（これで画面が切り替わる）
        } else {
            // 受付番号が空っぽだった場合は意図的なエラーを起こす
            throw new Error("受付番号が取得できませんでした。");
        }

    } catch (error) {
        // try { ... } の中でエラーが起きたらここにジャンプする
        console.error("通信エラー:", error);
        errorMessage.value = "発行に失敗しました。サーバーの状況を確認してください。";
    } finally {
        // 成功しても失敗しても、最後に必ずローディング状態を解除する
        loading.value = false;
    }
};

// 画面をリセットする関数（最初からやり直すボタン用）
const resetForm = () => {
    ticketId.value = '';
    form.visit_time = '混雑';
    errorMessage.value = '';
};
</script>

<style scoped>
/* 画面をリッチに見せるためのCSS装飾 */
.form-group {
    margin-bottom: 20px;
    text-align: left;
}

.form-select {
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-size: 16px;
    margin-top: 8px;
}

.btn-submit {
    width: 100%;
    padding: 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}

.btn-submit:disabled {
    background-color: #999;
    cursor: not-allowed;
}

.error-msg {
    color: #d9534f;
    background-color: #f2dede;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
    font-size: 14px;
}

.success-box {
    text-align: center;
    padding: 20px 0;
}

.qr-mock-container {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 12px;
    display: inline-block;
    margin: 20px 0;
    border: 2px dashed #ccc;
}

.qr-mock {
    width: 150px;
    height: 150px;
    background: #fff;
    border: 8px solid #333;
    display: flex;
    align-items: center;
    justify-content: center;
}

.qr-text {
    font-weight: bold;
    font-size: 18px;
    color: #333;
    word-break: break-all;
}

.btn-secondary {
    padding: 8px 16px;
    background-color: #6c757d;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>