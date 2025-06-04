import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Upload, X, Image as ImageIcon } from 'lucide-react';

const ConsentModal: React.FC<{ onAccept: () => void; onClose: () => void }> = ({ onAccept, onClose }) => {
  const [checked, setChecked] = useState(false);
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Consentimiento</h2>
          <div className="prose prose-sm">
            <h3 className="text-lg font-semibold mb-2">📄 Consentimiento Informado para el Tratamiento de Datos Faciales</h3>
            <p>
              Piel Sana IA te informa que, para poder analizar tu imagen, necesitamos tu consentimiento para el tratamiento de datos personales sensibles, conforme a la Ley N.º 25.326 de Protección de Datos Personales y normativa aplicable.
            </p>
            <h4 className="font-semibold mt-4 mb-2">¿Para qué se usan tus datos?</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Promover el bienestar, autocuidado y prevención de problemas dermatológicos.</li>
              <li>Brindar información orientativa sobre el estado de tu piel y posibles condiciones frecuentes.</li>
              <li>Facilitar el acceso a herramientas de salud para todas las personas, sin distinción.</li>
            </ul>
            <h4 className="font-semibold mt-4 mb-2">¿Qué datos se procesan?</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Imágenes faciales que subas para el análisis.</li>
              <li>Datos derivados de la imagen (resultados automáticos del análisis).</li>
            </ul>
            <h4 className="font-semibold mt-4 mb-2">Privacidad y Seguridad</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Tus imágenes se procesan solo para el análisis y se eliminan inmediatamente después.</li>
              <li>No se almacenan datos personales ni se comparten con terceros.</li>
              <li>Se aplican medidas de seguridad para proteger tu información.</li>
            </ul>
            <h4 className="font-semibold mt-4 mb-2">Tus derechos</h4>
            <ul className="list-disc pl-5 space-y-1">
              <li>Puedes solicitar acceso, rectificación, actualización, cancelación u oposición al tratamiento de tus datos escribiendo a <a href="mailto:contacto@pielsanaia.com">contacto@pielsanaia.com</a>.</li>
            </ul>
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <p className="font-medium">
                Al aceptar, confirmas que has leído y comprendido la información anterior, y prestas tu consentimiento libre, expreso e informado para el tratamiento temporal de tus datos sensibles en los términos expuestos.
              </p>
            </div>
          </div>
          <div className="mt-6 flex items-center">
            <input
              id="consent-check"
              type="checkbox"
              checked={checked}
              onChange={e => setChecked(e.target.checked)}
              className="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="consent-check" className="text-gray-700 text-sm select-none">
              He leído y acepto el consentimiento informado para el tratamiento de mis datos sensibles.
            </label>
          </div>
          <div className="mt-6 flex justify-end space-x-4">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              Cancelar
            </button>
            <button
              onClick={onAccept}
              className={`px-4 py-2 rounded-md text-white ${checked ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-300 cursor-not-allowed'}`}
              disabled={!checked}
            >
              Aceptar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const ImageUploader: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showConsent, setShowConsent] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setShowConsent(true);
      e.dataTransfer.clearData();
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setShowConsent(true);
    }
  };

  const handleFile = (file: File) => {
    if (!file.type.match('image.*')) {
      alert('Por favor sube una imagen válida');
      return;
    }
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target && typeof e.target.result === 'string') {
        setImage(e.target.result);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleConsentAccept = () => {
    setShowConsent(false);
    if (fileInputRef.current?.files?.[0]) {
      handleFile(fileInputRef.current.files[0]);
    }
  };

  const handleRemoveImage = () => {
    setImage(null);
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);
  
    const formData = new FormData();
    formData.append('file', selectedFile);
  
    try {
      const response = await fetch('http://localhost:8080/skin/api/analyze', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Error en el análisis');
      const data = await response.json();
      navigate(`/results/${data.id}`);
    } catch {
      alert('Error al analizar la imagen');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      {showConsent && (
        <ConsentModal 
          onAccept={handleConsentAccept}
          onClose={() => {
            setShowConsent(false);
            if (fileInputRef.current) {
              fileInputRef.current.value = '';
            }
          }}
        />
      )}
      
      <div className="flex items-center text-blue-600 mb-4">
        <ImageIcon className="h-6 w-6 mr-2" />
        <h2 className="text-xl font-semibold">Análisis de Imagen</h2>
      </div>
      
      {!image ? (
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center ${
            isDragging ? 'border-blue-600 bg-blue-50' : 'border-gray-300'
          } transition-colors duration-200`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-lg font-medium text-gray-900">Sube una foto de tu piel</p>
          <p className="text-sm text-gray-500 mt-1">Arrastra y suelta o haz clic para seleccionar</p>
          
          <div className="mt-6">
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleFileInput}
              ref={fileInputRef}
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <Camera className="h-5 w-5 mr-2" />
              Seleccionar Imagen
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative">
            <img
              src={image}
              alt="Imagen para análisis"
              className="mx-auto max-h-80 rounded-lg object-contain"
            />
            <button
              className="absolute top-2 right-2 bg-red-600 text-white rounded-full p-1 hover:bg-red-700 focus:outline-none"
              onClick={handleRemoveImage}
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          
          <div className="flex justify-center">
            <button
              type="button"
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white ${
                isAnalyzing ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'
              } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200`}
            >
              {isAnalyzing ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white\" xmlns="http://www.w3.org/2000/svg\" fill="none\" viewBox="0 0 24 24">
                    <circle className="opacity-25\" cx="12\" cy="12\" r="10\" stroke="currentColor\" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analizando...
                </>
              ) : (
                'Analizar Imagen'
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;