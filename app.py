from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.path.join( os.path.dirname(__file__), "students.db")

# Database Connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# CREATE - Add Student
@app.route('/students', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not data:
                return jsonify({
                    "success": False,
                    "message": "Request body is required."
                }), 400
        name = data.get('name')
        email = data.get('email')
        course = data.get('course')
        if not name or not email or not course:
            return jsonify({
                "success": False,
                "message": "Name, Email and Course are required."
            }), 400
        conn = get_db_connection()
        cursor = conn.execute(""" INSERT INTO students (name, email, course) VALUES (?, ?, ?)""",(name, email, course))
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()
        return jsonify({
            "status": "success",
            "message": "Student added successfully",
            "student": {
                "id": student_id,
                "name": name,
                "email": email,
                "course": course
            }
        }), 201
    except Exception as e:
        get_db_connection().connection.rollback()
        print(str(e))
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# READ - Get All Students
@app.route('/students', methods=['GET'])
def get_students():
    try:
        conn = get_db_connection()
        students = conn.execute("SELECT * FROM students").fetchall()
        conn.close()
        result = []
        for student in students:
            result.append({
                "id": student["id"],
                "name": student["name"],
                "email": student["email"],
                "course": student["course"]
            })
        return jsonify({
            "status": "success",
            "count": len(result),
            "students": result
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# UPDATE - Update Student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.get_json()
        if not data:
                return jsonify({
                    "success": False,
                    "message": "Request body is required."
                }), 400
        name = data.get('name')
        email = data.get('email')
        course = data.get('course')
        if not name or not email or not course:
            return jsonify({
                "success": False,
                "message": "Name, Email and Phone are required."
            }), 400
        conn = get_db_connection()
        cursor = conn.execute("""UPDATE students SET name = ?, email = ?, course = ? WHERE id = ?""",(name, email, course, id))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        if rows_affected == 0:
            return jsonify({
                "status": "error",
                "message": "Student not found"
            }), 404

        return jsonify({
            "status": "success",
            "message": "Student updated successfully",
            "student": {
                "id": id,
                "name": name,
                "email": email,
                "course": course
            }
        }), 200
    except Exception as e:
            get_db_connection().connection.rollback()
            print(str(e))
            return jsonify({
                "success": False,
                "message": str(e)
            }), 500

# DELETE - Delete Student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        conn = get_db_connection()
        cursor = conn.execute( "DELETE FROM students WHERE id = ?",(id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        if rows_affected == 0:
            return jsonify({
                "status": "error",
                "message": "Student not found"
            }), 404
        return jsonify({
            "status": "success",
            "message": "Student deleted successfully",
            "student_id": id
        }), 200
    except Exception as e:
        get_db_connection().connection.rollback()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
if __name__ == '__main__':
    conn = sqlite3.connect("students.db") 
    conn.execute(""" 
    CREATE TABLE IF NOT EXISTS students ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    email TEXT NOT NULL, 
    course TEXT NOT NULL 
    ) 
    """) 
    conn.commit() 
    conn.close() 
    app.run(debug=True)