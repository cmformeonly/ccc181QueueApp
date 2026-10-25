## Jomar, the customer

> "I drop off my clothes and then I keep going back to ask if they're done. It wastes my time."

| | |
| --- | --- |
| **Photo or sketch** | Stock Picture |
| **Age, role and background** | 20, 3rd-year college student living in a boarding house, drops off laundry on weekends |
| **Goals** | Know when the laundry is ready without going back to ask. Drop off quickly before class. Pick up at a time that fits his schedule. |
| **Frustrations** | Walks to the shop only to find it isn't done. Can't tell how many loads are ahead of his. Shop staff are too busy to answer questions. |
| **Devices and context** | Android phone, one hand holding a bag of laundry, often outside or walking, mobile data that can be slow |
| **Tech comfort** | Medium: uses messaging and social apps daily but doesn't want to create an account just to do laundry |
| **Accessibility needs** | One hand busy, bright sunlight on the screen, slow mobile data, small phone screen |

### Scenario

Jomar arrives at the shop on Saturday morning with a bag of laundry and a class at 1 PM. He hands over his clothes, and the attendant gives him a ticket number through the app. He leaves to buy breakfast and, an hour later, opens the app on his phone to see how many loads are ahead of his and whether it's worth walking back yet.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Drop off a load and get a ticket | Join | FR-01 |
| Check my status and how many loads are ahead | My place | FR-0    2 |

### What this means for my interface

1. Because Jomar checks his phone with one hand while walking, his ticket number and loads ahead must be the biggest thing on My place.
2. Because his mobile data is often slow, pages must load fast and work without large images.
3. Because he doesn't want to create an account, the Join form must ask only for name, email, service, and kilos, with no password.

---

## Aling Nena, the staff member

> "Customers keep asking me if their laundry is ready, and I lose track     of whose bag is whose." 

| | |
| --- | --- |
| **Photo or sketch** | Stock Picture |
| **Age, role and background** | 42, owner and attendant of a small neighborhood laundry shop, handles drop-offs, washing, and pickups herself |
| **Goals** | Know which load to process next. Stop answering "is mine ready?" all day. Clear unclaimed laundry from the shelves. |
| **Frustrations** | Keeps orders in a notebook that gets messy. Customers interrupt her while she is working. Some laundry sits unclaimed for days. |
| **Devices and context** | Shared shop phone or an old laptop at the counter, hands often wet or busy, noisy machines runnin |
| **Tech comfort** | Low to medium: uses a phone for calls and messaging but is not used to business software |
| **Accessibility needs** | Wet or busy hands, needs large buttons that are hard to press by mistake, quick glances at the screen |

### Scenario

It's a busy Saturday, and Aling Nena has six loads waiting while two machines run. A new customer drops off a bag, and she sees it appear on her dashboard. When a machine finishes, she opens the dashboard, sees which load is next in line, marks it as being washed, and later marks it as picked up when the customer arrives.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See the waiting loads in order | Staff dashboard | FR-03 |
| Mark a load as being washed, picked up, or not collected | Staff dashboard | FR-03 |

### What this means for my interface

1. Because Aling Nena's hands are often wet or busy, the action buttons must be large and spaced apart so they are hard to press by mistake.
2. Because she needs to know what to do next at a glance, the dashboard must list the waiting loads in order with the next one at the top.
3. Because unclaimed laundry piles up, the dashboard must let her mark a load as not collected with one clear button.