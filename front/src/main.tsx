import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <div className="min-h-screen">
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </div>
  </StrictMode>
);