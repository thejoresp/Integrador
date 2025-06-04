import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { AlertTriangle, Check, AlertCircle, Thermometer, Sun, Crosshair, ArrowLeft } from 'lucide-react';

// Mocked skin analysis results
interface AnalysisResult {
  condition: string;
  probability: number;
  icon: React.ReactNode;
  description: string;
  recommendations: string[];
  color: string;
}

const Results: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState<AnalysisResult[]>([]);
  const [analysis, setAnalysis] = useState<any>(null);

  // Mock analysis results - in real app, this would come from API
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setResults([
        {
          condition: 'Acné',
          probability: 85,
          icon: <AlertCircle className="h-6 w-6" />,
          description: 'Detección de posible acné. Se observan signos de inflamación y puntos blancos/negros.',
          recommendations: [
            'Lavar el rostro dos veces al día con un limpiador suave',
            'Usar productos con ácido salicílico o peróxido de benzoilo',
            'Evitar tocar o exprimir las lesiones',
            'Consultar a un dermatólogo para tratamiento específico'
          ],
          color: 'red'
        },
        {
          condition: 'Rosácea',
          probability: 15,
          icon: <Thermometer className="h-6 w-6" />,
          description: 'Baja probabilidad de rosácea. Se detecta ligero enrojecimiento facial.',
          recommendations: [
            'Utilizar protector solar diario',
            'Evitar alimentos y bebidas desencadenantes (alcohol, picante)',
            'Utilizar productos suaves para la piel'
          ],
          color: 'yellow'
        },
        {
          condition: 'Manchas Solares',
          probability: 40,
          icon: <Sun className="h-6 w-6" />,
          description: 'Presencia moderada de hiperpigmentación posiblemente relacionada con exposición solar.',
          recommendations: [
            'Aplicar protector solar SPF 50+ diariamente',
            'Usar gorra/sombrero y lentes de sol al estar expuesto al sol',
            'Considerar productos con vitamina C o niacinamida'
          ],
          color: 'orange'
        },
        {
          condition: 'Lunares',
          probability: 10,
          icon: <Crosshair className="h-6 w-6" />,
          description: 'Se detectan algunos lunares regulares que parecen normales.',
          recommendations: [
            'Monitorear cambios en tamaño, color o forma',
            'Realizar autoexámenes mensuales',
            'Visitar al dermatólogo para evaluación anual'
          ],
          color: 'green'
        }
      ]);
      setAnalysis({
        embeddings: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        embedding_shape: [20]
      });
      setLoading(false);
    }, 1000);
  }, [id]);

  const getStatusColor = (probability: number): string => {
    if (probability >= 70) return 'text-red-600 bg-red-100';
    if (probability >= 40) return 'text-orange-600 bg-orange-100';
    return 'text-green-600 bg-green-100';
  };

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
            <h1 className="text-2xl font-bold text-white">Resultados del Análisis</h1>
            <div className="bg-white bg-opacity-20 text-white px-3 py-1 rounded-full text-sm">
              ID: {id}
            </div>
          </div>
          <p className="text-blue-100 mt-2">
            Estos resultados son indicativos y no reemplazan la opinión de un profesional.
          </p>
        </div>
        
        <div className="p-6">
          <div className="flex items-start space-x-2 mb-6">
            <AlertTriangle className="h-5 w-5 text-yellow-500 flex-shrink-0 mt-0.5" />
            <p className="text-gray-600 text-sm">
              <span className="font-medium">Nota importante:</span> Este análisis es preliminar y no constituye un diagnóstico médico. 
              Siempre consulta con un dermatólogo para una evaluación profesional.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {results.map((result, index) => (
              <div key={index} className="border rounded-lg overflow-hidden">
                <div className={`p-4 flex items-center justify-between ${getStatusColor(result.probability)}`}>
                  <div className="flex items-center">
                    {result.icon}
                    <h3 className="ml-2 font-semibold">{result.condition}</h3>
                  </div>
                  <div className="text-sm font-medium">
                    Probabilidad: {result.probability}%
                  </div>
                </div>
                <div className="p-4">
                  <p className="text-gray-700 mb-3">{result.description}</p>
                  <h4 className="font-medium text-gray-900 mb-2">Recomendaciones:</h4>
                  <ul className="space-y-1">
                    {result.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start">
                        <Check className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-600">{rec}</span>
                      </li>
                    ))}
                  </ul>
                  <div className="mt-4">
                    <Link 
                      to={`/conditions/${result.condition.toLowerCase()}`}
                      className="text-blue-600 hover:text-blue-800 font-medium inline-flex items-center"
                    >
                      Más información
                      <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
                  </div>
                </div>
              </div>
            ))}
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