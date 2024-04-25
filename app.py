from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    """Create and return a database connection."""
    try:
        connection = mysql.connector.connect(
            #host='127.0.0.1', 
            #host='db', 
            host='host.docker.internal',
            database='GitHub', 
            user='root', 
            password='Bgmi@2023'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

@app.route('/data', methods=['GET'])
def get_data():
    """API endpoint to fetch data for a specific language from the database."""
    language = request.args.get('language', '')  # Get the language from query parameters
    if not language:
        return jsonify({"error": "No language specified"}), 400
    
    conn = get_db_connection()
    if conn is not None and conn.is_connected():
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT language_name, SUM(total_issue_count) as total_issue_count, 
                       MAX(total_repo_count) as total_repo_count
                FROM github_combined_data
                WHERE language_name = %s
                GROUP BY language_name;
            """
            #, SUM(total_prs_count) as total_prs_count
            cursor.execute(query, (language,))
            result = cursor.fetchall()  # Fetch all results since we expect one row per language
            cursor.close()
            conn.close()
            if result:
                # Assuming you want only the first result for simplicity
                return jsonify(result[0])
            else:
                return jsonify({"error": "No data found for the specified language"}), 404
        except Error as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Database connection failed"}), 500


@app.route('/select_language')
def select_language():
    return app.send_static_file('select_language.html')

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=6000)


# def get_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host='127.0.0.1',  # Could also be 'localhost'
#             user='root',
#             password='Bgmi@2023',
#             database='GitHub'  # Make sure this is the actual database name
#         )
#         return connection
#     except Error as e:
#         print(f"Error connecting to MySQL database: {e}")
#         return None


# @app.route('/')
# def home():
#     return 'Welcome to my Flask app!'

# @app.route('/data', methods=['GET'])
# def get_data():
#     """API endpoint to fetch data from the database."""
#     conn = get_db_connection()
#     if conn is not None and conn.is_connected():
#         try:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM GitHub.github_combined_data LIMIT 5;")  # Fetch first 5 entries
#             rows = cursor.fetchall()
#             # Close connection resources
#             cursor.close()
#             conn.close()
#             # Convert query results to a list of dictionaries to return as JSON
#             columns = cursor.column_names
#             result = [dict(zip(columns, row)) for row in rows]
#             return jsonify(result)
#         except Error as e:
#             return jsonify({"error": str(e)}), 500
#     else:
#         return jsonify({"error": "Database connection failed"}), 500



# @app.route('/data/<language>', methods=['GET'])
# def get_language_data(language):
#     """API endpoint to fetch data for a specific language from the database."""
#     conn = get_db_connection()
#     if conn is not None and conn.is_connected():
#         try:
#             cursor = conn.cursor(dictionary=True)
#             # Adjusted query: now selecting distinct repo_count for the language
#             query = """
#                 SELECT language_name, SUM(total_issue_count) as total_issue_count, 
#                        MAX(total_repo_count) as total_repo_count, SUM(total_prs_count) as total_prs_count
#                 FROM github_combined_data
#                 WHERE language_name = %s
#                 GROUP BY language_name;
#             """
#             cursor.execute(query, (language,))
#             result = cursor.fetchone()  # Fetch the first row only since language_name should be unique
#             cursor.close()
#             conn.close()
#             if result:
#                 return jsonify(result)
#             else:
#                 return jsonify({"error": "No data found for the specified language"}), 404
#         except Error as e:
#             return jsonify({"error": str(e)}), 500
#     else:
#         return jsonify({"error": "Database connection failed"}), 500


# app = Flask(__name__)

# Your database connection and route definitions here

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)
# def get_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host='db',  # This matches the service name in docker-compose.yml
#             database='GitHub', 
#             user='root', 
#             password='Bgmi@2023'
#         )
#         return connection
#     except Error as e:
#         print(f"Error connecting to MySQL database: {e}")
#         return None

# from flask import Flask, jsonify
# import mysql.connector
