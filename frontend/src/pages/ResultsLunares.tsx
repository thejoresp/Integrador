import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, AlertTriangle } from 'lucide-react';

const Results: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState<any | null>(null);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetch(`${API_URL}/skin/api/analyze-lunares/${id}`)
      .then(res => res.json())
      .then(setAnalysis)
      .catch(() => setAnalysis({ error: 'No se pudo obtener el resultado.' }))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8 flex flex-col items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-600 mb-4"></div>
        <h2 className="text-xl font-semibold text-gray-700">Analizando resultados...</h2>
        <p className="text-gray-500 mt-2">Esto puede tomar unos momentos</p>
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
            <h1 className="text-2xl font-bold text-white">Resultados del Análisis de Lunares</h1>
            <div className="bg-white bg-opacity-20 text-white px-3 py-1 rounded-full text-sm">
              ID: {id}
            </div>
          </div>
          <p className="text-blue-100 mt-2">
            Estos resultados de <span className="font-bold">lunares</span> son indicativos y no reemplazan la opinión de un profesional.
          </p>
        </div>
        <div className="p-6">
          {analysis && (
            <>
              <pre className="bg-gray-100 p-4 rounded text-xs overflow-x-auto mb-6">
                {JSON.stringify(analysis, null, 2)}
              </pre>
              {analysis.prediccion && (
                <div className="mb-6">
                  <h2 className="text-lg font-semibold mb-2 text-blue-800">Predicción de Lunares:</h2>
                  <div className="bg-blue-50 border border-blue-200 rounded p-4 text-xs text-blue-900 overflow-x-auto">
                    {analysis.prediccion}
                  </div>
                  <div className="text-gray-500 text-xs mt-2">Probabilidades: {JSON.stringify(analysis.probabilidades)}</div>
                </div>
              )}
            </>
          )}
          <div className="flex items-start space-x-2 mb-6">
            <AlertTriangle className="h-5 w-5 text-yellow-500 flex-shrink-0 mt-0.5" />
            <p className="text-gray-600 text-sm">
              <span className="font-medium">Nota importante:</span> Este análisis de <span className="font-bold">lunares</span> es preliminar y no constituye un diagnóstico médico. 
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

export default Results;