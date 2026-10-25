"""Wash'NLearn: a queue system for a neighborhood laundry shop.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable

APP_NAME = "Wash'NLearn"

SERVICES = [
    {"id": 1, "name": "Wash and fold"},
    {"id": 2, "name": "Dry only"},
    {"id": 3, "name": "Comforter / bulky items"},
]

# What the screen says for each status (the code values stay the same).
STATUS_LABELS = {
    "waiting": "In line",
    "washing": "Washing now",
    "called": "Ready for pickup",
    "served": "Picked up",
    "no-show": "Left the queue",
}
STATUS_BADGES = {
    "waiting": "text-bg-secondary",
    "washing": "text-bg-info",
    "called": "text-bg-primary",
    "served": "text-bg-success",
    "no-show": "text-bg-warning",
}

# Each ticket: number, name, email, service_id, kilos, status
# status is one of: waiting, washing, called, served, no-show
# A real app would load this from a database later (Week 4).
TICKETS = [
    {"number": 1, "name": "Ana", "email": "ana@example.com", "service_id": 1, "kilos": 5, "status": "waiting"},
    {"number": 2, "name": "Ben", "email": "ben@example.com", "service_id": 3, "kilos": 3, "status": "waiting"},
]


@app.context_processor
def inject_globals():
    # Makes these available in every template automatically.
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
    kilos = form.get("kilos", type=int)

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."
    if kilos is None or not 1 <= kilos <= 15:
        errors["kilos"] = "Enter the weight in kilos, from 1 to 15."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "kilos": kilos, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "washing", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    names = {s["id"]: s["name"] for s in SERVICES}
    # Star feature: how many loads are in line for each service.
    counts = {s["id"]: sum(1 for t in TICKETS
                           if t["service_id"] == s["id"] and t["status"] == "waiting")
              for s in SERVICES}
    return render_template("staff.html", queue=queue, services=SERVICES,
                           names=names, selected=service_id, counts=counts)


@app.post("/staff/call-next")
def staff_call_next():
    service_id = request.form.get("service_id", type=int)
    waiting = [t for t in TICKETS if t["status"] == "waiting"]
    if service_id:
        waiting = [t for t in waiting if t["service_id"] == service_id]
    if not waiting:
        flash("No one is in line right now.", "warning")
    else:
        waiting[0]["status"] = "washing"
        flash(f"Ticket #{waiting[0]['number']} is now washing.", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"wash": "washing", "ready": "called", "serve": "served"}.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or new_status is None:
        abort(404)

    allowed_from = {
        "washing": ("waiting",),
        "called": ("washing",),
        "served": ("called",),
    }
    if t["status"] not in allowed_from[new_status]:
        flash(f"Ticket #{ticket_id} can't be changed that way.", "warning")
    else:
        t["status"] = new_status
        flash(f"Ticket #{ticket_id} marked {STATUS_LABELS[new_status]}.", "info")
    return redirect(url_for("staff_dashboard", service_id=request.form.get("service_id", type=int)))


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
    app.run(debug=True)