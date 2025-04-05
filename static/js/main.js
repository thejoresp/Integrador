document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const imageUpload = document.getElementById('image-upload');
    const resultsContainer = document.getElementById('results-container');
    const loadingContainer = document.getElementById('loading-container');
    
    // Referencias a contenedores de resultados
    const resultImage = document.getElementById('result-image');
    const ageGenderResults = document.getElementById('age-gender-results');
    const emotionResults = document.getElementById('emotion-results');
    const skinResults = document.getElementById('skin-results');
    const healthResults = document.getElementById('health-results');
    
    // Gráficos para mostrar resultados
    let emotionChart = null;
    
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = imageUpload.files[0];
        if (!file) {
            alert('Por favor, selecciona una imagen');
            return;
        }
        
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
            // Enviar imagen al servidor
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Error al procesar la imagen: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Actualizar la interfaz con los resultados
            updateResults(data);
            
            // Ocultar carga y mostrar resultados
            loadingContainer.style.display = 'none';
            resultsContainer.style.display = 'block';
            
        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
            loadingContainer.style.display = 'none';
        }
    });
    
    function updateResults(data) {
        // Mostrar imagen
        resultImage.src = data.image_url;
        
        // Actualizar sección edad y género
        if (data.age_gender) {
            let ageGenderHtml = `
                <div class="data-row">
                    <span class="result-label">Edad aparente:</span>
                    <span class="result-value">${data.age_gender.age.years} años</span>
                </div>
                <div class="data-row">
                    <span class="result-label">Rango de edad:</span>
                    <span>${data.age_gender.age.range} años</span>
                </div>
                <div class="data-row">
                    <span class="result-label">Género aparente:</span>
                    <span class="result-value">${data.age_gender.gender.label}</span>
                </div>
                <div class="data-row">
                    <span class="result-label">Confianza:</span>
                    <span>${data.age_gender.gender.confidence}%</span>
                </div>
                <div class="mt-3">
                    <span class="result-label">Simetría facial:</span>
                    <div class="progress mt-2">
                        <div class="progress-bar" role="progressbar" style="width: ${data.age_gender.symmetry.score}%;" 
                            aria-valuenow="${data.age_gender.symmetry.score}" aria-valuemin="0" aria-valuemax="100">
                            ${data.age_gender.symmetry.score}%
                        </div>
                    </div>
                    <div class="text-end mt-1">
                        <small>${data.age_gender.symmetry.level}</small>
                    </div>
                </div>
            `;
            ageGenderResults.innerHTML = ageGenderHtml;
        }
        
        // Actualizar sección emociones
        if (data.emotion) {
            let emotionHtml = `
                <div class="data-row">
                    <span class="result-label">Emoción dominante:</span>
                    <span class="result-value">${capitalize(data.emotion.dominant_emotion)}</span>
                </div>
                <div class="data-row">
                    <span class="result-label">Nivel de estrés:</span>
                    <span>${data.emotion.stress_level.level} (${data.emotion.stress_level.score}%)</span>
                </div>
                <div class="data-row">
                    <span class="result-label">Expresión social:</span>
                    <span>${capitalize(data.emotion.social_expression)}</span>
                </div>
                <div class="mt-3">
                    <canvas id="emotion-chart" class="emotion-chart"></canvas>
                </div>
            `;
            emotionResults.innerHTML = emotionHtml;
            
            // Crear gráfico de emociones
            createEmotionChart(data.emotion.emotions);
        }
        
        // Actualizar sección piel
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
            `;
            skinResults.innerHTML = skinHtml;
        }
        
        // Actualizar sección salud
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
        }
    }
    
    function createEmotionChart(emotions) {
        const ctx = document.getElementById('emotion-chart').getContext('2d');
        
        // Destruir gráfico existente si hay uno
        if (emotionChart) {
            emotionChart.destroy();
        }
        
        // Ordenar emociones por valor
        const sortedEmotions = Object.entries(emotions)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5); // Mostrar solo las 5 principales
            
        const labels = sortedEmotions.map(item => capitalize(item[0]));
        const values = sortedEmotions.map(item => item[1]);
        
        emotionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Emociones (%)',
                    data: values,
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
    
    // Función para capitalizar la primera letra
    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
});
