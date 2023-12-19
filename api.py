from flask import Flask, request, jsonify, render_template, send_from_directory
from DataBase import DataBase

app = Flask(__name__, static_folder='image')
db = DataBase('basa.db')

@app.route("/")
def index():
    workers = db.get_workers()
    requests = db.get_all_requests()
    print(requests)
    return render_template("index.html", workers=workers, requests=requests)

@app.route("/api/add_worker", methods=["POST"])
def add_worker():
    try:
        data = request.get_json()
        db.add_worker(data.get("role"), data.get("vk"), data.get("mark"), data.get("note"))
        print(data.get("role"), data.get("vk"), data.get("mark"), data.get("note"))
        response = {'status': 'success', 'message': 'Worker added successfully'}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route("/api/delete_worker", methods=["POST"])
def delete_worker():
    try:
        data = request.get_json()
        db.delete_worker(data.get("vk_id"))
        print(data.get("vk"))
        response = {'status': 'success', 'message': 'Worker deleted successfully'}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500


@app.route("/api/existence_worker", methods=["POST"])
def existence_worker():
    try:
        data = request.get_json()
        ret = db.existence_worker(data.get("vk_id"))
        print(data.get("vk_id"))
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500
    
@app.route("/api/send_notification_to_worker", methods=["POST"])
def send_notification_to_worker():
    try:
        data = request.get_json()
        ret = db.send_notification_to_worker(data.get("role"))
        print(data.get("role"))
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route("/api/existence_captain", methods=["POST"])
def existence_captain():
    try:
        data = request.get_json()
        ret = db.existence_captain(data.get("vk_id"))
        print(data.get("vk_id"))
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500


@app.route("/api/adding_captain_to_the_check", methods=["POST"])
def adding_captain_to_the_check():
    try:
        data = request.get_json()
        ret = db.adding_captain_to_the_check(data.get("vk_id"), data.get("link"))
        print(data.get("vk_id"), data.get("link"))
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route("/api/removal_captain_to_the_check", methods=["POST"])
def removal_captain_to_the_check():
    try:
        data = request.get_json()
        ret = db.removal_captain_to_the_check(data.get("vk_id"))
        print(data.get("vk_id"))
        response = {'status': 'success', 'message': "Deleted captain to check success"}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route("/api/adding_captain", methods=["POST"])
def adding_captain():
    try:
        data = request.get_json()
        ret = db.adding_captain(data.get("vk_id"), data.get("link"))
        print(data.get("vk_id"), data.get("link"))
        response = {'status': 'success', 'message': "Deleted adding success"}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500


@app.route("/api/get_captains_to_the_check", methods=["POST"])
def get_captains_to_the_check():
    try:
        data = request.get_json()
        ret = db.get_captains_to_the_check(data.get("vk_id"), data.get("link"))
        print(data.get("vk_id"), data.get("link"))
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500
    

@app.route("/api/add_request", methods=["POST"])
def add_request():
    try:
        data = request.get_json()
        ret = db.add_request(data.get("captain"), data.get("project"), data.get("worker"), data.get("bet"), data.get("condition"), data.get("other"))
        print(data.get("captain"), data.get("project"), data.get("worker"), data.get("bet"), data.get("condition"), data.get("other"))
        response = {'status': 'success', 'message': "Request add succesful"}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route("/api/get_requests", methods=["POST"])
def get_requests():
    try:
        data = request.get_json()
        ret = db.get_requests(data.get("worker"))
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500

@app.route("/api/delete_request", methods=["POST"])
def delete_request():
    try:
        data = request.get_json()
        ret = db.delete_request(data.get("id"))
        response = {'status': 'success', 'message': "Delete request succesful"}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500


@app.route("/api/get_workers", methods=["POST"])
def get_workers():
    try:
        data = request.get_json()
        ret = db.get_workers()
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500


@app.route("/api/existence_request", methods=["POST"])
def existence_request():
    try:
        data = request.get_json()
        ret = db.existence_request(data.get("id"))
        response = {'status': 'success', 'message': ret}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500


@app.route("/api/update_date", methods=["POST"])
def update_date():
    try:
        data = request.get_json()
        ret = db.update_date(data.get("id"))
        response = {'status': 'success', 'message': "Update date succesful"}
        return jsonify(response)
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response), 500
  