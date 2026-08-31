module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        neon: '#39ff14',
        midnight: '#0b0f14',
        panel: '#111827'
      },
      boxShadow: {
        neon: '0 0 12px rgba(57,255,20,0.25), 0 0 24px rgba(57,255,20,0.12)'
      }
    }
  },
  plugins: []
}
