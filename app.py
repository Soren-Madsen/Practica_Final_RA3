import gradio as gr
from rag_engine import recuperar_documentos, generar_respuesta


def ask(query, top_k, umbral):
    """
    Función principal que procesa la consulta del usuario y retorna la respuesta y documentos.
    
    Args:
        query (str): La pregunta del usuario
        top_k (int): Número de documentos a recuperar
        umbral (float): Umbral de similitud
    
    Returns:
        tuple: (respuesta, docs_formateados)
    """
    if not query or query.strip() == "":
        return "Por favor, ingresa una pregunta.", ""
    
    try:
        # Recuperar documentos relevantes
        documentos_recuperados = recuperar_documentos(query, top_k=int(top_k), umbral=float(umbral))
        
        # Generar respuesta usando el modelo de lenguaje
        respuesta = generar_respuesta(query, documentos_recuperados)
        
        # Formatear documentos recuperados para mostrarlos de forma legible
        if documentos_recuperados:
            docs_formateados = "\n\n---\n\n".join(documentos_recuperados)
        else:
            docs_formateados = "No se encontraron documentos relevantes con el umbral especificado."
        
        return respuesta, docs_formateados
    
    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}", ""


# Crear la interfaz Gradio
with gr.Blocks(title="Chat RAG") as demo:
    # Título y descripción
    gr.Markdown(
        """
        # Chat RAG 
        
        Este sistema utiliza RAG para responder preguntas sobre información hospitalaria.

        El sistema recupera documentos relevantes y genera respuestas basadas únicamente en el contexto proporcionado.
        
        **Instrucciones:** Escribe tu pregunta en inglés, ajusta los parámetros si lo deseas, y haz clic en "Enviar".
        """
    )
    
    with gr.Row():
        with gr.Column():
            # Input: Pregunta del usuario
            query_input = gr.Textbox(
                label="Pregunta",
                placeholder="Ejemplo: What is the hospital email?",
                lines=2
            )
            
            # Input: Slider para top_k
            top_k_slider = gr.Slider(
                minimum=1,
                maximum=5,
                value=1,
                step=1,
                label="Top K - documentos"
            )
            
            # Input: Slider para umbral
            umbral_slider = gr.Slider(
                minimum=0.0,
                maximum=1.0,
                value=0.55,
                step=0.05,
                label="Umbral de similitud"
            )
            
            # Botón Enviar
            submit_btn = gr.Button("Enviar", variant="primary")
        
        with gr.Column():
            # Output: Respuesta generada
            respuesta_output = gr.Textbox(
                label="Respuesta",
                lines=3,
                interactive=False
            )
            
            # Output: Documentos recuperados
            docs_output = gr.Textbox(
                label="Documentos recuperados",
                lines=6,
                max_lines=15,
                interactive=False
            )
    
    # Conectar el botón con la función ask
    submit_btn.click(
        fn=ask,
        inputs=[query_input, top_k_slider, umbral_slider],
        outputs=[respuesta_output, docs_output]
    )

# Lanzar la interfaz
if __name__ == "__main__":
    demo.launch()
