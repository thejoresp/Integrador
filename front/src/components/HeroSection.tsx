import React from 'react';

const HeroSection: React.FC = () => {
  return (
    <div className="bg-gradient-to-b from-blue-50 to-white dark:from-gray-800 dark:to-gray-900 py-12 sm:py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-gray-100 mb-4">
          Detecta y Aprende sobre Condiciones de la Piel
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Analiza tu piel con inteligencia artificial o conoce más sobre las condiciones
          comunes de la piel y cómo prevenirlas.
        </p>
      </div>
    </div>
  );
};

export default HeroSection;