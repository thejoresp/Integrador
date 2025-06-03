import React from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle, Thermometer, Sun, Crosshair, Droplets, Flame } from 'lucide-react';

interface SkinCondition {
  id: string;
  icon: React.ReactNode;
  title: string;
  description: string;
  image: string;
}

const skinConditions: SkinCondition[] = [
  {
    id: 'acne',
    icon: <AlertCircle className="h-6 w-6" />,
    title: 'Acné',
    description: 'El acné es una condición común que ocurre cuando los folículos pilosos se obstruyen con grasa y células muertas de la piel.',
    image: 'https://images.pexels.com/photos/10004287/pexels-photo-10004287.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
  },
  {
    id: 'rosacea',
    icon: <Thermometer className="h-6 w-6" />,
    title: 'Rosácea',
    description: 'La rosácea es una afección crónica que causa enrojecimiento y vasos sanguíneos visibles en la cara.',
    image: 'https://images.pexels.com/photos/1138531/pexels-photo-1138531.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
  },
  {
    id: 'sunspots',
    icon: <Sun className="h-6 w-6" />,
    title: 'Manchas Solares',
    description: 'Las manchas solares son áreas de la piel que se oscurecen debido a la exposición al sol.',
    image: 'https://images.pexels.com/photos/7479603/pexels-photo-7479603.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
  },
  {
    id: 'moles',
    icon: <Crosshair className="h-6 w-6" />,
    title: 'Lunares',
    description: 'Los lunares son áreas pequeñas de pigmentación en la piel. La mayoría son inofensivos, pero es importante monitorearlos.',
    image: 'https://images.pexels.com/photos/8058606/pexels-photo-8058606.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
  },
  {
    id: 'urticaria',
    icon: <Droplets className= "h-6 w-6" />,
    title: 'Urticaria',
    description: 'La urticaria causa ronchas elevadas, rojas o de color piel, que aparecen repentinamente y causan picazón intensa.',
    image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/EMminor2010.JPG/1200px-EMminor2010.JPG',
  },
  {
    id: 'quemaduras',
    icon: <Flame className= "h-6 w-6" />,
    title: 'Quemaduras',
    description: 'Las quemaduras son lesiones en la piel causadas por calor, electricidad, productos químicos, fricción o radiación.',
    image: 'https://upload.wikimedia.org/wikipedia/commons/8/87/Hand2ndburn.jpg',
  },
];

const ConditionsOverview: React.FC = () => {
  return (
    <div className="py-10">
      <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">Condiciones Comunes de la Piel</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {skinConditions.map((condition) => (
          <Link 
            key={condition.id}
            to={`/conditions/${condition.id}`}
            className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
          >
            <div className="h-48 overflow-hidden">
              <img 
                src={condition.image} 
                alt={condition.title}
                className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
              />
            </div>
            <div className="p-5">
              <div className="flex items-center mb-2">
                <div className="text-blue-600 mr-2">
                  {condition.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900">{condition.title}</h3>
              </div>
              <p className="text-gray-600">{condition.description}</p>
              <div className="mt-4 text-blue-600 font-medium flex items-center">
                Más información
                <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </Link>
        ))}
      </div>
      
      <div className="mt-12 bg-blue-50 rounded-xl p-6 border border-blue-100">
        <div className="flex items-center justify-center text-blue-800 mb-4">
          <svg className="w-8 h-8 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="text-xl font-semibold">¿Tienes una preocupación específica?</h3>
        </div>
        <p className="text-blue-700 text-center">
          Consulta con un dermatólogo profesional para un diagnóstico preciso.
        </p>
        <div className="mt-4 flex justify-center">
          <button onClick={() => window.open('https://buenosaires.gob.ar/salud/hospitales-y-establecimientos-de-salud/turnos-en-hospitales-y-establecimientos-de-salud', '_blank', 'noopener,noreferrer')} 
          className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors font-medium">
            Más Info
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConditionsOverview;