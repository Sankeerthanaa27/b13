from flask import Flask, request, render_template, send_file, redirect, url_for
import os

app = Flask(__name__)

# ========= STORAGE =========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========= HOSPITALS =========
HOSPITALS = ["Apollo Hospital", "AIIMS Hospital", "KIMS Hospital"]

# ========= ACCESS CONTROL =========
ACCESS = {}  # patient_id -> hospital

# ========= ROUTES =========

@app.route("/")
def main():
    return render_template("main.html")


@app.route("/upload_page")
def upload_page():
    return render_template("upload.html", hospitals=HOSPITALS)


@app.route("/download_page")
def download_page():
    return render_template("download.html", hospitals=HOSPITALS)


# ========= UPLOAD =========
@app.route("/upload", methods=["POST"])
def upload():
    patient_id = request.form.get("patient_id", "").strip()
    hospital = request.form.get("hospital")
    file = request.files.get("file")

    if not patient_id or not hospital or not file:
        return "Missing details"

    filename = patient_id + "_" + file.filename.replace(" ", "_")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    ACCESS[patient_id] = hospital

    return redirect(url_for("main"))


# ========= DOWNLOAD =========
@app.route("/download", methods=["POST"])
def download():
    patient_id = request.form.get("patient_id", "").strip()
    hospital = request.form.get("hospital")

    if ACCESS.get(patient_id) != hospital:
        return "Access Denied"

    for f in os.listdir(UPLOAD_FOLDER):
        if f.startswith(patient_id + "_"):
            return send_file(os.path.join(UPLOAD_FOLDER, f), as_attachment=True)

    return "File not found"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
