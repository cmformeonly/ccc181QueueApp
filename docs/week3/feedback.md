# Self-review of personas and wireframes

## Join

**Works well:** On the phone, the service is three large tap tiles and "Get my ticket" is pinned at the bottom, so Jomar can finish with one thumb. On the laptop, the "How it works" panel tells a first-time customer what to expect before the form. Both follow my rule that he shouldn't need an account or extra steps.
**Problem:** Jomar may not know how many kilos his laundry weighs before the shop weighs it, so he could guess wrong or get stuck on that field. This is a mismatch with the real world, because at a laundry shop the staff weigh the laundry, not the customer.
**Change:** Rename the field "Kilos (estimate)" and add a hint underneath: "Staff will confirm the weight at the counter." I will also show the allowed range (1 to 15) so he can't enter something invalid, which helps with error prevention.

## My place

**Works well:** The ticket number and "loads ahead" are the largest things at the top on both frames, and the tracker (In line, Washing now, Picked up) shows where the laundry is without any reading. This follows my rule that Jomar must see his place first and gives visibility of status.
**Problem:** The page says "Updates automatically" but never shows when it last updated, so Jomar can't tell whether the number is current or the connection is stuck. That breaks visibility of status.
**Change:** Add "Last updated: (Time)" to the note on both frames. Use the same words on every screen: In line, Washing now, Picked up, Not collected.

## Staff dashboard

**Works well:** The loads are sorted by status (three columns on the laptop, three tabs on the phone), with the next load first and a large "Start washing" button as the first action. This follows my rule for Aling Nena that the most frequent action must be easy to reach with wet or busy hands.
**Problem:** "Picked up" and "Not collected" sit next to each other at the same size, so she could tap "Not collected" by accident, and nothing lets her undo it. That is an error prevention problem.
**Change:** Put more space between the two buttons, make "Not collected" look secondary, and ask for confirmation before it applies. Keep the counts on the tabs so she can see at a glance that loads are waiting in another tab. 