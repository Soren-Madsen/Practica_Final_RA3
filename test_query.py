#!/usr/bin/env python
"""
Script simple para probar el sistema RAG con tus propias preguntas.
"""

from rag_engine import preguntar, recuperar_documentos

def main():
    print("\n" + "="*80)
    print("🏥 SISTEMA RAG - PRUEBA INTERACTIVA")
    print("="*80 + "\n")
    
    while True:
        # Solicitar la pregunta
        consulta = input("\n💬 Escribe tu pregunta (o 'salir' para terminar): ").strip()
        
        if consulta.lower() in ['salir', 'exit', 'quit', 'q']:
            print("\n👋 ¡Hasta luego!\n")
            break
        
        if not consulta:
            print("⚠️  Por favor, escribe una pregunta válida.")
            continue
        
        # Solicitar parámetros (o usar valores por defecto)
        try:
            top_k_input = input("📊 Top K [default=2]: ").strip()
            top_k = int(top_k_input) if top_k_input else 2
            
            umbral_input = input("📏 Umbral [default=0.4]: ").strip()
            umbral = float(umbral_input) if umbral_input else 0.4
        except ValueError:
            print("⚠️  Valores inválidos. Usando valores por defecto (top_k=2, umbral=0.4)")
            top_k = 2
            umbral = 0.4
        
        print("\n" + "-"*80)
        print("🔍 Procesando tu consulta...\n")
        
        # Obtener documentos recuperados
        documentos = recuperar_documentos(consulta, top_k=top_k, umbral=umbral)
        
        print(f"📄 Documentos recuperados: {len(documentos)}")
        if documentos:
            for i, doc in enumerate(documentos, 1):
                print(f"\n  {i}. {doc}")
        else:
            print("\n  ⚠️  No se encontraron documentos relevantes con el umbral especificado.")
        
        print("\n" + "-"*80)
        
        # Generar respuesta completa
        respuesta = preguntar(consulta, top_k=top_k, umbral=umbral)
        
        print(f"\n💡 Respuesta:\n\n{respuesta}")
        print("\n" + "-"*80)


if __name__ == "__main__":
    main()
