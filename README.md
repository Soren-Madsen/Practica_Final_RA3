# 🤖 Chat RAG - Análisis Predictivo

Sistema completo de **Retrieval-Augmented Generation (RAG)** con interfaz web e API para responder preguntas basadas en una base de conocimiento.

## 📋 Descripción

Este proyecto implementa un sistema RAG que:
- ✅ Recupera documentos relevantes usando embeddings semánticos
- ✅ Genera respuestas precisas con un modelo de lenguaje especializado
- ✅ Ofrece interfaz interactiva con Gradio
- ✅ Expone API REST para integración externa
- ✅ Desplegado en Hugging Face Spaces

## 🧠 Modelos Utilizados

| Componente | Modelo | Tamaño |
|-----------|--------|--------|
| **Embeddings** | `MongoDB/mdbr-leaf-ir` | ~90 MB |
| **Lenguaje** | `PleIAs/Pleias-RAG-350M` | ~707 MB |

Ambos modelos optimizados para CPU en entornos serverless.

---

## 🚀 Inicio Rápido

### Acceso Online
**🌐 [Abre el Chat RAG en Hugging Face Spaces](https://huggingface.co/spaces/SorenMad/ChatRAG2)**

### Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/Soren-Madsen/Practica-Final-RA3-Analisis-predictivo-de-informacion.git
cd Practica-Final-RA3-Analisis-predictivo-de-informacion.

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

Abre tu navegador en `http://localhost:7860`

---

## 💻 Uso

### Opción 1: Interfaz Web (Gradio)

```bash
python app.py
```

Luego accede a `http://localhost:7860` y:
1. Escribe tu pregunta en inglés
2. Ajusta los parámetros (Top K, Umbral) si lo deseas
3. Haz clic en "Enviar"

**Parámetros:**
- **Top K**: Número de documentos a recuperar (1-5)
- **Umbral**: Similitud mínima requerida (0.0-1.0)

### Opción 2: API Python

```python
from rag_engine import preguntar

# Hacer una pregunta
respuesta = preguntar("What is the hospital email?", top_k=1, umbral=0.55)
print(respuesta)
# Output: "The hospital email is testing@gmail.com."
```

### Opción 3: Pruebas Locales

```bash
# Ejecutar ejemplos de prueba
python rag_engine.py
```

### Opción 4: API Remota (Hugging Face)

```python
from gradio_client import Client

client = Client("SorenMad/ChatRAG2")
result = client.predict(
    query="Where is the hospital located?",
    top_k=1,
    umbral=0.55,
    api_name="/ask"
)
print(result[0])  # Respuesta
print(result[1])  # Documentos recuperados
```

O ejecuta:
```bash
python tests/test_api.py
```

---

## 📚 Referencia de Funciones

### `recuperar_documentos(consulta, top_k=2, umbral=0.4)`
Recupera documentos relevantes basados en similitud semántica.

**Parámetros:**
- `consulta` (str): Pregunta del usuario
- `top_k` (int): Número máximo de documentos a retornar
- `umbral` (float): Similitud mínima (0.0 - 1.0)

**Retorna:** Lista de textos de documentos relevantes

```python
docs = recuperar_documentos("What is the hospital email?", top_k=2, umbral=0.4)
# Output: ['Document 1 text', 'Document 2 text']
```

### `generar_respuesta(consulta, documentos_recuperados)`
Genera una respuesta usando los documentos como contexto.

**Parámetros:**
- `consulta` (str): Pregunta original
- `documentos_recuperados` (list): Documentos del paso anterior

**Retorna:** String con la respuesta generada

```python
respuesta = generar_respuesta("What is the email?", docs)
# Output: "The hospital email is testing@gmail.com."
```

### `preguntar(consulta, top_k=2, umbral=0.4)`
Función completa que combina recuperación y generación.

```python
respuesta = preguntar("What are the working hours?")
# Output: "The hospital's working hours are 7:00 AM - 8:00 PM daily."
```

---

## 📂 Estructura del Proyecto

```
├── app.py                          # Interfaz Gradio (web)
├── rag_engine.py                   # Motor RAG principal
├── documents.json                  # Base de conocimiento
├── requirements.txt                # Dependencias Python
├── README.md                       # Este archivo
├── LICENSE                         # Licencia MIT
├── tests/
│   └── test_api.py                 # Tests de API remota
└── teoria/
    └── crud_flask.py               # Código teórico (referencia)
```

---

## 🧪 Ejemplos de Uso

### Pregunta 1: Email
```
Input:  "What is the hospital email?"
Output: "The hospital email is testing@gmail.com."
```

### Pregunta 2: Horarios
```
Input:  "What are the working hours?"
Output: "The hospital's working hours are 7:00 AM - 8:00 PM daily."
```

### Pregunta 3: Ubicación
```
Input:  "Where is the hospital located?"
Output: "The hospital is located at xyz, abc, 1234, Nepal."
```

---

## 🌐 Despliegue en Hugging Face Spaces

El proyecto está **ya desplegado y funcionando** en:
- **URL:** https://huggingface.co/spaces/SorenMad/ChatRAG2
- **Estado:** ✅ Running
- **API:** Disponible y documentada

### Para desplegar tu propia instancia:

1. **Crear un Space en Hugging Face**
   - Ir a https://huggingface.co/spaces
   - Crear nuevo Space con SDK "Gradio"

2. **Clonar y actualizar el Space**
   ```bash
   git clone https://huggingface.co/spaces/tu-usuario/tu-space
   cd tu-space
   cp app.py rag_engine.py documents.json requirements.txt .
   ```

3. **Push de cambios**
   ```bash
   git add .
   git commit -m "Deploy Chat RAG"
   git push
   ```

El Space se actualizará automáticamente.

---

## ⚙️ Configuración

### Parámetros Recomendados

Para **máxima precisión:**
```python
preguntar(consulta, top_k=2, umbral=0.55)
```

Para **máxima cobertura:**
```python
preguntar(consulta, top_k=5, umbral=0.40)
```

Para **respuestas rápidas:**
```python
preguntar(consulta, top_k=1, umbral=0.60)
```

### Modelos Personalizados

Para usar otros modelos, edita `rag_engine.py`:

```python
# Cambiar modelo de embeddings
embedding_model = SentenceTransformer("tu-modelo-aqui")

# Cambiar modelo de lenguaje
language_model = AutoModelForCausalLM.from_pretrained("tu-modelo-aqui")
```

---

## 📊 Arquitectura RAG

```
┌─────────────────┐
│  Pregunta       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ 1. RECUPERACIÓN            │
│ (Embedding + Similitud)     │
└────────┬────────────────────┘
         │
         ▼ Documentos relevantes
┌─────────────────────────────┐
│ 2. GENERACIÓN              │
│ (LLM + Contexto)            │
└────────┬────────────────────┘
         │
         ▼
    ┌──────────┐
    │ Respuesta│
    └──────────┘
```

**Recuperación:**
- Convierte pregunta a embedding (768-dim)
- Calcula similitud coseno con documentos
- Filtra por umbral y retorna top-k

**Generación:**
- Inyecta documentos como contexto
- Pasa a modelo de lenguaje especializado
- Genera respuesta determinista (sin muestreo)

---

## 🔧 Requisitos

- Python 3.8+
- PyTorch
- Transformers
- Sentence-Transformers
- Scikit-learn
- Gradio
- NumPy

Ver `requirements.txt` para versiones exactas.

---

## 📝 Licencia

Este proyecto está bajo la **licencia MIT**. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Soren Madsen**
- GitHub: [@Soren-Madsen](https://github.com/Soren-Madsen)
- Proyecto: Práctica Final RA3 - Análisis Predictivo

---

## 📚 Referencias

- [Hugging Face Spaces](https://huggingface.co/spaces)
- [Gradio Documentation](https://gradio.app/)
- [RAG Papers](https://arxiv.org/abs/2005.11401)
- [Sentence Transformers](https://www.sbert.net/)

---

**Última actualización:** Marzo 2026  
**Estado:** ✅ Producción - Fully Functional
