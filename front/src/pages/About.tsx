import React from 'react';
import { Shield, Award, BarChart, Users } from 'lucide-react';

const About: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 sm:text-4xl">Sobre Piel Sana IA</h1>
        <p className="mt-3 max-w-2xl mx-auto text-lg text-gray-600 dark:text-gray-300">
          Combinando inteligencia artificial y conocimiento dermatológico para ayudarte a entender y cuidar tu piel.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-16">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Nuestra Misión</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            En Piel Sana IA, nuestra misión es democratizar el acceso a información dermatológica de calidad. 
            Creemos que todas las personas deberían tener acceso a herramientas que les ayuden a entender 
            y cuidar su piel, independientemente de su ubicación o recursos.
          </p>
          <p className="text-gray-600 dark:text-gray-300">
            A través de nuestra plataforma impulsada por inteligencia artificial, buscamos proporcionar un primer 
            análisis accesible y educativo, siempre enfatizando la importancia de la consulta con profesionales 
            de la salud para diagnósticos definitivos.
          </p>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Cómo Funciona</h2>
          <ol className="space-y-4">
            <li className="flex">
              <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                <span className="text-blue-600 font-medium">1</span>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-300">
                  <span className="font-medium text-gray-900 dark:text-gray-100">Sube una foto</span> - Captura claramente el área de la piel que te preocupa.
                </p>
              </div>
            </li>
            <li className="flex">
              <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                <span className="text-blue-600 font-medium">2</span>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-300">
                  <span className="font-medium text-gray-900 dark:text-gray-100">Procesamiento por IA</span> - Nuestro algoritmo analiza la imagen buscando patrones característicos de condiciones dermatológicas comunes.
                </p>
              </div>
            </li>
            <li className="flex">
              <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                <span className="text-blue-600 font-medium">3</span>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-300">
                  <span className="font-medium text-gray-900 dark:text-gray-100">Recibe resultados</span> - Obtendrás un informe con posibles condiciones identificadas y su probabilidad.
                </p>
              </div>
            </li>
            <li className="flex">
              <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                <span className="text-blue-600 font-medium">4</span>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-300">
                  <span className="font-medium text-gray-900 dark:text-gray-100">Recomendaciones</span> - Te proporcionamos información educativa y sugerencias para el cuidado, pero siempre recomendamos la consulta con especialistas.
                </p>
              </div>
            </li>
          </ol>
        </div>
      </div>
      
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg overflow-hidden shadow-xl mb-16">
        <div className="px-6 py-12 sm:px-12">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">Nuestros Valores</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-white bg-opacity-10 p-6 rounded-lg backdrop-blur-sm">
              <Shield className="h-10 w-10 text-white mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Privacidad</h3>
              <p className="text-blue-100">
                Protegemos tus datos personales y tu información médica con los más altos estándares de seguridad.
              </p>
            </div>
            <div className="bg-white bg-opacity-10 p-6 rounded-lg backdrop-blur-sm">
              <Award className="h-10 w-10 text-white mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Calidad</h3>
              <p className="text-blue-100">
                Nos comprometemos a proporcionar información precisa y actualizada, respaldada por evidencia científica.
              </p>
            </div>
            <div className="bg-white bg-opacity-10 p-6 rounded-lg backdrop-blur-sm">
              <BarChart className="h-10 w-10 text-white mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Innovación</h3>
              <p className="text-blue-100">
                Mejoramos constantemente nuestros algoritmos y servicios para ofrecer la mejor experiencia posible.
              </p>
            </div>
            <div className="bg-white bg-opacity-10 p-6 rounded-lg backdrop-blur-sm">
              <Users className="h-10 w-10 text-white mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Accesibilidad</h3>
              <p className="text-blue-100">
                Creemos que todos merecen acceso a información sobre salud dermatológica, sin barreras.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-8 border border-gray-200 dark:border-gray-700">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6 text-center">Preguntas Frecuentes</h2>
        <div className="space-y-6 max-w-3xl mx-auto">
          <div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">¿Es Piel Sana IA un reemplazo para la consulta médica?</h3>
            <p className="text-gray-600 dark:text-gray-300">
              No. Piel Sana IA es una herramienta educativa y de análisis preliminar que puede ayudar a identificar posibles condiciones, 
              pero no sustituye la evaluación y diagnóstico de un profesional de la salud.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">¿Qué tan preciso es el análisis?</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Nuestro sistema utiliza algoritmos avanzados de inteligencia artificial, pero la precisión puede variar según la calidad 
              de la imagen y las características de la condición. Los resultados deben considerarse como orientativos.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">¿Cómo se protege mi privacidad?</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Todas las imágenes se procesan con estrictos protocolos de seguridad y privacidad. No compartimos tus datos con terceros 
              y puedes solicitar la eliminación de tu información en cualquier momento.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">¿Qué debo hacer después de recibir mi análisis?</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Te recomendamos revisar la información educativa proporcionada, seguir las recomendaciones generales para el cuidado de 
              la piel y, especialmente si se detecta una alta probabilidad de alguna condición, consultar con un dermatólogo.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;