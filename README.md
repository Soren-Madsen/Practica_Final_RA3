# Sistema RAG - Chat

Sistema de **Retrieval-Augmented Generation (RAG)** para responder preguntas.

## Descripción

Sistema que recupera documentos relevantes y genera respuestas precisas usando modelos de IA.

## Modelos Utilizados

- **Embeddings**: `MongoDB/mdbr-leaf-ir`
- **Lenguaje**: `PleIAs/Pleias-RAG-350M`

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/Soren-Madsen/Practica-Final-RA3-Analisis-predictivo-de-informacion.git
cd Practica-Final-RA3-Analisis-predictivo-de-informacion.

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Ejecutar ejemplos de prueba
```bash
python rag_engine.py
```

### Pruebas interactivas
```bash
python test_query.py
```

### Uso en código
```python
from rag_engine import preguntar

respuesta = preguntar("What is the hospital email?")
print(respuesta)
# Output: "The hospital email is testing@gmail.com."
```

## Funciones Principales

### `recuperar_documentos(consulta, top_k=2, umbral=0.4)`
Recupera documentos relevantes de la base de conocimiento.

- `consulta`: Pregunta del usuario
- `top_k`: Número máximo de documentos
- `umbral`: Similitud mínima (0.0 - 1.0)

### `generar_respuesta(consulta, documentos_recuperados)`
Genera una respuesta usando el modelo de lenguaje.

### `preguntar(consulta, top_k=2, umbral=0.4)`
Función completa que recupera documentos y genera la respuesta.

## Ejemplos

```python
>>> preguntar("What is the hospital email?")
"The hospital email is testing@gmail.com."

>>> preguntar("What are the working hours?")
"The hospital's working hours are 7:00 AM - 8:00 PM daily."

>>> preguntar("Where is the hospital located?")
"The hospital is located at xyz, abc, 1234, Nepal."
```

## Estructura del Proyecto

```
├── rag_engine.py       # Motor principal RAG
├── app.py              # Interfaz Gradio
├── documents.json      # Base de conocimiento
├── test_query.py       # Pruebas interactivas
├── tests/
│   └── test_api.py     # Tests de la API
└── requirements.txt    # Dependencias
```

## Despliegue en Hugging Face Spaces

### 1. Crear un Space en Hugging Face

1. Ir a [huggingface.co/spaces](https://huggingface.co/spaces)
2. Crear un nuevo Space
3. Seleccionar "Gradio" como SDK
4. Configurar nombre y visibilidad

### 2. Desplegar la aplicación

```bash
# Clonar el Space
git clone https://huggingface.co/spaces/tu-usuario/nombre-del-space
cd nombre-del-space

# Copiar archivos del proyecto
cp ../Practica-Final-RA3-Analisis-predictivo-de-informacion/* .

# Push a Hugging Face
git add .
git commit -m "Deploy RAG Chat"
git push
```

### 3. Probar la API con Gradio Client

Una vez desplegado, puedes probar la API usando el script `test_api.py`:

```python
from gradio_client import Client

client = Client("tu-usuario/nombre-del-space")
result = client.predict(
    query="What is the hospital email?",
    top_k=2,
    umbral=0.55,
    api_name="/ask"
)
print(result[0])  # Respuesta
print(result[1])  # Documentos recuperados
```

**Para ejecutar el test:**

```bash
python tests/test_api.py
```

Si todo está correcto, verás:
- La respuesta generada
- Los documentos recuperados

## Autor

**Soren Madsen**  
GitHub: [@Soren-Madsen](https://github.com/Soren-Madsen)

---
*Última actualización: Marzo 2026*
