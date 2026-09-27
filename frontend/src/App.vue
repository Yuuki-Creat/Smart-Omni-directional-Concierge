<!-- App Component(main) -->
<template>
  <div id="app-container">
    <header class="app-header">
      <h1>Smart-Omni-directional-Concierge</h1>
      <p class="subtitle">〜 お客様の感動と、業務平準化のハイブリッド基盤 〜</p>
      
      <!-- ロール（役割）切り替え用のナビゲーション -->
      <nav class="role-nav">
        <button 
          v-for="(view, key) in views" 
          :key="key"
          :class="{ active: currentView === key }"
          @click="currentView = key"
        >
          {{ view.label }}
        </button>
      </nav>
    </header>

    <main class="app-main">
      <!-- 選択されたロールのコンポーネントを動的に表示 -->
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
// ※markRawを使うことで、Vueの監視オーバーヘッドを減らしパフォーマンスを上げます
const views = {
  individual: { label: '👤 個人のお客様 (B2C)', component: markRaw(IndividualUI) },
  corporate:  { label: '🏢 法人のお客様 (B2B)', component: markRaw(CorporateUI) },
  store:      { label: '🏪 店舗スタッフ受付',   component: markRaw(StoreRecp) },
  factory:    { label: '🏭 工場稼働ダッシュボード', component: markRaw(FactoryDash) }
}

// 初期表示の画面を設定（デモ時はここを切り替えて見せます）
const currentView = ref('individual')
</script>

<style scoped>
/* 画面全体の背景を薄緑に設定 */
:global(body) {
  margin: 0;
  background-color: #f2f7f4;
}

#app-container {
  max-width: 800px;
  margin: 0 auto;
  padding-top: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #333;
}

.app-header {
  text-align: center;
  padding: 20px 0;
  border-bottom: 2px solid #e0e8e3;
  margin-bottom: 30px;
}

.app-header h1 {
  margin: 0;
  color: #2c4234;
  font-size: 24px;
}

.subtitle {
  color: #66786d;
  font-size: 14px;
  margin-top: 5px;
}

.role-nav {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.role-nav button {
  padding: 10px 15px;
  border: 1px solid #ccc;
  background-color: #ffffff;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  color: #555;
  transition: all 0.2s ease;
}

.role-nav button:hover {
  background-color: #eaf5ee;
}

.role-nav button.active {
  background-color: #5ba77a;
  color: white;
  border-color: #5ba77a;
  box-shadow: 0 4px 6px rgba(91, 167, 122, 0.2);
}

.app-main {
  padding: 0 20px;
  padding-bottom: 40px;
}
</style>