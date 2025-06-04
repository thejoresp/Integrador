import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, AlertCircle, Thermometer, Sun, Crosshair, Droplets, Flame } from 'lucide-react';

// Mocked condition data - in a real application, this would come from an API
const conditionsData = {
  acne: {
    title: 'Acné',
    icon: <AlertCircle className="h-6 w-6" />,
    description: 'El acné es una condición común que ocurre cuando los folículos pilosos se obstruyen con grasa y células muertas de la piel.',
    causes: [
      'Producción excesiva de grasa (sebo)',
      'Acumulación de células muertas de la piel',
      'Bacterias (Propionibacterium acnes)',
      'Inflamación',
      'Factores hormonales',
      'Predisposición genética'
    ],
    symptoms: [
      'Espinillas (comedones cerrados)',
      'Puntos negros (comedones abiertos)',
      'Pápulas (bultos rojos pequeños)',
      'Pústulas (pápulas con pus en la punta)',
      'Nódulos (lesiones grandes, dolorosas bajo la piel)',
      'Quistes (lesiones dolorosas llenas de pus)'
    ],
    treatment: [
      'Limpiadores con ácido salicílico o peróxido de benzoilo',
      'Retinoides tópicos',
      'Antibióticos tópicos u orales',
      'Medicamentos hormonales (para mujeres)',
      'Isotretinoína (para casos severos)',
      'Procedimientos dermatológicos (extracciones, peelings)'
    ],
    prevention: [
      'Lavar el rostro dos veces al día',
      'Usar productos no comedogénicos',
      'Evitar tocar o exprimir las lesiones',
      'Mantener el cabello limpio y apartado del rostro',
      'Seguir una dieta equilibrada',
      'Controlar el estrés'
    ],
    image: 'https://images.pexels.com/photos/10004287/pexels-photo-10004287.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
  },
  rosacea: {
    title: 'Rosácea',
    icon: <Thermometer className="h-6 w-6" />,
    description: 'La rosácea es una afección crónica que causa enrojecimiento y vasos sanguíneos visibles en la cara, a veces con pequeños bultos rojos llenos de pus.',
    causes: [
      'Predisposición genética',
      'Problemas con los vasos sanguíneos faciales',
      'Ácaros microscópicos (Demodex)',
      'Bacterias intestinales (H. pylori)',
      'Desencadenantes ambientales'
    ],
    symptoms: [
      'Enrojecimiento persistente en el centro de la cara',
      'Vasos sanguíneos dilatados visibles',
      'Bultos rojos (pápulas) y pústulas',
      'Sensación de ardor o escozor',
      'Piel sensible y reactiva',
      'Engrosamiento de la piel nasal (rinofima)'
    ],
    treatment: [
      'Medicamentos tópicos (metronidazol, ácido azelaico)',
      'Antibióticos orales',
      'Isotretinoína (casos severos)',
      'Terapias con láser o luz pulsada',
      'Evitar desencadenantes conocidos'
    ],
    prevention: [
      'Usar protector solar diariamente',
      'Evitar extremos de temperatura',
      'Evitar alimentos y bebidas desencadenantes',
      'Usar productos para piel sensible',
      'Mantener una buena rutina de cuidado facial'
    ],
    image: 'https://images.pexels.com/photos/1138531/pexels-photo-1138531.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
  },
  sunspots: {
    title: 'Manchas Solares',
    icon: <Sun className="h-6 w-6" />,
    description: 'Las manchas solares son áreas de la piel que se oscurecen debido a la exposición al sol, también conocidas como hiperpigmentación o lentigos solares.',
    causes: [
      'Exposición excesiva a rayos UV',
      'Envejecimiento natural',
      'Predisposición genética',
      'Hormonas (melasma)'
    ],
    symptoms: [
      'Manchas planas de color marrón, gris o negro',
      'Aparecen en áreas expuestas al sol (cara, manos, brazos)',
      'No duelen ni pican',
      'Pueden aumentar con el tiempo sin protección'
    ],
    treatment: [
      'Cremas despigmentantes (hidroquinona, retinoides)',
      'Ácidos (glicólico, kójico, láctico)',
      'Procedimientos dermatológicos (peelings químicos)',
      'Tratamientos con láser',
      'Crioterapia'
    ],
    prevention: [
      'Usar protector solar SPF 30+ diariamente',
      'Evitar la exposición solar entre 10am y 4pm',
      'Usar sombreros, gafas y ropa protectora',
      'Aplicar antioxidantes tópicos (vitamina C)',
      'Evitar camas de bronceado'
    ],
    image: 'https://images.pexels.com/photos/7479603/pexels-photo-7479603.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
  },
  moles: {
    title: 'Lunares',
    icon: <Crosshair className="h-6 w-6" />,
    description: 'Los lunares son áreas pequeñas de pigmentación en la piel. La mayoría son inofensivos, pero es importante monitorearlos para detectar cambios que podrían indicar melanoma.',
    causes: [
      'Agrupaciones de células pigmentadas (melanocitos)',
      'Factores genéticos',
      'Exposición solar (especialmente en la infancia)',
      'Cambios hormonales'
    ],
    symptoms: [
      'Manchas de color marrón, negro o azul',
      'Pueden ser planos o elevados',
      'Generalmente redondos y simétricos',
      'Pueden aparecer en cualquier parte del cuerpo'
    ],
    treatment: [
      'La mayoría no requieren tratamiento',
      'Extirpación quirúrgica (por razones estéticas o sospecha)',
      'Biopsia para descartar melanoma'
    ],
    prevention: [
      'Protección solar para evitar la formación de nuevos lunares',
      'Autoexamen regular siguiendo la regla ABCDE',
      'Visitas anuales al dermatólogo',
      'Documentar cambios con fotografías'
    ],
    image: 'https://images.pexels.com/photos/8058606/pexels-photo-8058606.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
  },
  urticaria: {
    title: 'Urticaria',
    icon: <Droplets className="h-6 w-6" />,
    description: 'La urticaria (también conocida como ronchas o habones) se caracteriza por la aparición súbita de elevaciones rojizas o del color de la piel, edematosas y pruriginosas que pueden aparecer en cualquier parte del cuerpo. Puede ser aguda (menos de 6 semanas) o crónica.',
    causes: [
      'Reacciones alérgicas a alimentos',
      'Medicamentos (antibióticos, AINEs)',
      'Picaduras de insectos',
      'Contacto con alérgenos (látex, plantas)',
      'Infecciones',
      'Estrés físico o emocional',
      'Exposición al frío o calor',
      'Enfermedades autoinmunes subyacentes'
    ],
    symptoms: [
      'Ronchas elevadas de color rojo o piel',
      'Picazón intensa',
      'Cambio de localización de las lesiones',
      'Angioedema (hinchazón de capas profundas de la piel)',
      'Resolución individual de ronchas en menos de 24 horas',
      'Recurrencia en diferentes áreas'
    ],
    treatment: [
      'ATENCIÓN: es recomendable no automedicarse previa visita con profesional.',
      'Antihistamínicos H1 no sedantes',
      'Antihistamínicos H1 sedantes para picazón nocturna',
      'Corticosteroides orales para casos severos y a corto plazo',
    ],
    prevention: [
      'Identificar y evitar desencadenantes específicos',
      'Llevar un diario para documentar episodios y posibles causas',
      'Usar productos hipoalergénicos para la piel',
      'Evitar ropa ajustada y tejidos sintéticos',
      'Manejar el estrés',
      'Considerar pulseras de alerta médica en casos severos',
      'Seguimiento médico regular en casos crónicos'
    ],
    image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/EMminor2010.JPG/1200px-EMminor2010.JPG'
  },
  quemaduras: {
    title: 'Quemaduras',
    icon: <Flame className="h-6 w-6" />,
    description: 'Las quemaduras son lesiones tisulares causadas por calor, radiación, electricidad, productos químicos o fricción. Se clasifican por su profundidad (primer, segundo o tercer grado) y extensión, lo que determina su gravedad y tratamiento.',
    causes: [
      'Exposición a llamas o fuego',
      'Líquidos calientes (escaldaduras)',
      'Contacto con superficies calientes',
      'Exposición solar excesiva',
      'Productos químicos corrosivos',
      'Electricidad',
      'Radiación'
    ],
    symptoms: [
      'Primer grado: enrojecimiento, dolor, inflamación leve',
      'Segundo grado: ampollas, dolor intenso, enrojecimiento',
      'Tercer grado: piel blanca/carbonizada, insensibilidad por daño nervioso',
      'Edema (hinchazón)',
      'Descamación de la piel en días posteriores',
      'Posibles síntomas sistémicos en quemaduras extensas'
    ],
    treatment: [
      'Enfriamiento inmediato con agua fresca (no helada) durante 10-15 minutos',
      'No aplicar hielo directamente',
      'Analgésicos para el dolor',
      'Vendajes estériles no adherentes',
      'Atención médica urgente para quemaduras graves o extensas',
    ],
    prevention: [
      'Instalar detectores de humo en el hogar',
      'Utilizar ropa de trabajo y protección adecuada al manipular o instalar circuitos eléctricos',
      'Supervisar a los niños cerca de fuentes de calor',
      'Mantener líquidos calientes fuera del alcance de niños',
      'Usar protector solar adecuado',
      'Manipular productos químicos con equipo de protección',
      'Comprobar la temperatura del agua antes del baño',
      'Mantener dispositivos eléctricos en buen estado'
    ],
    image: 'https://upload.wikimedia.org/wikipedia/commons/8/87/Hand2ndburn.jpg'
  }
};

const ConditionInfo: React.FC = () => {
  const { condition } = useParams<{ condition: string }>();
  const conditionData = condition ? conditionsData[condition as keyof typeof conditionsData] : null;
  
  if (!conditionData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 sm:px-6 lg:px-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900">Condición no encontrada</h2>
        <p className="mt-2 text-gray-600">La información sobre esta condición no está disponible.</p>
        <Link to="/" className="mt-4 inline-flex items-center text-blue-600 hover:text-blue-800">
          <ArrowLeft className="h-5 w-5 mr-1" />
          Volver al inicio
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <Link to="/" className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6">
        <ArrowLeft className="h-5 w-5 mr-1" />
        Volver al inicio
      </Link>
      
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="h-64 overflow-hidden">
          <img 
            src={conditionData.image} 
            alt={conditionData.title} 
            className="w-full h-full object-cover"
          />
        </div>
        
        <div className="p-6 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
          <div className="flex items-center mb-4">
            <div className="text-blue-600 mr-3">
              {conditionData.icon}
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{conditionData.title}</h1>
          </div>
          
          <p className="text-lg text-gray-700 dark:text-gray-300 mb-8">{conditionData.description}</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Causas</h2>
              <ul className="space-y-2">
                {conditionData.causes.map((cause, index) => (
                  <li key={index} className="flex items-start">
                    <span className="inline-flex items-center justify-center h-6 w-6 rounded-full bg-blue-100 text-blue-800 text-sm font-medium mr-3 flex-shrink-0">
                      {index + 1}
                    </span>
                    <span className="text-gray-600 dark:text-gray-300">{cause}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Síntomas</h2>
              <ul className="space-y-2">
                {conditionData.symptoms.map((symptom, index) => (
                  <li key={index} className="flex items-start">
                    <svg className="h-5 w-5 text-blue-600 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-600 dark:text-gray-300">{symptom}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Tratamiento</h2>
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-100 dark:border-blue-700 mb-6">
              <ul className="space-y-2">
                {conditionData.treatment.map((treatment, index) => (
                  <li key={index} className="flex items-start">
                    <svg className="h-5 w-5 text-blue-600 dark:text-blue-400 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span className="text-gray-700 dark:text-gray-200">{treatment}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Prevención</h2>
            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4 border border-green-100 dark:border-green-700">
              <ul className="space-y-2">
                {conditionData.prevention.map((prevention, index) => (
                  <li key={index} className="flex items-start">
                    <svg className="h-5 w-5 text-green-600 dark:text-green-400 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                    <span className="text-gray-700 dark:text-gray-200">{prevention}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="mt-10 p-6 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center mb-4">
              <svg className="h-6 w-6 text-yellow-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">Importante</h3>
            </div>
            <p className="text-gray-600 dark:text-gray-300">
              La información proporcionada es de carácter general y educativo. Siempre consulta con un dermatólogo 
              profesional para un diagnóstico preciso y un plan de tratamiento personalizado.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConditionInfo;