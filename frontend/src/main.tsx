import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './app/App.tsx'
import './index.css'
import { Buffer } from 'buffer'

// Polyfill para o Buffer, necessário para o plotly.js no Vite
window.Buffer = Buffer;

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
