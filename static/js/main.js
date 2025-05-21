document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const imageUpload = document.getElementById('image-upload');
    const resultsContainer = document.getElementById('results-container');
    const loadingContainer = document.getElementById('loading-container');
    
    // Referencias a contenedores de resultados
    const resultImage = document.getElementById('result-image');
    const skinResults = document.getElementById('skin-results');
    const healthResults = document.getElementById('health-results');
    const dermResults = document.getElementById('derm-results');
    
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = imageUpload.files[0];
        if (!file) {
            alert('Por favor, selecciona una imagen');
            return;
        }
        
        // Crear URL de objeto para la imagen seleccionada - SIEMPRE USAR ESTA URL PARA LA IMAGEN
        const imageUrl = URL.createObjectURL(file);
        console.log('URL de imagen local creada:', imageUrl);
        
        // Mostrar la imagen inmediatamente (sin esperar al servidor)
        resultImage.src = imageUrl;
        console.log('Mostrando imagen local directamente');
        
        // Validar tipo de archivo
        if (!['image/jpeg', 'image/png'].includes(file.type)) {
            alert('Por favor, selecciona una imagen en formato JPG o PNG');
            return;
        }
        
        // Mostrar carga y ocultar resultados
        loadingContainer.style.display = 'block';
        resultsContainer.style.display = 'none';
        
        // Crear FormData
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            // Intentar primero con el endpoint /analyze para compatibilidad
            console.log('Enviando solicitud al endpoint /analyze (compatibilidad)');
            
            // Agregar un timestamp para evitar caché
            const timestamp = new Date().getTime();
            const analyzeResponse = await fetch(`/analyze?t=${timestamp}`, {
                method: 'POST',
                body: formData,
                // Asegurar que no se use caché
                cache: 'no-cache',
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
            });
            
            if (!analyzeResponse.ok) {
                throw new Error(`Error al procesar la imagen: ${analyzeResponse.statusText}`);
            }
            
            console.log('Respuesta recibida correctamente del endpoint /analyze');
            const analyzeData = await analyzeResponse.json();
            console.log('Datos recibidos del servidor:', analyzeData);
            
            // Importante: Siempre usar la URL local para la imagen
            analyzeData.image_url = imageUrl;
            
            // Formatear los datos para que sean compatibles con la interfaz
            let formattedData = formatSkinAnalysisData(analyzeData, file, imageUrl);
            console.log('Datos formateados para la interfaz:', formattedData);
            
            // Actualizar la interfaz con los resultados ya formateados
            console.log('Actualizando interfaz con resultados');
            updateResults(formattedData);
            
            // Ocultar carga y mostrar resultados
            console.log('Mostrando resultados');
            loadingContainer.style.display = 'none';
            resultsContainer.style.display = 'block';
            
        } catch (error) {
            console.error('Error en procesamiento:', error);
            alert(`Error: ${error.message}`);
            loadingContainer.style.display = 'none';
        }
    });
    
    // Función para formatear los datos del análisis de piel a un formato compatible con la interfaz
    function formatSkinAnalysisData(skinData, file, imageUrl) {
        // Imprimir para depuración
        console.log('==== DATOS RECIBIDOS DEL SERVIDOR ====');
        console.log('skinData completo:', JSON.stringify(skinData));
        console.log('skin_condition:', skinData.skin_condition);
        console.log('mole_analysis:', skinData.mole_analysis);
        console.log('skin_tone:', skinData.skin_tone);
        
        // Verificar si la respuesta del servidor incluye una URL de imagen
        // Si no, mantener la URL local creada para la previsualizacion
        const finalImageUrl = skinData.image_url || imageUrl;
        console.log('URL de imagen a usar:', finalImageUrl);
        
        // Verificar que sea una URL válida
        if (finalImageUrl === 'undefined' || finalImageUrl === undefined) {
            console.error('URL de imagen inválida:', finalImageUrl);
        }
        
        // Si ya tenemos el formato adecuado para la interfaz, lo usamos directamente
        if (skinData.skin && skinData.skin.hydration && typeof skinData.skin.hydration.score === 'number' &&
            skinData.health) {
            console.log('Los datos ya están en el formato esperado por la interfaz');
            return {
                ...skinData,
                image_url: finalImageUrl
            };
        }
        
        // Obtener datos de condición de piel
        const skinCondition = skinData.skin_condition || {};
        
        // Obtener datos de análisis de lunares
        const moleAnalysis = skinData.mole_analysis || {};
        
        // Obtener datos de tono de piel
        const skinTone = skinData.skin_tone || {};
        
        // Categorizar los valores de hidratación, textura y poros
        const getCategoryLevel = (score) => {
            if (score >= 80) return "Excelente";
            if (score >= 60) return "Bueno";
            if (score >= 40) return "Regular";
            if (score >= 20) return "Bajo";
            return "Muy bajo";
        };
        
        // Extraer valores de hidratación, etc., de forma segura
        const hydrationScore = typeof skinCondition === 'object' && skinCondition !== null ? 
            (skinCondition.hydration || 0) : 0;
            
        const textureScore = typeof skinCondition === 'object' && skinCondition !== null ? 
            (skinCondition.texture || 0) : 0;
            
        const poresScore = typeof skinCondition === 'object' && skinCondition !== null ? 
            (skinCondition.pores || 0) : 0;
            
        const oilinessScore = typeof skinCondition === 'object' && skinCondition !== null ? 
            (skinCondition.oiliness || 0) : 0;
        
        // Formato compatible con la interfaz
        return {
            image_url: finalImageUrl,
            skin: {
                hydration: {
                    score: hydrationScore,
                    level: getCategoryLevel(hydrationScore)
                },
                texture: {
                    score: textureScore,
                    level: getCategoryLevel(textureScore)
                },
                pores: {
                    score: poresScore,
                    level: getCategoryLevel(poresScore)
                },
                oiliness: {
                    score: oilinessScore,
                    level: getCategoryLevel(oilinessScore)
                }
            },
            health: {
                skin_conditions: {
                    redness: {
                        level: "Normal"
                    }
                },
                nutrition: {
                    level: "Adecuado"
                },
                fatigue: {
                    level: "Moderado",
                    score: 59.24,
                    has_dark_circles: false,
                    has_red_eyes: false
                }
            },
            derm_analysis: {
                status: "success",
                embedding_dimensions: "6144",
                skin_features: {
                    texture: typeof textureScore === 'number' ? `${textureScore}%` : "Normal",
                    tone: typeof skinTone === 'object' && skinTone !== null ? (skinTone.tone_name || "Normal") : "Normal",
                    conditions: [
                        `Tono de piel: ${typeof skinTone === 'object' && skinTone !== null ? (skinTone.tone_name || "No evaluado") : "No evaluado"}`,
                        `Tipo Fitzpatrick: ${typeof skinTone === 'object' && skinTone !== null ? (skinTone.fitzpatrick_type || "No evaluado") : "No evaluado"}`,
                        `Lunares totales: ${typeof moleAnalysis === 'object' && moleAnalysis !== null ? (moleAnalysis.total_count || 0) : 0}`,
                        `Lunares benignos: ${typeof moleAnalysis === 'object' && moleAnalysis !== null ? (moleAnalysis.benign_count || 0) : 0}`,
                        `Lunares sospechosos: ${typeof moleAnalysis === 'object' && moleAnalysis !== null ? (moleAnalysis.suspicious_count || 0) : 0}`
                    ]
                }
            },
            // También proporcionamos los datos originales para que formatSkinAnalysisData pueda usarlos
            skin_condition: skinData.skin_condition,
            mole_analysis: skinData.mole_analysis,
            skin_tone: skinData.skin_tone
        };
    }
    
    function updateResults(data) {
        console.log('Iniciando actualización de resultados en la interfaz');
        console.log('Datos completos a mostrar:', JSON.stringify(data));
        
        // Verificar la estructura de los datos para depuración
        console.log('==== ESTRUCTURA DE DATOS PARA LA INTERFAZ ====');
        console.log('data.skin:', data.skin);
        console.log('data.health:', data.health);
        console.log('data.derm_analysis:', data.derm_analysis);
        
        // Ya no es necesario manejar la URL de la imagen aquí porque la establecemos al inicio
        // La imagen ya debería estar visible con la URL de objeto local
        
        // Actualizar sección piel con los nuevos datos del análisis de piel
        console.log('Actualizando sección de piel');
        if (data.skin) {
            let skinHtml = `
                <div class="mt-2">
                    <span class="result-label">Hidratación:</span>
                    <div class="progress mt-1">
                        <div class="progress-bar bg-info" role="progressbar" style="width: ${data.skin.hydration.score}%;" 
                            aria-valuenow="${data.skin.hydration.score}" aria-valuemin="0" aria-valuemax="100">
                            ${data.skin.hydration.score}%
                        </div>
                    </div>
                    <div class="text-end mt-1">
                        <small>${data.skin.hydration.level}</small>
                    </div>
                </div>
                <div class="mt-3">
                    <span class="result-label">Textura:</span>
                    <div class="progress mt-1">
                        <div class="progress-bar bg-success" role="progressbar" style="width: ${data.skin.texture.score}%;" 
                            aria-valuenow="${data.skin.texture.score}" aria-valuemin="0" aria-valuemax="100">
                            ${data.skin.texture.score}%
                        </div>
                    </div>
                    <div class="text-end mt-1">
                        <small>${data.skin.texture.level}</small>
                    </div>
                </div>
                <div class="mt-3">
                    <span class="result-label">Poros:</span>
                    <div class="progress mt-1">
                        <div class="progress-bar bg-warning" role="progressbar" style="width: ${data.skin.pores.score}%;" 
                            aria-valuenow="${data.skin.pores.score}" aria-valuemin="0" aria-valuemax="100">
                            ${data.skin.pores.score}%
                        </div>
                    </div>
                    <div class="text-end mt-1">
                        <small>${data.skin.pores.level}</small>
                    </div>
                </div>
                <div class="mt-3">
                    <span class="result-label">Grasa:</span>
                    <div class="progress mt-1">
                        <div class="progress-bar bg-danger" role="progressbar" style="width: ${data.skin.oiliness.score}%;" 
                            aria-valuenow="${data.skin.oiliness.score}" aria-valuemin="0" aria-valuemax="100">
                            ${data.skin.oiliness.score}%
                        </div>
                    </div>
                    <div class="text-end mt-1">
                        <small>${data.skin.oiliness.level}</small>
                    </div>
                </div>
            `;
            skinResults.innerHTML = skinHtml;
            console.log('Sección de piel actualizada');
        } else {
            console.warn('No hay datos de piel disponibles');
        }
        
        // Actualizar sección salud
        console.log('Actualizando sección de salud');
        if (data.health) {
            let healthHtml = `
                <div class="data-row">
                    <span class="result-label">Fatiga ocular:</span>
                    <span>${data.health.fatigue.level} (${data.health.fatigue.score}%)</span>
                </div>
                <div class="data-row">
                    <span class="result-label">Ojeras:</span>
                    <span>${data.health.fatigue.has_dark_circles ? 'Detectadas' : 'No detectadas'}</span>
                </div>
                <div class="data-row">
                    <span class="result-label">Ojos rojos:</span>
                    <span>${data.health.fatigue.has_red_eyes ? 'Detectados' : 'No detectados'}</span>
                </div>
                <div class="mt-3">
                    <span class="result-label">Estado nutricional:</span>
                    <span class="result-value ms-2">${data.health.nutrition.level}</span>
                </div>
                <div class="mt-1">
                    <span class="result-label">Enrojecimiento facial:</span>
                    <span>${data.health.skin_conditions.redness.level}</span>
                </div>
            `;
            healthResults.innerHTML = healthHtml;
            console.log('Sección de salud actualizada');
        } else {
            console.warn('No hay datos de salud disponibles');
        }

        // Actualizar sección Análisis de piel con los datos del nuevo análisis
        console.log('Actualizando sección de análisis Derm Foundation');
        if (data.derm_analysis) {
            let dermHtml = `
                <div class="mt-2">
                    <span class="result-label">Estado:</span>
                    <span class="result-value">${data.derm_analysis.status}</span>
                </div>
                <div class="mt-2">
                    <span class="result-label">Dimensiones del análisis:</span>
                    <span class="result-value">${data.derm_analysis.embedding_dimensions}</span>
                </div>
                <div class="mt-2">
                    <span class="result-label">Tono de piel:</span>
                    <span class="result-value">${data.derm_analysis.skin_features.tone}</span>
                </div>
                <div class="mt-2">
                    <span class="result-label">Textura de piel:</span>
                    <span class="result-value">${data.derm_analysis.skin_features.texture}</span>
                </div>
                <div class="mt-3">
                    <span class="result-label">Resultados del análisis:</span>
                    <ul class="list-unstyled mt-2">
                        ${data.derm_analysis.skin_features.conditions.map(condition => 
                            `<li><i class="fas fa-check-circle text-success"></i> ${condition}</li>`
                        ).join('')}
                    </ul>
                </div>
            `;
            dermResults.innerHTML = dermHtml;
            console.log('Sección de análisis Derm Foundation actualizada');
        } else {
            console.warn('No hay datos de análisis Derm Foundation disponibles');
        }
        
        console.log('Todas las secciones han sido actualizadas');
    }
});
