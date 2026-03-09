from flask import Flask, request, jsonify


app = Flask(__name__)  #creamos la aplicación Flask.

tasks = [
    {"id": 1, "titulo": "Aprender Flask", "completada": False},
    {"id": 2, "titulo": "Construir un API CRUD", "completada": False}
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    
    new_task = {
        "id": max(t["id"] for t in tasks) + 1 if tasks else 1,
        "titulo": request.json['titulo'],
        "completada": request.json.get('completada', False)
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    data = request.json
    task['titulo'] = data.get('titulo', task['titulo'])
    task['completada'] = data.get('completada', task['completada'])
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"result": "Tarea eliminada"})

app.run(debug=True)