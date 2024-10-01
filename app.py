from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'db',  
    'user': 'root',
    'password': 'passwordtest',
    'database': 'test_db'
}

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(255) UNIQUE NOT NULL,
                            password VARCHAR(255) NOT NULL
                        )''')

        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        return jsonify({"message": "Inscription réussie!", "username": username}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur est survenue: " + str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Récupérer les résultats sous forme de dictionnaires

        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        return jsonify(users), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur est survenue: " + str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
