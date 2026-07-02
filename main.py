from pawpal_system import Task, Owner, Pet, Scheduler, Priority, TimeSlot

BOLD   = "\033[1m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
GREEN  = "\033[32m"
RESET  = "\033[0m"

def section(title: str) -> None:
    print(f"\n{BOLD}{CYAN}── {title} ──{RESET}")

owner = Owner(name="Adam", available_time=60)

huey = Pet(name="Huey", breed="Dachshund", species="Dog")
luna = Pet(name="Luna", breed="Doberman",  species="Dog")
owner.add_pet(huey)
owner.add_pet(luna)

# start_time = minutes from midnight (480 = 8:00, 1080 = 18:00, etc.)
huey.add_task(Task("Bath time",      duration=30, priority=Priority.LOW,    time_slot=TimeSlot.EVENING,   start_time=1080))
huey.add_task(Task("Morning walk",   duration=20, priority=Priority.HIGH,   time_slot=TimeSlot.MORNING,   recurrence_interval="daily", start_time=485))
huey.add_task(Task("Evening stroll", duration=15, priority=Priority.MEDIUM, time_slot=TimeSlot.EVENING,   start_time=1110))
huey.add_task(Task("Feed breakfast", duration=10, priority=Priority.HIGH,   time_slot=TimeSlot.MORNING,   recurrence_interval="daily", start_time=480))

luna.add_task(Task("Brush Teeth",    duration=10, priority=Priority.MEDIUM, time_slot=TimeSlot.EVENING,   recurrence_interval="daily", start_time=1120))
luna.add_task(Task("Evening meds",   duration=5,  priority=Priority.HIGH,   time_slot=TimeSlot.EVENING,   start_time=1080))
luna.add_task(Task("Cut Nails",      duration=15, priority=Priority.HIGH,   is_recurring=True,            recurrence_interval="weekly"))
luna.add_task(Task("Afternoon play", duration=20, priority=Priority.LOW,    time_slot=TimeSlot.AFTERNOON, start_time=780))

huey.tasks[0].mark_complete()  # Bath time pre-marked done

# ── 1. Schedule ────────────────────────────────────────────────────
scheduler = Scheduler(owner)
scheduler.generate_schedule()
print(scheduler.display_schedule())

# ── 2. Chronological view ──────────────────────────────────────────
section("Tasks by time slot (chronological)")
for pet, task in scheduler.sort_by_time_slot(scheduler.get_all_tasks()):
    slot = f"[{task.time_slot.name.lower()}]"
    time_range = ""
    if task.start_time is not None:
        time_range = f"  {task.fmt_time(task.start_time)}–{task.fmt_time(task.end_time())}"
    print(f"  {slot:<13} [{pet.name:<4}] {task.description:<18}{time_range}")

# ── 3. Completed tasks ─────────────────────────────────────────────
section("Completed tasks")
completed = scheduler.get_completed_tasks()
if completed:
    for pet, task in completed:
        print(f"  {GREEN}✓{RESET} [{pet.name}] {task.description}  ({task.duration} min)")
else:
    print("  (none yet)")

# ── 4. Recurrence ──────────────────────────────────────────────────
section("Recurrence: completing a task auto-queues its next occurrence")

walk_task  = huey.tasks[1]  # Morning walk  (daily)
nails_task = luna.tasks[2]  # Cut Nails     (weekly)

next_walk  = scheduler.complete_task(huey, walk_task)
next_nails = scheduler.complete_task(luna, nails_task)

print(f"  ✓ {walk_task.description!r} ({walk_task.recurrence_interval}) → queued: {next_walk.description!r}")
print(f"  ✓ {nails_task.description!r} ({nails_task.recurrence_interval}) → queued: {next_nails.description!r}")

stroll_task = huey.tasks[2]  # Evening stroll (no recurrence)
result = scheduler.complete_task(huey, stroll_task)
print(f"  ✓ {stroll_task.description!r} (no interval) → next occurrence: {result!r}")

# ── 5. Conflict detection ──────────────────────────────────────────
section("Conflict detection")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {YELLOW}⚠  {warning}{RESET}")
else:
    print(f"  {GREEN}No conflicts detected ✓{RESET}")
