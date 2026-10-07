<!-- Individual Check-in UI -->
<template>
    <div class="card individual-card">
        <h2>顧客：事前カルテの作成 📝</h2>
        <p class="desc">気になる箇所を教えてください。</p>
        <!-- ticketId（受付番号）がない場合は入力フォームを表示 -->
        <form @submit.prevent="handleSubmit" v-if="!ticketId" class="calte-form">
            <!-- 1. 服の種類を選択 -->
            <div class="form-group">
                <label>お預かり品（主な種類） <span class="required">*</span></label>
                <select v-model="form.clothing_type" class="form-control" required>
                    <option value="" disabled>選択してください</option>
                    <option value="スーツ上下">スーツ上下</option>
                    <option value="ワイシャツ">ワイシャツ</option>
                    <option value="コート・アウター">コート・アウター</option>
                    <option value="ワンピース">ワンピース</option>
                    <option value="その他">その他（一般衣類）</option>
                </select>
            </div>

            <!-- 2. 要望 -->
            <div class="form-group">
                <label>気になる箇所（任意）</label>
                <input type="text" v-model="form.requests" placeholder="例：襟の汚れ、袖のシミなど" class="form-input">
            </div>

            <!-- 3. 点数（着数）を入力 -->
            <div class="form-group">
                <label>お預かり点数</label>
                <div class="number-input-group">
                    <input 
                        type="number" 
                        v-model.number="form.quantity" 
                        class="form-input short-input" 
                        min="1" 
                        max="50"
                        required
                    >
                    <span class="unit">点</span>
                </div>
            </div>
            <!-- 4. ご来店予定時間を選択 -->
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
                    <!-- サーバーから取得した受付番号を表示 -->
                    <span class="qr-text">{{ ticketId }}</span>
                </div>
            </div>
            <p></p>
            <button @click="resetForm" class="btn-secondary">最初に戻る</button>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { submitIndividualCheckin } from '../../api/apiClient'; // API通信関数をインポート

// 入力データを入れる箱（リアクティブ＝画面と連動する変数）
const form = reactive({
    clothing_type: '',
    requests: '',
    quantity: 1,
    visit_time: 'オフピーク',
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

        // 例: res.ticket_id や res.data.ticket_id にデータが入っているかチェック
        const receivedTicketId = res.ticket_id || (res.data && res.data.ticket_id);

        if (receivedTicketId) {
            ticketId.value = receivedTicketId; // 成功画面に切り替え
        } else {
            // 受付番号が空っぽだった場合はエラーを表示
            throw new Error("受付番号が取得できませんでした。");
        }

    } catch (error) {
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
    form.clothing_type = '';
    form.requests = '';
    form.quantity = 1;
    form.visit_time = 'オフピーク';
    errorMessage.value = '';
};
</script>

<!-- 個人受付UIのカードデザイン -->
<style scoped>
/* カード全体デザイン */
.individual-card {
    background: #ffffff;
    border-radius: 24px;
    padding: 30px;
    border: 12px solid #173f4e;
    max-width: 400px;
    margin: 0 auto;
}

/* タイトルの設定 */
.individual-card h2 {
    font-size: 18px;
    color: #173f4e;
    margin-bottom: 20px;
    border-bottom: 2px dotted #008992;
    padding-bottom: 10px;
    display: inline-block;
}

/* フォーム全体の間隔設定 */
.karte-form {
    display: flex;
    flex-direction: column;
    gap: 15px; /* 項目間の余白 */
}

/* 入力項目の文字設定 */
.form-group { text-align: left; }
.form-group label { 
    display: block; 
    font-size: 12px; 
    color: #555; 
    margin-bottom: 6px; 
}

/* テキストやセレクトボックスの共通デザイン */
.form-input {
    width: 100%; 
    padding: 14px; 
    border-radius: 8px;
    border: none; 
    background-color: #f4f7f6; 
    font-size: 14px; 
    color: #333; 
    outline: none; 
    box-sizing: border-box;
}
/* フォーカス時のデザイン */
.form-input:focus {
    box-shadow: 0 0 0 2px #008992;
}

/* 数値入力欄のデザイン */
.number-input-group {
    display: flex;
    align-items: center;
    gap: 10px;
}
.short-input {
    width: 80px;
}
.unit {
    font-size: 14px;
    color: #333;
}

/* 送信ボタンのデザイン */
.btn-submit {
    width: 100%; 
    padding: 16px;
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

/* エラーメッセージのデザイン */
.error-msg {
    color: #d9534f; background-color: #f2dede;
    padding: 10px; border-radius: 4px; font-size: 14px;
}

/* 成功画面 */
.success-box { text-align: center; padding: 20px 0; }
.qr-mock-container {
    background: #f4f7f6;
    padding: 20px; border-radius: 12px; display: inline-block;
    margin: 20px 0; border: 2px dashed #008992;
}
.qr-mock {
    width: 150px; height: 150px; background: #fff;
    border: 8px solid #173f4e; display: flex; align-items: center; justify-content: center;
}
.qr-text { font-weight: bold; font-size: 18px; color: #333; word-break: break-all; }

/* 最初に戻るボタン */
.btn-secondary {
    padding: 8px 16px; background-color: #666; color: white;
    border: none; border-radius: 4px; cursor: pointer;
}
</style>