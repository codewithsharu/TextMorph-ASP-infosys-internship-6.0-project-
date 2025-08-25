import random
import string
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all CORS requests

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'infosys'

mysql = MySQL(app)

def generate_unique_id(length=10):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET'])
def home():
    return test_connection()

@app.route('/register', methods=['POST'])
def register():
    # Accept JSON payload with username and password
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    # Store password in plain text (NOT RECOMMENDED FOR PRODUCTION)
    unique_id = generate_unique_id()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password, unique_id) VALUES (%s, %s, %s)", (username, password, unique_id))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'User registered successfully!', 'unique_id': unique_id})

@app.route('/login', methods=['POST'])
def login():
    # Accept JSON payload with username and password
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT password, unique_id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()

    if result:
        stored_password = result[0]
        unique_id = result[1]
        if password == stored_password:
            return jsonify({'message': 'Login successful!', 'unique_id': unique_id}), 200
        else:
            return jsonify({'message': 'Invalid username or password.'}), 401
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401

@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return jsonify({'message': 'Database connection is successful!'}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed!', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)