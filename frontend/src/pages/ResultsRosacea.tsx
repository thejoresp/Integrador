import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { ArrowLeft, AlertTriangle } from 'lucide-react';

const ResultsRosacea: React.FC = () => {
  const location = useLocation();
  const analysis = location.state?.analysis;

  if (!analysis) {
    return (
      <div className="p-8">
        <h2 className="text-xl font-bold mb-4">No hay resultado disponible</h2>
        <Link to="/">Volver al inicio</Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <Link to="/" className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6">
        <ArrowLeft className="h-5 w-5 mr-1" />
        Volver al inicio
      </Link>
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 py-6 px-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-white">Resultados del Análisis de Rosácea</h1>
          </div>
          <p className="text-blue-100 mt-2">
            Estos resultados de <span className="font-bold">rosácea</span> son indicativos y no reemplazan la opinión de un profesional.
          </p>
        </div>
        <div className="p-6">
          <pre className="bg-gray-100 p-4 rounded text-xs overflow-x-auto mb-6">
            {JSON.stringify(analysis, null, 2)}
          </pre>
          {analysis.prediccion && (
            <div className="mb-6">
              <h2 className="text-lg font-semibold mb-2 text-blue-800">Predicción de Rosácea:</h2>
              <div className="bg-blue-50 border border-blue-200 rounded p-4 text-xs text-blue-900 overflow-x-auto">
                {analysis.prediccion}
              </div>
              <div className="text-gray-500 text-xs mt-2">Probabilidades: {JSON.stringify(analysis.probabilidades)}</div>
            </div>
          )}
          <div className="flex items-start space-x-2 mb-6">
            <AlertTriangle className="h-5 w-5 text-yellow-500 flex-shrink-0 mt-0.5" />
            <p className="text-gray-600 text-sm">
              <span className="font-medium">Nota importante:</span> Este análisis de <span className="font-bold">rosácea</span> es preliminar y no constituye un diagnóstico médico. 
              Siempre consulta con un dermatólogo para una evaluación profesional.
            </p>
          </div>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h3 className="text-xl font-semibold text-blue-800 mb-3">Próximos Pasos</h3>
            <p className="text-gray-700 mb-4">
              Para un diagnóstico preciso y un plan de tratamiento personalizado, te recomendamos consultar con un dermatólogo. 
              Tu salud dermatológica es importante.
            </p>
            <button onClick={() => window.open('https://buenosaires.gob.ar/salud/hospitales-y-establecimientos-de-salud/turnos-en-hospitales-y-establecimientos-de-salud', '_blank', 'noopener,noreferrer')}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors">
              Encontrar Especialista
            </button>
          </div>
          <div className="text-center">
            <Link to="/" className="text-blue-600 hover:text-blue-800 font-medium">
              Realizar nuevo análisis
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsRosacea; 