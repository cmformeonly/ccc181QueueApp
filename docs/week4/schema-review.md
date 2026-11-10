# Schema self-review

## 1. Coverage (question 1)

**Works well:** Every requirement with Stores data? = Yes has a table or column. The Week 3 data (name, email, service, kilos, status) is in `customers`, `services` and `tickets`, and the staff dashboard (FR-03) can order loads by `tickets.created_at`.
**Problem:** In my first draft, FR-11 (staff record the actual weight, which may differ from the estimate) had no column. I only stored the customer's estimate, so staff would have had nowhere to put the real weight. I found this by checking each *Stores data* requirement against my columns (question 1).
**Change:** I added `tickets.actual_kilos` (numeric(4,1), empty until staff weigh the load) and renamed `kilos` to `kilos_estimate`, so the two weights cannot be confused. The final ERD and `schema.md` already include both.

## 2. Bad data: email typed in different capitals (question 4)

**Works well:** `customers.email` is UNIQUE, so a returning customer is matched to their existing row instead of getting a second one.
**Problem:** PostgreSQL treats `Ana@School.edu` and `ana@school.edu` as different values, so UNIQUE alone allows two rows for one person if the email is not lowercased first. My Flask code lowercases it, but a bug or a direct insert would skip that.
**Change:** I added `CHECK (email = lower(email))` to `customers.email`, so the database itself only accepts lowercase emails. I updated 2c in `schema.md` and the ERD.

## 3. Facts that could disagree (questions 3 and 4)

**Works well:** I store `called_at`, the moment a load became ready, and compute "ready for more than 3 days" (FR-12) from it. No "days waiting" number is stored, so it can never go out of date.
**Problem:** Nothing stopped a ticket from having status `called` or `served` with an empty `called_at`, and FR-12 would then miss that load.
**Change:** I added a table CHECK: `status NOT IN ('called', 'served') OR called_at IS NOT NULL`. A load can only be ready or picked up if it has a ready time. I updated 2c in `schema.md` and the ERD.

## 4. Deletes (question 5)

**Works well:** Both foreign keys use RESTRICT. A service or a customer with tickets cannot be deleted, so the shop keeps its history for reports, and staff switch a service off (FR-09) instead of deleting it.
**Problem:** A mistaken ticket (FR-14) is hard-deleted, but its customer row stays behind with no tickets.
**Change:** I kept it as it is. A leftover customer does no harm, and the same row is reused the next time that person joins with the same email. Removing it automatically would need extra code for very little benefit.

## Other questions checked

- **One fact in one place (question 2):** A customer's name and email are stored once in `customers`, and a service's name once in `services`. I found no repeated facts.
- **Types (question 6):** Every moment in time is `timestamptz`, the estimate is an integer and the actual weight is a numeric, and no number is stored as text.