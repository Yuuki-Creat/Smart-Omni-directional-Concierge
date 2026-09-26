// ビルドツール（Vite）が正しくVueをコンパイルするための設定ファイル
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
  }
})