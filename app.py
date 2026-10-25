"""WashNLearn: a queue system for a neighborhood laundry shop.

Run it with:    
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

app = Flask(__name__)

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


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    return render_template("ticket.html", ticket_id=ticket_id)
    

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
