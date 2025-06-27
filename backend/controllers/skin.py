from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from pathlib import Path
import asyncio
import uuid

# Importar el servicio de análisis de piel
from backend.services.skin_analysis_service import predict_lunares_class
from backend.models.condition import ConditionInfo

# Configurar el router
router = APIRouter()

# Diccionario de condiciones (temporal, normalmente iría en un archivo aparte)
conditions_data = {
    "rosacea": ConditionInfo(
        name="rosacea",
        title="Rosácea",
        description="La rosácea es una afección crónica que causa enrojecimiento y vasos sanguíneos visibles en la cara, a veces con pequeños bultos rojos llenos de pus.",
        causes=[
            'Predisposición genética',
            'Problemas con los vasos sanguíneos faciales',
            'Ácaros microscópicos (Demodex)',
            'Bacterias intestinales (H. pylori)',
            'Desencadenantes ambientales'
        ],
        symptoms=[
            'Enrojecimiento persistente en el centro de la cara',
            'Vasos sanguíneos dilatados visibles',
            'Bultos rojos (pápulas) y pústulas',
            'Sensación de ardor o escozor',
            'Piel sensible y reactiva',
            'Engrosamiento de la piel nasal (rinofima)'
        ],
        treatment=[
            'Medicamentos tópicos (metronidazol, ácido azelaico)',
            'Antibióticos orales',
            'Isotretinoína (casos severos)',
            'Terapias con láser o luz pulsada',
            'Evitar desencadenantes conocidos'
        ],
        prevention=[
            'Usar protector solar diariamente',
            'Evitar extremos de temperatura',
            'Evitar alimentos y bebidas desencadenantes',
            'Usar productos para piel sensible',
            'Mantener una buena rutina de cuidado facial'
        ],
        image='https://images.pexels.com/photos/1138531/pexels-photo-1138531.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
    ),
    "acne": ConditionInfo(
        name="acne",
        title="Acné",
        description="El acné es una condición común que ocurre cuando los folículos pilosos se obstruyen con grasa y células muertas de la piel, causando granos y espinillas.",
        causes=[
            'Cambios hormonales',
            'Exceso de producción de grasa (sebo)',
            'Bacterias',
            'Ciertos medicamentos',
            'Estrés'
        ],
        symptoms=[
            'Puntos negros y blancos',
            'Espinillas',
            'Protuberancias rojas y dolorosas',
            'Quistes',
            'Cicatrices'
        ],
        treatment=[
            'Limpieza suave de la piel',
            'Medicamentos tópicos (peróxido de benzoilo, retinoides)',
            'Antibióticos',
            'Terapias hormonales',
            'Evitar manipular las lesiones'
        ],
        prevention=[
            'Lavar el rostro regularmente',
            'Evitar productos grasos',
            'No exprimir los granos',
            'Mantener el cabello limpio',
            'Usar protector solar no comedogénico'
        ],
        image='https://images.pexels.com/photos/10004287/pexels-photo-10004287.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
    ),
    "manchas": ConditionInfo(
        name="manchas",
        title="Manchas Solares",
        description="Las manchas solares son áreas de la piel que se oscurecen debido a la exposición prolongada al sol, también conocidas como lentigos solares.",
        causes=[
            'Exposición excesiva a la radiación UV',
            'Envejecimiento de la piel',
            'Predisposición genética'
        ],
        symptoms=[
            'Manchas planas y marrones',
            'Aparición en zonas expuestas al sol',
            'No suelen causar dolor ni molestias'
        ],
        treatment=[
            'Cremas despigmentantes',
            'Tratamientos con láser',
            'Peelings químicos',
            'Crioterapia',
            'Protección solar diaria'
        ],
        prevention=[
            'Evitar la exposición solar prolongada',
            'Usar protector solar de amplio espectro',
            'Utilizar ropa protectora',
            'Evitar camas solares',
            'Revisar la piel regularmente'
        ],
        image='https://images.pexels.com/photos/7479603/pexels-photo-7479603.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
    ),
    "lunares": ConditionInfo(
        name="lunares",
        title="Lunares",
        description="Los lunares son áreas pequeñas de pigmentación en la piel, generalmente inofensivas, pero algunos pueden evolucionar y requerir control dermatológico.",
        causes=[
            'Acumulación de melanocitos',
            'Factores genéticos',
            'Exposición solar'
        ],
        symptoms=[
            'Pequeñas manchas marrones o negras',
            'Pueden ser planas o elevadas',
            'Cambios en el color, tamaño o forma pueden ser signo de alerta'
        ],
        treatment=[
            'Observación regular',
            'Extirpación quirúrgica si es necesario',
            'Biopsia en caso de sospecha de malignidad',
            'Evitar la exposición solar excesiva',
            'Consulta dermatológica ante cambios sospechosos'
        ],
        prevention=[
            'Usar protector solar',
            'Evitar la exposición solar intensa',
            'Autoexamen de la piel',
            'Consultar al dermatólogo ante cambios',
            'No manipular los lunares'
        ],
        image='https://images.pexels.com/photos/8058606/pexels-photo-8058606.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
    ),
}

# Almacenamiento en memoria para resultados de lunares
lunares_results = {}

@router.get("/", response_class=HTMLResponse)
async def get_upload_page(request: Request):
    """Sirve la página principal para cargar imágenes."""
    raise HTTPException(status_code=404, detail="No implementado: la vista HTML es manejada por el frontend.")

@router.post("/upload")
async def handle_image_upload(request: Request, file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
    try:
        image_bytes = await file.read()
        pred_label, probabilities = predict_lunares_class(image_bytes)
        if pred_label is not None:
            print(f"Predicción para {file.filename}: {pred_label}")
        else:
            print(f"No se pudo predecir la clase para {file.filename}.")
            raise HTTPException(status_code=500, detail="Error al procesar la imagen: No se pudo predecir la clase.")
        return {"filename": file.filename, "prediccion": pred_label, "probabilidades": probabilities}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error crítico al procesar la imagen: {e}")
        raise HTTPException(status_code=500, detail=f"Error crítico al procesar la imagen: {str(e)}")

@router.get("/results", response_class=HTMLResponse)
async def get_results_page(request: Request, image_name: str = None, analysis_status: str = None):
    """Sirve la página de resultados."""
    raise HTTPException(status_code=404, detail="No implementado: la vista HTML es manejada por el frontend.")

@router.post("/api/analyze", tags=["Skin Analysis API"])
async def api_analyze_skin(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
    try:
        image_bytes = await file.read()
        pred_label, probabilities = predict_lunares_class(image_bytes)
        if pred_label is not None:
            return {
                "filename": file.filename,
                "content_type": file.content_type,
                "prediccion": pred_label,
                "probabilidades": probabilities
            }
        else:
            raise HTTPException(status_code=500, detail="No se pudo predecir la clase para la imagen.")
    except Exception as e:
        print(f"Error en API /api/analyze: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor al analizar la imagen: {str(e)}")

@router.post("/api/analyze-lunares", tags=["Skin Analysis API"])
async def api_analyze_lunares(file: UploadFile = File(...)):
    """Endpoint API para analizar una imagen solo con el modelo lunares.keras."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
    try:
        image_bytes = await file.read()
        pred_label, probabilities = predict_lunares_class(image_bytes)
        if pred_label is not None:
            result_id = str(uuid.uuid4())
            lunares_results[result_id] = {
                "filename": file.filename,
                "content_type": file.content_type,
                "prediccion": pred_label,
                "probabilidades": probabilities
            }
            return {"id": result_id}
        else:
            raise HTTPException(status_code=500, detail="No se pudo predecir la clase para la imagen.")
    except Exception as e:
        print(f"Error en API /api/analyze-lunares: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor al analizar la imagen: {str(e)}")

@router.get("/api/analyze-lunares/{result_id}", tags=["Skin Analysis API"])
async def get_lunares_result(result_id: str):
    """Obtener el resultado del análisis de lunares por ID."""
    result = lunares_results.get(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return result

@router.get("/api/condition/{condition_name}", response_model=ConditionInfo, tags=["Skin Info"])
async def get_condition_info(condition_name: str):
    condition = conditions_data.get(condition_name.lower())
    if not condition:
        raise HTTPException(status_code=404, detail="Condición no encontrada")
    return condition 