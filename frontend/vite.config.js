import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    watch: {
      usePolling: true
    }
  }, 
  devServer: {
    proxy: 'http://localhost:8000'
  }
})
