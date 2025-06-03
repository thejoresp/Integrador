import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Results from './pages/Results';
import ConditionInfo from './pages/ConditionInfo';
import About from './pages/About';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="results" element={<Results />} />
        <Route path="results/:id" element={<Results />} />
        <Route path="conditions/:condition" element={<ConditionInfo />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  );
}

export default App;