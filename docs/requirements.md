# Wash'NLearn requirements

**Setting:** A neighborhood laundry shop, where customers drop off a load, leave, and come back for it.
**People who wait:** Customers who drop off laundry, such as Jomar in [docs/week3/personas.md](week3/personas.md).
**People who serve:** The shop attendant who washes and hands over loads, such as Aling Nena in [docs/week3/personas.md](week3/personas.md).

**Problem statement:** A laundry customer needs a way to know when their laundry is ready without going back to ask, because they keep making trips to the shop only to find it isn't done.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A customer can get a ticket by entering their name, email, service, and estimated kilos. | Must | **Yes** | Built (Week 3) |
| FR-02 | A customer can see their ticket number, status, and how many loads are ahead of them. | Must | **Yes** | Built (Week 3) |
| FR-03 | A staff member can see the loads that are in line, being washed, or ready for pickup, in order, and filter them by service. | Must | **Yes** | Built (Week 3) |
| FR-04 | A staff member can start washing the next load in line for a service. | Must | **Yes** | Built (Week 3) |
| FR-05 | A staff member can mark a load that is being washed as ready for pickup. | Must | **Yes** | Built (Week 3) |
| FR-06 | A staff member can mark a ready load as picked up. | Must | **Yes** | Built (Week 3) |
| FR-07 | A customer can leave the queue before their load starts washing. | Must | **Yes** | Built (Week 3) |
| FR-08 | A customer's My place page updates its status by itself within 10 seconds, without a reload. | Should | No | Built (Week 3) |
| FR-09 | A staff member can add, rename, and switch off a service. | Must | **Yes** | This week |
| FR-10 ★ | A staff member can see how many loads are in line for each service. | Should | No | Built (Week 3) |
| FR-11 ★ | A staff member can record the actual weight of a load, which may differ from the customer's estimate. | Should | **Yes** | Later |
| FR-12 ★ | A staff member can see which loads have been ready for pickup for more than 3 days. | Should | **Yes** | Later |
| FR-13 ★ | A customer can add a short care note to their load, such as "delicate items" or "no fabric softener", and staff can read it on the dashboard. | Could | **Yes** | Later |
| FR-14 | A staff member can remove a ticket that was created by mistake. | Should | **Yes** | This week |
| FR-15 | A customer can get back to their ticket by entering their email address or ticket number. | Must | No | Later |
| FR-16 ★ | A customer can see an estimated time for when their laundry will be ready. | Could | No | Later |

## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two customers can never get the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | My place loads in under 2 seconds on mobile data. | Performance | Must |
| NFR-04 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-05 | No password or secret key is stored in the repository. | Security | Must |
| NFR-06 | Every button and form field is at least 44 px tall on a phone, so it can be pressed with one hand or a wet hand. | Usability | Should |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-09, FR-15, plus NFR-01, NFR-02, NFR-03, NFR-04, and NFR-05. This is the smallest version that solves the problem: a customer can join, find their ticket again, and see when their laundry is ready, and the shop can run the queue and keep its list of services. It also needs the data to survive restarts, since a queue that forgets tickets is no use to anyone.

**Out of scope:**
- **Staff login.** The dashboard is open to anyone who knows the address. Logins need an accounts feature that is beyond this semester's database work.
- **Payment and pricing.** Taking payment or calculating a price from the kilos is a separate system, and the shop settles up at the counter.
- **Text message or email alerts.** Customers check My place themselves. Sending messages needs an outside service.

## Checked with a real person

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Customer | "If I close the page, how do I get back to my ticket? I'd need to look it up with my email or name." | Added FR-15 as Must |
| Customer | "I'd like to know roughly when it will be ready, not only how many bags are ahead." | Added FR-16 ★ as Could |