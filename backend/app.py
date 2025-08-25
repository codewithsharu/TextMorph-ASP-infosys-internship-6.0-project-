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
  
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required.'}), 400

  
    unique_id = generate_unique_id()

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password, unique_id) VALUES (%s, %s, %s, %s)",
        (username, email, password, unique_id)
    )
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'User registered successfully!', 'unique_id': unique_id})

@app.route('/login', methods=['POST'])
def login():
   
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
          
            print(f"Login failed for user '{username}'. Provided password: '{password}', Stored password: '{stored_password}'")
            return jsonify({'message': 'Invalid username or password.'}), 401
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'message': 'Email is required.'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users WHERE email = %s", (email,))
    result = cur.fetchone()
    cur.close()

    if result:
       
        return jsonify({'message': 'Password reset link has been sent to your email.'}), 200
    else:
        return jsonify({'message': 'Email not found.'}), 404

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