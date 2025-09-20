from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

# Mounted IP2 folder
UPLOAD_FOLDER = "/Volumes/kashvi123"

@app.route("/")
def home():
    return render_template("test.html")

@app.route("/connect", methods=["POST"])
def connect():
    data = request.get_json()
    ip1 = data.get("ip1")
    ip2 = data.get("ip2")
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
    return f"All files uploaded successfully: {saved_files}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
