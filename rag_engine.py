import json
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Cargar el modelo de embeddings
print("Cargando modelo de embeddings...")
embedding_model = SentenceTransformer("MongoDB/mdbr-leaf-ir")

# Cargar el modelo de lenguaje
print("Cargando modelo de lenguaje...")
tokenizer = AutoTokenizer.from_pretrained("PleIAs/Pleias-RAG-350M")
language_model = AutoModelForCausalLM.from_pretrained("PleIAs/Pleias-RAG-350M")

# Cargar documentos desde documents.json
print("Cargando documentos...")
with open("documents.json", "r", encoding="utf-8") as f:
    documentos = json.load(f)

# Crear lista de documentos y sus embeddings
documentos_lista = list(documentos.values())


print("Generando embeddings de documentos...")
documentos_embeddings = embedding_model.encode(documentos_lista, convert_to_tensor=False)


def recuperar_documentos(consulta, top_k=2, umbral=0.4):
    """
    Recupera los documentos más relevantes para una consulta dada.
    
    Args:
        consulta (str): Pregunta del usuario en inglés
        top_k (int): Número máximo de documentos a recuperar (default: 2)
        umbral (float): Valor mínimo de similitud (coseno) para considerar un documento relevante (default: 0.4)
    
    Returns:
        list: Lista con los textos de los documentos seleccionados
    """
    # 1. Calcular el embedding de la consulta
    consulta_embedding = embedding_model.encode([consulta], convert_to_tensor=False)
    
    # 2. Calcular la similitud del coseno entre el embedding de la consulta y los embeddings de los documentos
    similitudes = cosine_similarity(consulta_embedding, documentos_embeddings)[0]
    
    # 3. Ordenar los documentos de mayor a menor similitud
    # Crear lista de índices ordenados por similitud descendente
    indices_ordenados = np.argsort(similitudes)[::-1]
    
    # 4. Recorrer en ese orden y seleccionar aquellos cuya similitud sea >= umbral, hasta un máximo de top_k
    documentos_seleccionados = []
    for idx in indices_ordenados:
        if similitudes[idx] >= umbral and len(documentos_seleccionados) < top_k:
            documentos_seleccionados.append(documentos_lista[idx])
        elif len(documentos_seleccionados) >= top_k:
            break
    
    return documentos_seleccionados


def generar_respuesta(consulta, documentos_recuperados):
    """
    Genera una respuesta usando el modelo de lenguaje, inyectando los documentos recuperados como contexto.
    
    Args:
        consulta (str): Pregunta original del usuario
        documentos_recuperados (list): Lista de textos con los documentos relevantes
    
    Returns:
        str: Cadena con la respuesta generada
    """
    # 1. Concatenar todos los documentos en un solo string
    contexto = " ".join(documentos_recuperados)
    
    # 2. Construir el prompt con el formato especificado
    prompt = f"""Answer the question based only on the context provided. Provide a direct and factual answer.

Context: {contexto}

Question: {consulta}

Answer:"""
    
    # 3. Generar la respuesta con el modelo
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = language_model.generate(
            **inputs,
            max_new_tokens=50,
            num_return_sequences=1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    # Decodificar la respuesta completa
    respuesta_completa = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extraer solo la parte de la respuesta (después de "Answer:")
    if "Answer:" in respuesta_completa:
        respuesta = respuesta_completa.split("Answer:")[-1].strip()
    else:
        respuesta = respuesta_completa[len(prompt):].strip()
    
    # Buscar patrones comunes donde el modelo meta-explica y extraer la info útil
    if "is located at" in respuesta:
        # Extraer la parte que contiene "is located at"
        partes = respuesta.split("is located at")
        if len(partes) > 1:
            # Tomar desde el inicio hasta el final de la ubicación
            ubicacion = partes[1].split(".")[0] + "."
            respuesta = f"The hospital is located at{ubicacion}"
    
    # Limpiar la respuesta: tomar solo la primera oración o párrafo relevante
    # Eliminar texto adicional después de doble salto de línea o referencias
    if "\n\n" in respuesta:
        respuesta = respuesta.split("\n\n")[0].strip()
    
    # Eliminar referencias y texto extra común (expandir lista)
    separadores = [
        "<ref", "Trivial", "Le bureau", "The answer should", "I would structure",
        "¿", "However,", "While", "It's worth noting", "This is", "The sources",
        "The answer can be found", "which directly states", "Looking into",
        ", which directly", ", which "
    ]
    
    for separador in separadores:
        if separador in respuesta:
            partes = respuesta.split(separador)
            # Si hay contenido antes del separador, usarlo; sino, buscar el siguiente
            if partes[0].strip():
                respuesta = partes[0].strip()
                break
    
    # Limpiar puntos finales múltiples
    respuesta = respuesta.rstrip('.')
    if respuesta and not respuesta.endswith('.'):
        respuesta += '.'
    
    return respuesta

def preguntar(consulta, top_k=2, umbral=0.4):
    """
    Función de alto nivel que une la lógica de recuperar_documentos y generar_respuesta.
    
    Args:
        consulta (str): Pregunta del usuario en inglés
        top_k (int): Número máximo de documentos a recuperar (default: 2)
        umbral (float): Valor mínimo de similitud para considerar un documento relevante (default: 0.4)
    
    Returns:
        str: La respuesta generada
    """
    # Recuperar documentos relevantes
    documentos_recuperados = recuperar_documentos(consulta, top_k, umbral)
    
    # Generar respuesta con el contexto recuperado
    respuesta = generar_respuesta(consulta, documentos_recuperados)
    
    return respuesta

# PRUEBAS

if __name__ == "__main__":
    print("\n=== Probando el sistema RAG ===\n")
    
    # Prueba 1: recuperar_documentos
    print("1. Prueba de recuperar_documentos:")
    consulta_test = "What is the hospital email?"
    print(f"Consulta: {consulta_test}")
    
    documentos = recuperar_documentos(consulta_test, top_k=2, umbral=0.4)
    print(f"Documentos recuperados: {len(documentos)}")
    for i, doc in enumerate(documentos, 1):
        print(f"  {i}. {doc}")
    
    print("\n" + "="*80 + "\n")
    
    # Prueba 2: generar_respuesta
    print("2. Prueba de generar_respuesta:")
    if documentos:
        respuesta = generar_respuesta(consulta_test, documentos)
        print(f"Respuesta generada: {respuesta}")
    
    print("\n" + "="*80 + "\n")
    
    # Prueba 3: preguntar (función completa)
    print("3. Prueba de preguntar (función completa):")
    consultas_ejemplo = [
        "What is the hospital email?",
        "What are the working hours?",
        "Where is the hospital located?"
    ]
    
    for consulta in consultas_ejemplo:
        print(f"\nConsulta: {consulta}")
        respuesta = preguntar(consulta, top_k=2, umbral=0.4)
        print(f"Respuesta: {respuesta}")
        print("-" * 80)
