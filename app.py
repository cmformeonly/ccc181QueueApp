"""WashNLearn: a queue system for a neighborhood laundry shop.

Run it with:    
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

APP_NAME = "WashNLearn"

SERVICES = [
    {"id": 1, "name": "Wash and fold"},
    {"id": 2, "name": "Dry only"},
    {"id": 3, "name": "Comforter / bulky items"},
]

# Each ticket: number, name, email, service_id, kilos, status
# status is one of: waiting, called, served, no-show
# A real app would load this from a database later (Week 4).
TICKETS = [
    {"number": 1, "name": "Ana", "email": "ana@example.com", "service_id": 1, "kilos": 5, "status": "waiting"},
    {"number": 2, "name": "Ben", "email": "ben@example.com", "service_id": 3, "kilos": 3, "status": "waiting"},
]

@app.context_processor
def inject_app_name():
    return {"app_name": APP_NAME}

@app.route("/")
def index():
    return render_template("index.html", services=SERVICES)


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"    



@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    return render_template("ticket.html", ticket_id=ticket_id)
    

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
