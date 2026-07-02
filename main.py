from pawpal_system import Task, Owner, Pet, Scheduler, Priority, TimeSlot

BOLD   = "\033[1m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
RESET  = "\033[0m"

def section(title: str) -> None:
    print(f"\n{BOLD}{CYAN}── {title} ──{RESET}")

owner = Owner(name="Adam", available_time=60)

huey = Pet(name="Huey", breed="Dachshund", species="Dog")
luna = Pet(name="Luna", breed="Doberman",  species="Dog")
owner.add_pet(huey)
owner.add_pet(luna)

# Tasks added OUT OF ORDER (evening before morning, low before high, long before short)
# start_time = minutes from midnight  (e.g. 480 = 8:00, 490 = 8:10, 540 = 9:00)

# Huey — Feed breakfast (8:00–8:10) and Morning walk (8:05–8:25) OVERLAP intentionally
huey.add_task(Task("Bath time",      duration=30, priority=Priority.LOW,    time_slot=TimeSlot.EVENING,   start_time=1080))  # 18:00–18:30
huey.add_task(Task("Morning walk",   duration=20, priority=Priority.HIGH,   time_slot=TimeSlot.MORNING,   recurrence_interval="daily", start_time=485))  # 8:05–8:25
huey.add_task(Task("Evening stroll", duration=15, priority=Priority.MEDIUM, time_slot=TimeSlot.EVENING,   start_time=1110))  # 18:30–18:45
huey.add_task(Task("Feed breakfast", duration=10, priority=Priority.HIGH,   time_slot=TimeSlot.MORNING,   recurrence_interval="daily", start_time=480))  # 8:00–8:10

# Luna — Evening meds (18:00–18:05) overlaps Huey's Bath time (18:00–18:30) — cross-pet conflict
luna.add_task(Task("Brush Teeth",    duration=10, priority=Priority.MEDIUM, time_slot=TimeSlot.EVENING,   recurrence_interval="daily", start_time=1120))  # 18:40–18:50
luna.add_task(Task("Evening meds",   duration=5,  priority=Priority.HIGH,   time_slot=TimeSlot.EVENING,   start_time=1080))  # 18:00–18:05  ← conflicts with Huey's Bath time
luna.add_task(Task("Cut Nails",      duration=15, priority=Priority.HIGH,   is_recurring=True,            recurrence_interval="weekly"))
luna.add_task(Task("Afternoon play", duration=20, priority=Priority.LOW,    time_slot=TimeSlot.AFTERNOON, start_time=780))   # 13:00–13:20

# Mark one task done so get_completed_tasks() has something to show
huey.tasks[0].mark_complete()   # Bath time → completed (no recurrence_interval, no clone)

# ── 1. Full schedule (priority-first sort) ─────────────────────────
scheduler = Scheduler(owner)
scheduler.generate_schedule()
print(scheduler.display_schedule())

# ── 2. Sort by time slot (chronological view) ──────────────────────
section("All tasks sorted by TIME SLOT (chronological)")
for pet, task in scheduler.sort_by_time_slot(scheduler.get_all_tasks()):
    slot = f"[{task.time_slot.name.lower()}]" if task.time_slot.name != "ANYTIME" else "[anytime]"
    print(f"  {slot:<13} [{pet.name}] {task.get_summary()}")

# ── 3. Filter by pet ───────────────────────────────────────────────
section("Filter: Huey's scheduled tasks only")
huey_tasks = scheduler.filter_by_pet("Huey")
if huey_tasks:
    for _, task in huey_tasks:
        print(f"  • {task.get_summary()}")
else:
    print("  (none scheduled)")

section("Filter: Luna's scheduled tasks only")
luna_tasks = scheduler.filter_by_pet("Luna")
if luna_tasks:
    for _, task in luna_tasks:
        print(f"  • {task.get_summary()}")
else:
    print("  (none scheduled)")

# ── 4. Filter by status ────────────────────────────────────────────
section("Filter: all PENDING tasks (not completed)")
for pet, task in scheduler.get_pending_tasks():
    print(f"  • [{pet.name}] {task.get_summary()}")

section("Filter: all COMPLETED tasks")
completed = scheduler.get_completed_tasks()
if completed:
    for pet, task in completed:
        print(f"  • [{pet.name}] {task.get_summary()}")
else:
    print("  (none yet)")

# ── 5. Recurrence demo ─────────────────────────────────────────────
section("Recurrence: completing daily/weekly tasks auto-queues next occurrence")

# Complete "Morning walk" (daily) and "Cut Nails" (weekly)
walk_task  = huey.tasks[1]   # Morning walk
nails_task = luna.tasks[2]   # Cut Nails

print(f"  Before — Huey task count : {len(huey.tasks)}")
print(f"  Before — Luna task count : {len(luna.tasks)}")

next_walk  = scheduler.complete_task(huey, walk_task)
next_nails = scheduler.complete_task(luna, nails_task)

print(f"\n  Completed : {walk_task.description!r}  [{walk_task.recurrence_interval}]")
print(f"  Queued    : {next_walk.get_summary()}")

print(f"\n  Completed : {nails_task.description!r}  [{nails_task.recurrence_interval}]")
print(f"  Queued    : {next_nails.get_summary()}")

print(f"\n  After  — Huey task count : {len(huey.tasks)}")
print(f"  After  — Luna task count : {len(luna.tasks)}")

# Complete a task with NO recurrence_interval — should return None
stroll_task = huey.tasks[2]  # Evening stroll
result = scheduler.complete_task(huey, stroll_task)
print(f"\n  Completed : {stroll_task.description!r}  [no interval]")
print(f"  Next occurrence : {result!r}  ← None, no clone created")

# ── 6. Conflict detection ──────────────────────────────────────────
section("Conflict detection: overlapping start times")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {YELLOW}⚠  {warning}{RESET}")
else:
    print("  No conflicts detected ✓")