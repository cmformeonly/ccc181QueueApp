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

STATUS_LABELS = {
    "waiting": "In line",
    "called": "Washing now",
    "served": "Picked up",
    "no-show": "Not collected",
}
STATUS_BADGES = {
    "waiting": "text-bg-secondary",
    "called": "text-bg-info",
    "served": "text-bg-success",
    "no-show": "text-bg-warning",
}

# Each ticket: number, name, email, service_id, kilos, status
# status is one of: waiting, called, served, no-show
# A real app would load this from a database later (Week 4).
TICKETS = [
    {"number": 1, "name": "Ana", "email": "ana@example.com", "service_id": 1, "kilos": 5, "status": "waiting"},
    {"number": 2, "name": "Ben", "email": "ben@example.com", "service_id": 3, "kilos": 3, "status": "waiting"},
]

@app.context_processor
def inject_globals():
    return {
        "app_name": APP_NAME,
        "status_labels": STATUS_LABELS,
        "status_badges": STATUS_BADGES,
    }

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


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash("You left the queue.", "info")
    return redirect(url_for("index"))

    

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
