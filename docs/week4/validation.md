# Validation

## Results

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Name, email and service must be valid | Flask | curl POST /join with `name=`, `email=not-an-email`, `service_id=999` | 400 BAD REQUEST, ticket count unchanged |
| Name is at most 80 characters | Flask | curl POST /join with a 100-character name | 400 BAD REQUEST, ticket count unchanged |
| Kilos must be 1 to 15 | Flask | curl POST /join with `kilos=99` | 400 BAD REQUEST, ticket count unchanged |
| A switched-off service cannot be joined | Flask | curl POST /join with the id of a switched-off service | 400 BAD REQUEST, ticket count unchanged |
| Ticket needs an existing service | Database (FOREIGN KEY) | `INSERT INTO tickets ... service_id 999` in psql | `ERROR:  insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Ticket needs a customer | Database (NOT NULL) | `INSERT INTO tickets` with no customer_id | `ERROR:  null value in column "customer_id" of relation "tickets" violates not-null constraint` |
| One customer row per email | Database (UNIQUE) | `INSERT INTO customers` with an email that already exists | `ERROR:  duplicate key value violates unique constraint "customers_email_key"` |
| Average minutes must be above 0 | Database (CHECK) | `INSERT INTO services ... avg_minutes 0` | `ERROR:  new row for relation "services" violates check constraint "ck_services_avg_minutes"` |
| Status must be one of the five allowed | Database (CHECK) | `UPDATE tickets SET status = 'lost'` | `ERROR:  new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| A ready ticket must have a ready time | Database (CHECK) | `UPDATE tickets SET status = 'called', called_at = NULL` | `ERROR:  new row for relation "tickets" violates check constraint "ck_tickets_called_at_set"` |
| Email must be lowercase | Database (CHECK) | `INSERT INTO customers ... 'Test@Example.com'` | `ERROR:  new row for relation "customers" violates check constraint "ck_customers_email_lowercase"` |
| Kilos must be 1 to 15 | Database (CHECK) | `INSERT INTO tickets ... kilos_estimate 99` | `ERROR:  new row for relation "tickets" violates check constraint "ck_tickets_kilos_estimate"` |
| A service with tickets cannot be deleted | Database (RESTRICT) | `DELETE FROM services WHERE id = <a service with tickets>` | `ERROR:  update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |
