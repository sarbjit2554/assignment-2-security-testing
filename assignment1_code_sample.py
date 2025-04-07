import os
import pymysql # type: ignore
from urllib.request import urlopen
import subprocess
from dotenv import load_dotenv
import ssl

# Load environment variables
load_dotenv()

# Get database credentials from environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_user_input():
    user_input = input('Enter your name: ').strip()
    # Sanitize user input to avoid issues (e.g., remove harmful characters)
    if not user_input.isalnum():
        raise ValueError("Invalid input! Please enter a valid name.")
    return user_input

def send_email(to, subject, body):
    # Replacing os.system() with subprocess.run() to prevent command injection
    command = f'echo "{body}" | mail -s "{subject}" {to}'
    subprocess.run(command, shell=True, check=True)

def get_data():
    # Use HTTPS for secure API requests
    url = 'https://insecure-api.com/get-data'
    
    # Use SSL context to avoid man-in-the-middle attacks
    context = ssl.create_default_context()
    response = urlopen(url, context=context)
    data = response.read().decode()
    
    return data

def save_to_db(data):
    # Use parameterized query to prevent SQL injection
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query, (data, 'Another Value'))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    try:
        user_input = get_user_input()
        data = get_data()
        save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
