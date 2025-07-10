from flask import request, jsonify
from logic.notas import (
    read_excel_data, excel_url,
    get_student_average,
    get_all_students,
    get_student_assesment_grade,
    get_student_type_assesment_grade,
    get_general_average,
    get_all_student_average,
    get_all_student_average_sorted
)

df = read_excel_data(excel_url)

def register_routes(app):
    @app.route('/')
    def home():
        return "<h1>Base url!</h1>"

    @app.route('/api/promedio_estudiante', methods=['GET'])
    def get_info_student_endpoint():
        nombre = request.args.get('nombre')
        if not nombre:
            return jsonify({"error": "Falta el parámetro 'nombre'"}), 400
        try:
            result = get_student_average(df, nombre)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/todos_estudiantes', methods=['GET'])
    def get_all_students_endpoint():
        try:
            result = get_all_students(df)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/estudiante_evaluacion', methods=['GET'])
    def get_student_assessment_endpoint():
        nombre = request.args.get('nombre')
        evaluacion = request.args.get('evaluacion')
        if not nombre or not evaluacion:
            return jsonify({"error": "Faltan los parámetros 'nombre' o 'evaluacion'"}), 400
        try:
            result = get_student_assesment_grade(df, nombre, evaluacion)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/estudiante_evaluacion_tipo', methods=['GET'])
    def get_student_type_assessment_endpoint():
        nombre = request.args.get('nombre')
        tipo = request.args.get('tipo')
        if not nombre or not tipo:
            return jsonify({"error": "Faltan los parámetros 'nombre' o 'tipo'"}), 400
        try:
            result = get_student_type_assesment_grade(df, nombre, tipo)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/promedio_general', methods=['GET'])
    def get_general_average_endpoint():
        try:
            result = get_general_average(df)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/promedio_todos_estudiantes', methods=['GET'])
    def get_all_student_average_endpoint():
        try:
            result = get_all_student_average(df)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/promedio_todos_estudiantes_ordenado', methods=['GET'])
    def get_all_student_average_sorted_endpoint():
        ascending = request.args.get('ascending', 'true').lower() == 'true'
        try:
            result = get_all_student_average_sorted(df, ascending=ascending)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500
