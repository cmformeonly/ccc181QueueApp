"""Wash'NLearn: a queue system for a neighborhood laundry shop.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os

from datetime import timedelta, timezone
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

PH_TIME = timezone(timedelta(hours=8)) 


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Nov 08, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""


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
    "left": "Left the queue",
}
STATUS_BADGES = {
    "waiting": "text-bg-secondary",
    "washing": "text-bg-info",
    "called": "text-bg-primary",
    "served": "text-bg-success",
    "left": "text-bg-warning",
}


@app.context_processor
def inject_globals():
    # Makes these available in every template automatically.
    return {
        "app_name": APP_NAME,
        "status_labels": STATUS_LABELS,
        "status_badges": STATUS_BADGES,
    }


def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)


def waiting_counts():
    """How many loads are in line for each service (the star feature)."""
    stmt = (db.select(Ticket.service_id, func.count())
            .where(Ticket.status == "waiting")
            .group_by(Ticket.service_id))
    by_service = dict(db.session.execute(stmt).all())
    return {s.id: by_service.get(s.id, 0) for s in all_services()}


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
        "left": "You left the queue.",
    }[status]


@app.route("/")
def index():
    return render_template("index.html")


def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()


def active_services():
    stmt = db.select(Service).filter_by(active=True).order_by(Service.name)
    return db.session.scalars(stmt).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=active_services(), form={})


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
    if service is None or not service.active:
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
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "washing", "called"]))
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()
    return render_template("staff.html", queue=queue, services=all_services(),
                           selected=service_id, counts=waiting_counts())


STAFF_ACTIONS = {"wash": "washing", "ready": "called", "serve": "served"}
ALLOWED_FROM = {
    "washing": ("waiting",),
    "called": ("washing",),
    "served": ("called",),
}


@app.post("/staff/call-next")
def staff_call_next():
    service_id = request.form.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status == "waiting")
            .order_by(Ticket.created_at, Ticket.id)
            .limit(1))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    t = db.session.scalar(stmt)
    if t is None:
        flash("No one is in line right now.", "warning")
    else:
        t.status = "washing"
        db.session.commit()
        flash(f"Ticket #{t.id} is now washing.", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    if t.status not in ALLOWED_FROM[new_status]:
        flash(f"Ticket #{ticket_id} can't be changed that way.", "warning")
    else:
        t.status = new_status
        if new_status == "called":
            t.called_at = func.now()  # the database fills in the time
        db.session.commit()
        flash(f"Ticket #{ticket_id} marked {STATUS_LABELS[new_status]}.", "info")
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    message = status_message(t.status, people_ahead(t))
    return render_template("ticket.html", ticket=t, service=t.service, message=message)



@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ahead = people_ahead(t)
    return {
        "status": t.status,
        "label": STATUS_LABELS[t.status],
        "badge": STATUS_BADGES[t.status],
        "message": status_message(t.status, ahead),
        "ahead": ahead,
    }


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status == "waiting":
        t.status = "left"  # soft delete: the row stays for reports
        db.session.commit()
    flash("You left the queue.", "info")
    return redirect(url_for("index"))


@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)  # hard delete: the row is gone for good
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))


@app.get("/staff/services")
def services_list():
    return render_template("services.html", services=all_services())


@app.post("/staff/services")
def service_create():
    name = request.form.get("name", "").strip()
    minutes = request.form.get("avg_minutes", type=int)
    if not name or len(name) > 60 or not minutes or minutes <= 0:
        flash("Enter a name (up to 60 characters) and minutes greater than 0.", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name, avg_minutes=minutes))
    try:
        db.session.commit()
        flash(f"Service “{name}” added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name = request.form.get("name", "").strip()
    minutes = request.form.get("avg_minutes", type=int)
    if not name or len(name) > 60 or not minutes or minutes <= 0:
        flash("Enter a name (up to 60 characters) and minutes greater than 0.", "danger")
        return redirect(url_for("services_list"))
    s.name = name
    s.avg_minutes = minutes
    s.active = request.form.get("active") == "on"  # an unticked box is not sent at all
    try:
        db.session.commit()
        flash(f"Service “{name}” saved.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    name = s.name
    if s.tickets:
        flash(f"“{name}” has tickets, so it cannot be deleted. Turn it off instead.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Service “{name}” deleted.", "warning")
    return redirect(url_for("services_list"))

if __name__ == "__main__":
    app.run(debug=True)