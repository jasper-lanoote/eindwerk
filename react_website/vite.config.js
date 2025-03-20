import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Luister naar alle netwerken
    port: 3000,        // Poortnummer (standaard 3000)
  },
})
