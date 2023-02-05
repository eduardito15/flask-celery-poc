# project/server/main/views.py


from flask import render_template, Blueprint, jsonify, request
from project.server.tasks import create_task
from celery.result import AsyncResult
from werkzeug.utils import secure_filename

main_blueprint = Blueprint("main", __name__,)

files=[]


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    task = create_task.delay(int(task_type))
    return jsonify({"task_id": task.id}), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200

@main_blueprint.route('/upload')
def upload_file_p():
   return render_template('upload.html')
	
@main_blueprint.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      open_file = open(f.filename, "r", encoding="utf8", errors='ignore')
      files.append(open_file.read())
      return 'file uploaded successfully'