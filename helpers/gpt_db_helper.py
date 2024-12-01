import openai
import cx_Oracle  # Use psycopg2 or other drivers for different databases

# OpenAI GPT setup
openai.api_key = "your_openai_api_key"

# Connect to an Oracle database
def connect_to_db(username, password, dsn):
    connection = cx_Oracle.connect(username, password, dsn)
    return connection

# Execute SQL Query
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results

# Generate SQL Query from Natural Language
def generate_sql_from_query(user_query, schema_info=""):
    prompt = f"""
You are an SQL expert. Generate a valid SQL query based on the user's natural language question and the following schema info:
{schema_info}

User query: {user_query}

SQL query:
"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()