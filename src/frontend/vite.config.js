import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: { //when I do a request to the django's backend, I need to use the proxy, becuase otherwise I'd fetch data from the frontend's server
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/polls',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    },
    crossOriginIsolated: true, //this is needed for the axios requests to work properly
  },
})
