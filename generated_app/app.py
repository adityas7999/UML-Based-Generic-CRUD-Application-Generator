from flask import Flask, request, jsonify
from flasgger import Swagger
import repository as repo

app = Flask(__name__)

# Swagger Setup
swagger = Swagger(app, template={
    "info": {
        "title": "Auto-Generated MDE API",
        "description": "REST API generated from UML Class Diagram",
        "version": "1.0.0"
    }
})

# ==========================================
# Student API Endpoints
# ==========================================

@app.route('/student', methods=['POST'])
def create_student():
    """
    Create Student
    ---
    tags:
      - Student
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
          example:
            name: "string"
    responses:
      201:
        description: Created successfully
      400:
        description: Missing fields
      500:
        description: Server error
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required_fields = ["name"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        success = repo.insert_student(            data.get("name")        )

        if success:
            return jsonify({"message": "Student created"}), 201
        return jsonify({"error": "Insert failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/student', methods=['GET'])
def get_all_student():
    """
    Get all Student
    ---
    tags:
      - Student
    responses:
      200:
        description: List of Student
      500:
        description: Server error
    """
    try:
        data = repo.get_all_student()
        return jsonify(data or []), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/student/<string:id>', methods=['GET'])
def get_student(id):
    """
    Get Student by id
    ---
    tags:
      - Student
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Record found
      404:
        description: Not found
    """
    try:
        data = repo.get_student_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/student/<string:id>', methods=['PUT'])
def update_student(id):
    """
    Update Student
    ---
    tags:
      - Student
    parameters:
      - name: id
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
          example:
            name: "string"
    responses:
      200:
        description: Updated successfully
      400:
        description: Invalid input
      500:
        description: Server error
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No update data provided"}), 400

    try:
        success = repo.update_student(
            id,            data.get("name")        )

        if success:
            return jsonify({"message": "Student updated"}), 200
        return jsonify({"error": "Update failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/student/<string:id>', methods=['DELETE'])
def delete_student(id):
    """
    Delete Student
    ---
    tags:
      - Student
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Deleted successfully
      500:
        description: Server error
    """
    try:
        success = repo.delete_student(id)

        if success:
            return jsonify({"message": "Student deleted"}), 200
        return jsonify({"error": "Delete failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
