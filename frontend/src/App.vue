<!-- App Component(main) -->
<template>
  <div id="app-container">
    <header class="app-header">
      <!-- ヘッダー内容 -->
      <h1>Smart-Omni-directional-Concierge</h1>
      <p class="subtitle">〜 お客様の感動と、業務平準化のハイブリッド基盤 〜</p>
      
      <!-- ロール（役割）切り替え用のナビゲーション -->
      <nav class="role-nav">
        <!-- 画面切り替えボタン viewsをループしてボタンを生成 -->
        <button 
          v-for="(view, key) in views" 
          :key="key"
          :class="{ active: currentView === key }"
          @click="currentView = key"
        >
          {{ view.label }}
          <!-- 選ばれている画面のボタンにだけ 'active' クラスを付けて青くする -->
          <!-- クリックされたら、currentView の中身をその画面のキーに書き換える -->
        </button>
      </nav>
    </header>
    <!-- 画面表示領域 -->
    <main class="app-main">
      <!-- 選択されたロールのコンポーネントを動的に表示 -->
      <!-- 画面を切り替えても入力データは保持 -->
      <KeepAlive>
        <component :is="views[currentView].component" />
      </KeepAlive>
    </main>
  </div>
</template>

<script setup>
import { ref, markRaw } from 'vue'

// 4つのロールに応じたコンポーネントをインポート
import IndividualUI from './components/client/IndividualUI.vue'
import CorporateUI from './components/client/CorporateUI.vue'
import StoreRecp from './components/staff/StoreRecp.vue'
import FactoryDash from './components/staff/FactoryDash.vue'

// 画面（ビュー）の定義とラベル付け
// ※markRawを使うことで、Vueの監視オーバーヘッドを減らしパフォーマンスを向上
const views = {
  individual: { label: '👤 個人のお客様 (B2C)', component: markRaw(IndividualUI) },
  corporate:  { label: '🏢 法人のお客様 (B2B)', component: markRaw(CorporateUI) },
  store:      { label: '🏪 店舗スタッフ受付',   component: markRaw(StoreRecp) },
  factory:    { label: '🏭 工場稼働ダッシュボード', component: markRaw(FactoryDash) }
}

// 初期表示の画面を設定
const currentView = ref('individual')
</script>

<style>
/* 共通ベースデザイン */
body {
  background-color: #f7f9fc;
  color: #4a4a4a;
  font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
  margin: 0;
  padding: 0;
}
/* 共通カードデザイン */
.card {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
  max-width: 500px;
  margin: 0 auto;
}
</style>

<style scoped>
/* 全体幅と中央寄せ */
#app-container { max-width: 800px; margin: 0 auto; padding: 20px 0; }

/* ヘッダーのデザイン */
.app-header { text-align: center; margin-bottom: 30px; }
.app-header h1 { color: #2c3e50; font-size: 26px; margin: 0 0 8px 0; }
.subtitle { color: #7f8c8d; font-size: 15px; margin: 0; }

/* 切替ボタンの設定 */
.role-nav { display: flex; justify-content: center; gap: 12px; margin-top: 25px; flex-wrap: wrap; }
/* 切替ボタンのデザイン */
.role-nav button {
  padding: 12px 20px;
  border: none;
  background-color: #edf2f7;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  color: #718096;
  font-size: 14px;
  transition: all 0.3s ease;
}
/* ボタンにマウスを乗せたときの設定 */
.role-nav button:hover { background-color: #e2e8f0; transform: translateY(-1px); }
/* 選択中ボタンのデザイン */
.role-nav button.active {
  background-color: #4a90e2;
  color: white;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
}
</style>