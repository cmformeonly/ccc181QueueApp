# Wash'NLearn

Wash'NLearn is a queue system for a neighborhood laundry shop. Customers get a ticket when they drop off their laundry and can check how many loads are ahead of them from their phone, while staff update each load as it is washed and picked up.

Requirements: [docs/requirements.md](docs/requirements.md)

## How to run it

1. Copy `.env.example` to `.env` and set your own password in both lines.
2. Start the database: `docker compose up -d` (wait until `docker compose ps` says healthy).
3. Create a virtual environment and install the packages:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Create the tables and the starting services:

   ```
   flask --app app db upgrade
   flask --app app seed
   ```

5. Start the app: `flask --app app run --debug`, then open http://127.0.0.1:5000

**Note:** the staff pages (`/staff` and `/staff/services`) have no login yet. Staff login comes in Week 11.