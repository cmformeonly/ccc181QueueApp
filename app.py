"""Wash'NLearn: a queue system for a neighborhood laundry shop.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Customer, Service, Ticket, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

APP_NAME = "Wash'NLearn"    

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        ("Wash and fold", 90),
        ("Dry only", 45),
        ("Comforter / bulky items", 120),
    ]
    for name, minutes in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, avg_minutes=minutes))
    db.session.commit()
    print("Services are ready.")

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


@app.context_processor
def inject_globals():
    # Makes these available in every template automatically.
    return {
        "app_name": APP_NAME,
        "status_labels": STATUS_LABELS,
        "status_badges": STATUS_BADGES,
    }


def count_ahead(t):
    return sum(1 for x in TICKETS
               if x["service_id"] == t["service_id"]
               and x["status"] == "waiting"
               and x["number"] < t["number"])


def status_message(status, ahead):
    if status == "waiting":
        if ahead == 0:
            return "You're next!"
        if ahead == 1:      
            return "1 load ahead of you"
        return f"{ahead} loads ahead of you"
    return {
        "washing": "Your laundry is being washed.",
        "called": "Your laundry is ready for pickup!",
        "served": "All done. Thanks for picking up!",
        "no-show": "You left the queue.",
    }[status]


@app.route("/")
def index():
    return render_template("index.html")


def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    kilos = form.get("kilos", type=int)
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 80:
        errors["name"] = "Enter your name (up to 80 characters)."
    if "@" not in email or len(email) > 120:
        errors["email"] = "Enter a valid email address."
    if service is None:
        errors["service_id"] = "Choose a service."
    if kilos is None or not 1 <= kilos <= 15:
        errors["kilos"] = "Enter the weight in kilos, from 1 to 15."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors=errors), 400

    customer = db.session.scalar(db.select(Customer).filter_by(email=email))
    if customer is None:
        customer = Customer(name=name, email=email)
    ticket = Ticket(customer=customer, service=service, kilos_estimate=kilos)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


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
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    message = status_message(t["status"], count_ahead(t))
    return render_template("ticket.html", ticket=t, service=service, message=message)


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:   
        abort(404)
    ahead = count_ahead(t)
    return {
        "status": t["status"],
        "label": STATUS_LABELS[t["status"]],
        "badge": STATUS_BADGES[t["status"]],
        "message": status_message(t["status"], ahead),
        "ahead": ahead,
    }


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