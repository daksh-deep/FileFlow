from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os
import mysql.connector
from flask import session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'pptx', 'docs'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'daksh',
    'database': 'fileflow'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def connect_to_mysql():
    try:
        # Establish a connection to the MySQL server
        cnx = mysql.connector.connect(**db_config)
        return cnx

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_tables():
    try:
        cnx = connect_to_mysql()
        cursor = cnx.cursor()

        # Create User table
        cursor.execute("""CREATE TABLE IF NOT EXISTS User (
                            User_ID INT AUTO_INCREMENT PRIMARY KEY,
                            Email VARCHAR(255) UNIQUE NOT NULL,
                            Password VARCHAR(255) NOT NULL
                        )""")

        # Create Files table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Files (
                            File_ID INT AUTO_INCREMENT PRIMARY KEY,
                            File_Name VARCHAR(255) NOT NULL,
                            Protected BOOLEAN NOT NULL,
                            User_ID INT,
                            FOREIGN KEY (User_ID) REFERENCES User(User_ID)
                        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Admin_User (
                            admin_ID INT AUTO_INCREMENT PRIMARY KEY,
                            Name VARCHAR(255) NOT NULL,
                            email VARCHAR(255) UNIQUE NOT NULL,
                            password VARCHAR(255) NOT NULL
                        )""")

        cnx.commit()
        cursor.close()
        cnx.close()
        print("Tables created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def initiate_admin():
    try:
        cnx = connect_to_mysql()
        cursor = cnx.cursor()
        cursor.execute("""INSERT INTO Admin_User (Name, email, password) 
                        VALUES
                            ('Daksh', 'daksh@fileflow.com', 'admin'),
                            ('Yashvi', 'yashvi@fileflow.com', 'admin'),
                            ('Anju Yadav', 'anju@fileflow.com', 'admin'),
                            ('Kavita Jhajharia', 'kavita@fileflow.com', 'admin'),
                            ('Shikha Chaudhary', 'shikha@fileflow.com', 'admin'
                            )""")
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Default Admin Data Supplied (to database)")
        print("Default Password : admin")

    except mysql.connector.Error as err:
        print("Default Admin Data was NOT Supplied")

@app.route('/')
def home():
    session.pop('user_id', None)
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'files' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('files')
        for file in files:
            if file.filename == '':
                return render_template('upload.html', error='No selected file')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Insert file info into database
                cnx = connect_to_mysql()
                cursor = cnx.cursor()

                # Check if "Protect my files" checkbox is checked
                protected = request.form.get('protectFiles') == 'on'

                # Insert or retrieve user ID if files are protected
                if protected:
                    email = request.form.get('email')
                    password = request.form.get('password')
                    cursor.execute("SELECT User_ID FROM User WHERE Email = %s", (email,))
                    user_id = cursor.fetchone()
                    if user_id is None:
                        cursor.execute("INSERT INTO User (Email, Password) VALUES (%s, %s)", (email, password))
                        cnx.commit()
                        user_id = cursor.lastrowid
                    else:
                        user_id = user_id[0]
                else:
                    user_id = None

                # Insert file info into database
                cursor.execute("INSERT INTO Files (File_Name, Protected, User_ID) VALUES (%s, %s, %s)", (filename, protected, user_id))
                file_id = cursor.lastrowid

                cnx.commit()
                cursor.close()
                cnx.close()

        return render_template('upload.html', message="Files uploaded successfully.")

    return render_template('upload.html')

@app.route('/document')
def document():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_size = os.path.getsize(filepath)
        file_size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024 else f"{file_size / (1024 * 1024):.2f} MB"
        files.append({'name': filename, 'size': file_size_str, 'type': filename.rsplit('.', 1)[1].lower()})

    return render_template('document.html', files=files)


@app.route('/download/<filename>')
def download(filename):
    cnx = connect_to_mysql()
    cursor = cnx.cursor()

    cursor.execute("SELECT Protected FROM Files WHERE File_Name = %s", (filename,))
    result = cursor.fetchone()

    if result and result[0]:  # If file is protected
        if 'user_id' not in session:
            return redirect(url_for('authenticate', filename=filename))
        else:
            cursor.execute("SELECT User_ID FROM Files WHERE File_Name = %s", (filename,))
            owner_id = cursor.fetchone()[0]
            if session['user_id'] != owner_id:
                return "You are not authorized to download this file."
    
    cursor.close()
    cnx.close()
    session.pop('user_id', None)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/preview/<filename>')
def preview(filename):
    cnx = connect_to_mysql()
    cursor = cnx.cursor()

    cursor.execute("SELECT Protected FROM Files WHERE File_Name = %s", (filename,))
    result = cursor.fetchone()

    if result and result[0]:  # If file is protected
        if 'user_id' not in session:
            return redirect(url_for('authenticate', filename=filename))
        else:
            cursor.execute("SELECT User_ID FROM Files WHERE File_Name = %s", (filename,))
            owner_id = cursor.fetchone()[0]
            if session['user_id'] != owner_id:
                return "You are not authorized to preview this file."
    
    cursor.close()
    cnx.close()
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cnx = connect_to_mysql()
        cursor = cnx.cursor()

        cursor.execute("SELECT User_ID FROM User WHERE Email = %s AND Password = %s", (email, password))
        result = cursor.fetchone()

        if result:
            session['user_id'] = result[0]
            return redirect(url_for('download', filename=request.args.get('filename')))

        return render_template('authenticate.html', error='Wrong Credentials')

    return render_template('authenticate.html')

@app.route('/about')
def about():
    return render_template('about.html')


# Admin Routes
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or password is None:
            return render_template('admin_login.html', error='Please provide both email and password.')

        # Query to check if the entered credentials match any admin user in the database
        cnx = connect_to_mysql()
        cursor = cnx.cursor()

        query = "SELECT COUNT(*) FROM Admin_User WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        admin_exists = cursor.fetchone()[0]
        cursor.close()
        cnx.close()

        if admin_exists:

            # Get Admin Nmae
            cnx = connect_to_mysql()
            cursor = cnx.cursor()
            query = "select Name from Admin_User where email= %s AND password = %s"
            cursor.execute(query,(email, password))
            admin_name = cursor.fetchone()[0]
            cursor.close()

            # Query to perform LEFT JOIN of Files and User tables (excluding password column)
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT Files.File_ID, Files.File_Name, Files.Protected, User.User_ID, User.Email
                FROM Files
                LEFT JOIN User ON Files.User_ID = User.User_ID
            """
            cursor.execute(query)
            files_user_data = cursor.fetchall()
            cnx.close()

            return render_template('admin_table.html', files_user_data=files_user_data, admin_name=admin_name)

        else:
            return render_template('admin_login.html', error='Incorrect email or password')

    return render_template('admin_login.html')

@app.route('/admin_change_password', methods=['GET', 'POST'])
def admin_change_password():
    error = None
    
    if request.method == 'POST':
        email = request.form['email']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        cnx = connect_to_mysql()
        cursor = cnx.cursor()

        # Check if the email and current password match in the database
        cursor.execute("SELECT * FROM Admin_User WHERE email = %s AND password = %s", (email, current_password))
        user = cursor.fetchone()

        if user:
            # Update the password
            cursor.execute("UPDATE Admin_User SET password = %s WHERE email = %s", (new_password, email))
            cnx.commit()
            cnx.close()
            return render_template('admin_change_password.html', message="Password changed successfully!")
        else:
            cnx.close()
            error = "Incorrect email or password."

    return render_template('admin_change_password.html', error=error)

if __name__ == '__main__':
    create_tables()
    initiate_admin()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
