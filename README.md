# FileFlow

## Overview
FileFlow is a web-based application for secure file management. It enables users to upload, preview, download, and manage files with additional support for administrative oversight. Key features include file protection, user authentication, and administrative controls.

---

## Features

### General Features:
- **File Upload**: Upload multiple files of allowed types.
- **File Preview**: Preview files directly on the platform.
- **File Download**: Securely download files, with optional access restrictions.
- **User Authentication**: Email and password-based authentication for secure file access.
- **Admin Dashboard**: Admins can view and manage files and user details.

### User Features:
- **File Protection**: Option to protect files with user authentication.
- **User Session Management**: Seamless session handling for secure file operations.
- **Preview and Download Files**: Access and download uploaded files as per permissions.

### Admin Features:
- **Admin Login**: Authenticate and log in to access admin privileges.
- **Admin Dashboard**: View and manage files uploaded by users, including details such as file ownership.
- **Change Password**: Admins can securely change their passwords.

---

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/daksh-deep/FileFlow
   cd fileflow
   ```

2. **Install Dependencies**:
   ```bash
   pip install flask, mysql-connector-python
   ```

3. **Setup MySQL Database**:
   - Configure MySQL credentials in the `db_config` section of `app.py`.
   - Ensure MySQL server is running and accessible.

4. **Run the Application**:
   ```python
   python app.py
   ```

5. **Access the Application**:
   Open your web browser and navigate to:
   ```bash
   http://localhost:5000/
   ```

---

## Folder Structure
- **app.py**: Main application script.
- **templates/**: HTML templates for rendering the web pages.
- **static/**: Static assets (CSS, JavaScript, images).
- **uploads/**: Directory to store uploaded files.

---

## Admin Credentials
Upon initial setup, the following admin accounts are created:

| Name              | Email                    | Default Password |
|-------------------|--------------------------|------------------|
| Daksh Deep        | daksh@fileflow.com       | admin            |
| Yashvi Arya       | yashvi@fileflow.com      | admin            |


> **Note**: Admins are advised to change their passwords after the initial login.

---

## Key Routes

### User Routes
| Route                   | Method | Description                           |
|-------------------------|--------|---------------------------------------|
| `/`                     | GET    | Home page                            |
| `/upload`               | GET/POST | Upload files                        |
| `/document`             | GET    | View list of uploaded files          |
| `/download/<filename>`  | GET    | Download a specific file             |
| `/preview/<filename>`   | GET    | Preview a specific file              |
| `/authenticate`         | GET/POST | Authenticate user for file access   |
| `/about`                | GET    | About the application                |

### Admin Routes
| Route                     | Method | Description                           |
|---------------------------|--------|---------------------------------------|
| `/admin_login`            | GET/POST | Admin login page                    |
| `/admin_change_password`  | GET/POST | Change admin password               |

---

## Database Schema

### Tables
1. **User Table**:
   - **User_ID**: Auto-increment primary key.
   - **Email**: Unique email address.
   - **Password**: Encrypted user password.

2. **Files Table**:
   - **File_ID**: Auto-increment primary key.
   - **File_Name**: Name of the uploaded file.
   - **Protected**: Boolean indicating file protection status.
   - **User_ID**: Foreign key referencing the User table.

3. **Admin_User Table**:
   - **Admin_ID**: Auto-increment primary key.
   - **Name**: Name of the admin.
   - **Email**: Unique email address.
   - **Password**: Encrypted admin password.

---

## Security
- Passwords are securely hashed before being stored in the database.
- Session management ensures secure and private user interactions.

---

## Contributing
We welcome contributions to improve FileFlow. Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

---

## License
FileFlow is licensed under the MIT License. See the LICENSE file for more details.

---

## Contact
For any inquiries or support, please contact:
- **Daksh Deep**: [dakshsaxena04@gmail.com](mailto:dakshsaxena04@gmail.com)

