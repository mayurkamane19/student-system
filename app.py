from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)
FILE = "students.json"

# ---------- Load ----------
def load():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return []

# ---------- Save ----------
def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Auto ID ----------
def get_id(data):
    if not data:
        return 1
    return int(data[-1]["id"]) + 1

# ---------- HOME ----------
@app.route("/", methods=["GET", "POST"])
def index():
    data = load()

    # ADD
    if request.method == "POST":
        name = request.form["name"]
        course = request.form["course"]
        fee = request.form["fee"]
        status = request.form["status"]

        if name and fee.isdigit():
            data.append({
                "id": str(get_id(data)),   # store as string (fix)
                "name": name,
                "course": course,
                "fee": fee,
                "status": status
            })
            save(data)

        return redirect("/")

    # SEARCH
    search = request.args.get("search")
    if search:
        data = [s for s in data if search.lower() in s["name"].lower()]

    total_students = len(data)
    total_fee = sum(float(s["fee"]) for s in data)

    return render_template("index.html",
                           data=data,
                           total_students=total_students,
                           total_fee=total_fee)

# ---------- DELETE ----------
@app.route("/delete/<int:id>")
def delete(id):
    data = load()
    data = [s for s in data if int(s["id"]) != id]
    save(data)
    return redirect("/")

# ---------- EDIT ----------
@app.route("/edit/<int:id>")
def edit(id):
    data = load()

    student = next((s for s in data if int(s["id"]) == id), None)

    if not student:
        return "Student not found"

    return render_template("edit.html", student=student)

# ---------- UPDATE ----------
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    data = load()

    for s in data:
        if int(s["id"]) == id:
            s["name"] = request.form["name"]
            s["course"] = request.form["course"]
            s["fee"] = request.form["fee"]
            s["status"] = request.form["status"]

    save(data)
    return redirect("/")

# ---------- RUN ----------
# ---------- RUN ----------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)