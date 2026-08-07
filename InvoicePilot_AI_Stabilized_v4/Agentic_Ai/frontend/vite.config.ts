// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [react()],
// })

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // IMPORTANT: this must match your repo name for GitHub Pages project sites.
  // Your repo is "hackathon", so the site will live at:
  // https://Aditya-hope.github.io/hackathon/
  base: '/hackathon/',
})
