# Self-review of personas and wireframes

## Join

**Works well:** On the phone, the service is three large tap tiles and "Get my ticket" is pinned at the bottom, so Jomar can finish with one thumb. On the laptop, the "How it works" panel tells a first-time customer what to expect before the form. Both follow my rule that he shouldn't need an account or extra steps.
**Problem:** Jomar may not know how many kilos his laundry weighs before the shop weighs it, so he could guess wrong or get stuck on that field. This is a mismatch with the real world, because at a laundry shop the staff weigh the laundry, not the customer.
**Change:** Rename the field "Kilos (estimate)" and add a hint underneath: "Staff will confirm the weight at the counter." I will also show the allowed range (1 to 15) so he can't enter something invalid, which helps with error prevention.

## My place

**Works well:** The ticket number and "loads ahead" are the largest things at the top on both frames, and the tracker shows where the laundry is without any reading. This follows my rule that Jomar must see his place first and gives visibility of status.
**Problem:** My first version of the tracker stopped at "Washing now" and "Picked up", so Jomar had no signal that his laundry was finished and ready. He would have to keep coming back to ask, which is the frustration this app is meant to remove. That breaks visibility of status. The page also said "Updates automatically" but never showed when it last updated.
**Change:** Add a "Ready for pickup" step to the tracker, so the steps are In line, Washing now, Ready for pickup, and Picked up, with the message "Your laundry is ready for pickup!". Add "Last updated: 2:05 PM" under the note on both frames. Use the same words on every screen.

## Staff dashboard

**Works well:** The loads are sorted by status (three columns on the laptop, three tabs on the phone), with the next load first and a large button as the first action. Each status shows exactly one main button (Start washing, Mark ready, or Picked up). This follows my rule for Aling Nena that the most frequent action must be easy to reach with wet or busy hands.
**Problem:** My first version put "Picked up" and "Not collected" side by side at the same size, so she could tap "Not collected" by accident, and nothing let her undo it. That is an error prevention problem. The phone tab was also called "Missed" while other screens said "Not collected", which was inconsistent.
**Change:** Remove "Not collected" from the staff screen, since the only action a ready load needs is "Picked up", and customers can already cancel their own ticket with "Leave the queue". The tabs and columns are now In line, Washing now, and Ready for pickup, with counts. A load that is never collected stays in Ready for pickup, which I accept for this version.