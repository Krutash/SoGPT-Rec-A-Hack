from flask import Flask, request, render_template, jsonify
import os
from helpers.gpt_git_helper import clone_repo, list_repo_files, summarize_repo_file
from helpers.gpt_db_helper import connect_to_db, execute_query, generate_sql_from_query
from helpers.gpt_doc_helper import summarize_document, analyze_document

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Global repository and database connections
LOCAL_REPO_PATH = "./repo"
DB_CONNECTION = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        context = request.form.get("context")  # 'repository', 'database', or 'documents'
        response = ""

        if context == "repository":
            file_name = request.form.get("file_name")
            file_path = os.path.join(LOCAL_REPO_PATH, file_name)
            response = summarize_repo_file(file_path)

        elif context == "database":
            sql_query = generate_sql_from_query(user_input)
            results = execute_query(DB_CONNECTION, sql_query)
            response = {"query": sql_query, "results": results}

        elif context == "documents":
            uploaded_file = request.files.get("file")
            if uploaded_file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)
                response = summarize_document(file_path)

        return jsonify({"response": response})

    return render_template("index.html")

@app.route("/setup_repo", methods=["POST"])
def setup_repo():
    repo_url = request.form.get("repo_url")
    clone_repo(repo_url, LOCAL_REPO_PATH)
    files = list_repo_files(LOCAL_REPO_PATH)
    return jsonify({"files": files})

@app.route("/setup_db", methods=["POST"])
def setup_db():
    global DB_CONNECTION
    username = request.form.get("username")
    password = request.form.get("password")
    dsn = request.form.get("dsn")
    DB_CONNECTION = connect_to_db(username, password, dsn)
    return jsonify({"status": "Database connected!"})