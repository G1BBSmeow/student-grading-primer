from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    all_students = db.get_all_students()
    return jsonify(all_students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    student_data = request.json

    if student_data is None:
        return jsonify({"error": "Missing student data"}), 404

    student_name = student_data.get("name")
    student_course = student_data.get("course")
    student_mark = student_data.get("mark", 0)

    if student_name is None:
        return jsonify({"error": "Student name is required"}), 404
    
    if student_course is None:
        return jsonify({"error": "Student course is required"}), 404

    try:
        student_mark = int(student_mark)
    except (TypeError, ValueError):
        return jsonify({"error": "Student mark must be an integer"}), 404

    created_student = db.insert_student(student_name, student_course, student_mark)
    return jsonify(created_student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json

    if student_data is None:
        return jsonify({"error": "Missing student data"}), 404

    student_mark = student_data.get("mark")

    if student_mark is not None:
        try:
            student_mark = int(student_mark)
        except (TypeError, ValueError):
            return jsonify({"error": "Student mark must be an integer"}), 404

    updated_student = db.update_student(
        student_id,
        name=student_data.get("name"),
        course=student_data.get("course"),
        mark=student_mark,
    )

    if updated_student is None:
        return jsonify({"error": "Student to update does not exist"}), 404

    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student_to_delete = db.delete_student(student_id)

    if student_to_delete is None:
        return jsonify({"error": "Student to delete not found"}), 404
    
    return jsonify(student_to_delete), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    all_students = db.get_all_students()
    all_student_marks = [current_student["mark"] for current_student in all_students]

    if len(all_student_marks) == 0:
        return jsonify({
            "count": 0,
            "average": 0,
            "min": None,
            "max": None,
    }), 200

    mark_stats = {
        "count": len(all_student_marks),
        "average": sum(all_student_marks) / len(all_student_marks),
        "min": min(all_student_marks),
        "max": max(all_student_marks),
    }
    
    return jsonify(mark_stats), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
