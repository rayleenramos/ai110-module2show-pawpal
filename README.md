# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output
🐾 PawPal+ Daily Schedule                   
Owner: Adam  |  Budget: 45 min               

  🐾 Huey (Dachshund)
  ──────────────────────────────────────────────
   1. Feed breakfast          10 min  ● HIGH
   2. Morning walk            20 min  ● HIGH

  🐾 Luna (Doberman)
  ──────────────────────────────────────────────
   1. Cut Nails               15 min  ● HIGH  ↺ recurring
   2. Brush Teeth             10 min  ● MEDIUM

  Scheduled: 40 min  |  Skipped: 1 task(s)
  ⚠  Bath time skipped — needs 45 min

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

```
Sample test output:
================================= test session starts ===========================================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/rayleen/Desktop/AI_110/ai110-module2show-pawpal
plugins: anyio-4.14.0
collected 5 items                                                                                                                                                                                
tests/test_pawpal.py .....                                                                                                                                                                 [100%]
================= 5 passed in 0.04s =====================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting |sort_by_priority(), sort_by_time_slot()|Sort by priority and duration, or by time of day|
| Filtering |filter_by_pet(), get_pending_tasks(), get_completed_tasks()|Filter by pet name or completion status|
| Conflict handling |detect_conflicts()| Warns if two tasks overlap in time, no crash|
| Recurring tasks |complete_task(), Task.next_occurrence()|Completing a daily/weekly task auto-queues the next one |

## 📸 Demo Walkthrough

1. Create an owner with a time budget and add two pets with tasks of different priorities and time slots.
2. Generate a daily schedule sorted by priority, tasks that don't fit the budget are listed as skipped.
3. View the same tasks in chronological order from morning to evening.
4. Filter tasks by pet name or completion status to get a focused view.
5. Complete a recurring task and it automatically queues the next occurrence.
6. Detect any tasks with overlapping start and end times and get a warning.

![Screenshot](https://github.com/user-attachments/assets/466bbbf5-d7cd-46e5-96b9-b6cc7ff8d8ce)

<img width="696" height="289" alt="Screenshot 2026-07-02 at 12 20 17 AM" src="https://github.com/user-attachments/assets/c9e3b2d9-d96e-4de8-b624-09cb9fbe9ddc" />
