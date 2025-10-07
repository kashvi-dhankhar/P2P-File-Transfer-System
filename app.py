from flask import Flask, request, jsonify, render_template, send_from_directory, abort
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

AUTHORIZED_RECEIVER = None 

@app.route("/")
def home():
    return render_template("test.html")

@app.route("/connect", methods=["POST"])
def connect():
    global AUTHORIZED_RECEIVER
    data = request.get_json()
    ip1 = data.get("ip1")
    ip2 = data.get("ip2")
    AUTHORIZED_RECEIVER = ip2  
    print(f"[+] Trying to connect from {ip1} to {ip2}")

    try:
        result = subprocess.run(["ping", "-c", "2", ip2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"[+] Connection established between {ip1} and {ip2}")
            return jsonify({"success": True})
        else:
            print(f"[-] Connection failed between {ip1} and {ip2}")
            return jsonify({"success": False})
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({"success": False})

@app.route("/disconnect", methods=["POST"])
def disconnect():
    global AUTHORIZED_RECEIVER
    AUTHORIZED_RECEIVER = None
    return jsonify({"success": True, "message": "connection terminated successfully"})

@app.route("/upload", methods=["POST"])
def upload_file():
    files = request.files.getlist("file")
    if not files:
        return "No files uploaded"

    saved_files = []
    errors = []

    for file in files:
        if file.filename == '':
            continue
        try:
            save_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(save_path)
            saved_files.append(file.filename)
        except Exception as e:
            errors.append(f"{file.filename}: {e}")

    if errors:
        return f"Some files failed:\n{errors}\nUploaded files:\n{saved_files}"

    download_links = [f'<a href="/files/{fname}" target="_blank">{fname}</a>' for fname in saved_files]
    return "Files uploaded successfully:<br>" + "<br>".join(download_links)

@app.route("/files")
def list_files():
    client_ip = request.remote_addr
    if AUTHORIZED_RECEIVER and client_ip != AUTHORIZED_RECEIVER:
        abort(403, "You are not authorized to view this page.")

    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        return "<h3>No files uploaded yet.</h3>"

    file_links = [f'<a href="/files/{fname}" target="_blank">{fname}</a>' for fname in files]
    return "<h3>Uploaded Files:</h3><br>" + "<br>".join(file_links)

@app.route("/files/<filename>")
def get_file(filename):
    client_ip = request.remote_addr
    if AUTHORIZED_RECEIVER and client_ip != AUTHORIZED_RECEIVER:
        abort(403, "You are not authorized to access this file.")
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
