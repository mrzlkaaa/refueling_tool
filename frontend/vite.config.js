import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    watch: {
      usePolling: true
    },
    // proxy: {
    //   "/add-refuel":{
    //     target: "http://localhost:3000",
    //     changeOrigin:true,
    //     secure: false,
    //   },
    // }
  }, 
  devServer: {
    proxy: 'http://localhost:8000'
  }
})
