import os
import mysql.connector

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'daksh',
    'database': 'fileflow'
}

def connect_to_mysql():
    try:
        # Establish a connection to the MySQL server
        cnx = mysql.connector.connect(**db_config)
        return cnx

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def drop_tables():
    try:
        cnx = connect_to_mysql()
        cursor = cnx.cursor()

        # Drop Files table
        cursor.execute("DROP TABLE IF EXISTS Files")
        print("Drop Table: Files")

        # Drop User table
        cursor.execute("DROP TABLE IF EXISTS User")
        print("Drop Table: User")

        # Drop Admin table
        cursor.execute("DROP TABLE IF EXISTS Admin_User")
        print("Drop Table: Admin_User")


        cnx.commit()
        cursor.close()
        cnx.close()
        print("Exit Code: 0 (Success)")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def delete_files_in_folder(folder_path):
    # Get list of all files in the folder
    files = os.listdir(folder_path)
    
    # Iterate over each file and delete it

    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            os.remove(file_path)
            print(f"File '{file}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting file '{file}': {e}")

if __name__ == "__main__":
    folder_path = r"E:\Personal Projects\File Flow Codebase\File Flow Extended (UI Change)\uploads"  # Path to your uploads folder
    delete_files_in_folder(folder_path)
    drop_tables()
    print("System ready for Reboot")

