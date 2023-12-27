import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
  // Custom plugin to load markdown files
  {
    name: "markdown-loader",
    transform(code, id) {
      if (id.slice(-3) === ".md") {
        // For .md files, get the raw content
        return `export default ${JSON.stringify(code)};`;
      }
    }
  }
  ],
})
