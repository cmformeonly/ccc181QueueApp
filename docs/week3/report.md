# Wash'NLearn: Week 3 report

## 1. Title details

- **App name:** Wash'NLearn
- **Setting:** A neighborhood laundry shop
- **Name:** James Ralf P. Canonigo
- **Student ID:** 22024-0525
- **Section:** CS3A
- **Date:** October 25, 2026
- **Pull request:** [link to your pull request]

## 2. Personas  

Link to the full file: [personas.md](personas.md).

**Jomar, the customer**
> "I drop off my clothes and then I keep going back to ask if they're done. It wastes my time."

Top tasks: drop off a load and get a ticket (FR-01), and check his status and how many loads are ahead (FR-02).

**Aling Nena, the staff member**
> "Customers keep asking me if their laundry is ready, and I lose track of whose bag is whose."

Top tasks: see the waiting loads in order and move each load through washing, ready, and picked up (FR-03).

## 3. Screens

**Join (phone).** Jomar uses it on his phone to get a ticket. Requirement: FR-01.
![Join on a phone](screenshots/join-phone.png)

**Join (laptop).** Jomar uses it on a laptop to get a ticket. Requirement: FR-01.
![Join on a laptop](screenshots/join-laptop.png)

**My place (phone).** Jomar checks his ticket number, status, and loads ahead. Requirement: FR-02.
![My place on a phone](screenshots/myplace-phone.png)

**My place (laptop).** Jomar checks the same information on a laptop. Requirement: FR-02.
![My place on a laptop](screenshots/myplace-laptop.png)

**Staff dashboard (phone).** Aling Nena starts, finishes, and hands over loads, with each row shown as a card. Requirement: FR-03.
![Staff dashboard on a phone](screenshots/staff-phone.png)

**Staff dashboard (laptop).** Aling Nena sees all loads in a table, with the star feature (loads in line per service) above it. Requirement: FR-03.
![Staff dashboard on a laptop](screenshots/staff-laptop.png)

## 4. Design decisions

1. **The ticket number and "loads ahead" are the biggest things on My place.** Jomar checks his phone with one hand while walking or running errands, so he needs the answer to "where am I?" at a glance. In the usability test, the tester found both in 20 seconds with no hesitation.
2. **I added a "Ready for pickup" status.** My first design stopped at "Washing now" and "Picked up", so a customer had no way to know when their laundry was finished. That is the exact frustration Jomar describes in his quote. The status now appears in the My place tracker, the staff buttons, and the live refresh.
3. **The kilos field says "estimate" and explains who confirms it.** My self-review found that a customer does not know their laundry's weight until the shop weighs it. The field is labeled "Kilos (estimate)", shows the allowed range of 1 to 15, and has the hint "Staff will confirm the weight at the counter." The server also checks the value, so bad input is rejected even if someone skips the form.

## 5. Self-review

The full review is in [feedback.md](feedback.md). The main problems I found and changed:

- **Join:** customers could get stuck on the kilos field. I renamed it "Kilos (estimate)", added a hint, and showed the allowed range.
- **My place:** the tracker had no step for finished laundry, and "Updates automatically" never said when. I added the Ready for pickup step and a "Last updated" time.
- **Staff dashboard:** "Picked up" and "Not collected" sat side by side at the same size, so an accidental tap was easy and could not be undone. I removed "Not collected" from the staff screen. Customers can still cancel their own ticket with "Leave the queue".

## 6. Accessibility

The full check is in [accessibility.md](accessibility.md).

| Screen | Lighthouse accessibility score |
| --- | --- |
| Join | 100 |
| My place | 100 |
| Staff | 100 |

The most important issue I fixed was the navbar contrast. Bootstrap's default link color on my teal bar was about 2.7:1, below the 4.5:1 needed, so I made the links brighter and underlined the active page so it is not shown by color alone. I also gave My place an `<h1>`, set buttons and fields to at least 44 px tall, styled the skip link, and turned the staff table into cards on phones so nothing scrolls sideways.

## 7. Usability test

The full notes are in [usability-test.md](usability-test.md). One tester who usually avail laundry services.

| Task | Finished? | Time | What happened |
| --- | --- | --- | --- |
| 1. Get in line for Wash and fold | Yes, no help | 30 seconds | Asked what the email field is for |
| 2. Find how many are ahead and my number | Yes, no help | 20 seconds | No hesitation |
| 3. Start washing the next load, mark it ready, then picked up | Yes, no help | 1 minute | Asked why there are two buttons for starting a wash |

**Improvement:** the staff dashboard had a "Start washing the next load" button at the top and a "Start washing" button on every waiting row, which confused the tester on the longest task. I removed the buttons from the rows, so the top button is the single way to start the next load, and rows now show a dash until a load is washing.

**Before**
![Staff dashboard before the fix](screenshots/staff-before-fix.png)

**After**
![Staff dashboard after the fix](screenshots/staff-after-fix.png)

I also added a short hint under the email field ("The shop may contact you about your laundry."), because the tester asked what it was for.

## 8. Reflection

The hardest part was keeping every file consistent while the design changed. Adding the Washing now and Ready for pickup statuses touched `app.py`, three templates, my wireframes, and my self-review, and along the way I hit errors from a duplicate route, a missing route, and a missing template variable.

In Week 4, my tickets will move from a Python list, which disappears whenever Flask restarts, into a database table with columns for number, name, email, service, kilos, and status. The count of loads ahead will become a query instead of a loop, and the status values will be limited to the five I use. I plan to keep the JSON route's response the same, so the My place refresh will not need to change.

## 9. Declaration

AI Use Declaration

I used Claude Sonnet 5.5 (Anthropic) in preparing this work. It was used for:

1. Grammar, spelling, and punctuation correction
2. Rephrasing sentences for clarity
3. Brainstorming ideas, formatting, and explaining concepts