from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TimeSlot(Enum):
    MORNING   = 1
    AFTERNOON = 2
    EVENING   = 3
    ANYTIME   = 4  # no preference — sorted last within a priority group


@dataclass
class Task:
    description: str
    duration: int           # minutes
    priority: Priority
    is_recurring: bool = False
    completed: bool = False
    time_slot: TimeSlot = TimeSlot.ANYTIME
    recurrence_interval: str | None = None  # "daily" or "weekly"; None means no auto-recurrence
    start_time: int | None = None           # minutes from midnight (e.g. 480 = 8:00 AM); None = unscheduled

    def update_priority(self, priority: Priority) -> None:
        """Set a new priority level for this task."""
        self.priority = priority

    def update_duration(self, minutes: int) -> None:
        """Update how long this task takes in minutes."""
        self.duration = minutes

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Task:
        """Return a fresh, uncompleted copy of this task for its next occurrence.
        Raises ValueError if recurrence_interval is not set."""
        if not self.recurrence_interval:
            raise ValueError(f"Task '{self.description}' has no recurrence_interval set.")
        return Task(
            description=self.description,
            duration=self.duration,
            priority=self.priority,
            is_recurring=self.is_recurring,
            completed=False,
            time_slot=self.time_slot,
            recurrence_interval=self.recurrence_interval,
            start_time=self.start_time,
        )

    def end_time(self) -> int | None:
        """Return the minute-from-midnight when this task ends, or None if unscheduled."""
        return self.start_time + self.duration if self.start_time is not None else None

    def fmt_time(self, minutes: int) -> str:
        """Format minutes-from-midnight as HH:MM."""
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def get_summary(self) -> str:
        """Return a single-line string describing the task's key details."""
        status = "done" if self.completed else "pending"
        recur = " (recurring)" if self.is_recurring else ""
        return f"{self.description}{recur} — {self.duration} min [{self.priority.name}] [{status}]"


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_summary(self) -> str:
        """Return a one-line description of the pet and their task count."""
        return f"{self.name} ({self.breed}, {self.species}) — {len(self.tasks)} task(s)"


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time  # total minutes available today
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def update_available_time(self, minutes: int) -> None:
        """Update the total minutes the owner has available today."""
        self.available_time = minutes

    def update_pets(self, pet: Pet) -> None:
        """Replace an existing pet by name, or append if not found."""
        for i, p in enumerate(self.pets):
            if p.name == pet.name:
                self.pets[i] = pet
                return
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return the list of all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task across all pets, paired with its pet."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes, and schedules tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled_tasks: list[tuple[Pet, Task]] = []

    @property
    def available_time(self) -> int:
        return self.owner.available_time

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Collect every pending task from every pet."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if not task.completed
        ]

    def sort_by_priority(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort highest priority first, then by time slot (morning → evening → anytime), then shortest duration."""
        return sorted(tasks, key=lambda pt: (-pt[1].priority.value, pt[1].time_slot.value, pt[1].duration))

    def sort_by_time_slot(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort strictly by time slot order, then by priority within each slot."""
        return sorted(tasks, key=lambda pt: (pt[1].time_slot.value, -pt[1].priority.value, pt[1].duration))

    def filter_by_pet(self, pet_name: str) -> list[tuple[Pet, Task]]:
        """Return only scheduled tasks belonging to the named pet."""
        return [(pet, task) for pet, task in self.scheduled_tasks if pet.name == pet_name]

    def get_pending_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all tasks (across all pets) that are not yet completed."""
        return [(pet, task) for pet, task in self.owner.get_all_tasks() if not task.completed]

    def get_completed_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all tasks (across all pets) that are marked completed."""
        return [(pet, task) for pet, task in self.owner.get_all_tasks() if task.completed]

    def generate_schedule(self) -> list[tuple[Pet, Task]]:
        """
        Greedily schedule tasks in priority order until available_time is exhausted.
        Recurring tasks are always included regardless of remaining time.
        """
        tasks = self.sort_by_priority(self.get_all_tasks())
        time_left = self.available_time
        self.scheduled_tasks = []

        for pet, task in tasks:
            if task.is_recurring:
                self.scheduled_tasks.append((pet, task))
            elif task.duration <= time_left:
                self.scheduled_tasks.append((pet, task))
                time_left -= task.duration

        return self.scheduled_tasks

    def detect_conflicts(self) -> list[str]:
        """Check scheduled tasks with a start_time for overlapping intervals.
        Returns a list of human-readable warning strings (empty if no conflicts)."""
        timed = [
            (pet, task)
            for pet, task in self.scheduled_tasks
            if task.start_time is not None
        ]

        warnings: list[str] = []
        for i in range(len(timed)):
            for j in range(i + 1, len(timed)):
                pet_a, task_a = timed[i]
                pet_b, task_b = timed[j]
                # Overlap when one task starts before the other ends
                if task_a.start_time < task_b.start_time + task_b.duration and \
                   task_b.start_time < task_a.start_time + task_a.duration:
                    a_range = f"{task_a.fmt_time(task_a.start_time)}–{task_a.fmt_time(task_a.end_time())}"
                    b_range = f"{task_b.fmt_time(task_b.start_time)}–{task_b.fmt_time(task_b.end_time())}"
                    warnings.append(
                        f"CONFLICT: [{pet_a.name}] '{task_a.description}' ({a_range}) "
                        f"overlaps [{pet_b.name}] '{task_b.description}' ({b_range})"
                    )
        return warnings

    def complete_task(self, pet: Pet, task: Task) -> Task | None:
        """Mark task complete. If it has a recurrence_interval, add the next
        occurrence to the pet and return it; otherwise return None."""
        task.mark_complete()
        if task.recurrence_interval in ("daily", "weekly"):
            next_task = task.next_occurrence()
            pet.add_task(next_task)
            return next_task
        return None

    def add_task(self, pet: Pet, task: Task) -> None:
        """Add a task directly to the given pet."""
        pet.add_task(task)

    def remove_task(self, pet: Pet, task: Task) -> None:
        """Remove a task from the given pet."""
        pet.remove_task(task)

    def edit_task(self, task: Task, description: str = None,
                  priority: Priority = None, duration: int = None,
                  is_recurring: bool = None) -> None:
        """Update any combination of a task's fields in place."""
        if description is not None:
            task.description = description
        if priority is not None:
            task.update_priority(priority)
        if duration is not None:
            task.update_duration(duration)
        if is_recurring is not None:
            task.is_recurring = is_recurring

    def display_schedule(self) -> str:
        """Render the scheduled tasks as a formatted, color-coded terminal string."""
        # ANSI color codes
        RED    = "\033[31m"
        YELLOW = "\033[33m"
        GREEN  = "\033[32m"
        CYAN   = "\033[36m"
        BOLD   = "\033[1m"
        DIM    = "\033[2m"
        RESET  = "\033[0m"

        PRIORITY_COLOR = {
            Priority.HIGH:   RED,
            Priority.MEDIUM: YELLOW,
            Priority.LOW:    GREEN,
        }

        WIDTH = 50
        border = "═" * WIDTH

        if not self.scheduled_tasks:
            return "No schedule generated yet. Call generate_schedule() first."

        # --- skipped tasks ---
        scheduled_set = set(id(t) for _, t in self.scheduled_tasks)
        skipped = [
            (pet, task)
            for pet, task in self.get_all_tasks()
            if id(task) not in scheduled_set and not task.is_recurring
        ]

        lines = []
        lines.append(f"╔{'═' * (WIDTH - 2)}╗")
        lines.append(f"║  {BOLD}🐾 PawPal+ Daily Schedule{RESET}{'':>{WIDTH - 28}}║")
        header_body = f"  Owner: {self.owner.name}  |  Budget: {self.available_time} min"
        lines.append(f"║{header_body:<{WIDTH - 2}}║")
        lines.append(f"╚{'═' * (WIDTH - 2)}╝")

        # group scheduled tasks by pet
        pet_groups: dict[str, list[tuple[Pet, Task]]] = {}
        for pet, task in self.scheduled_tasks:
            pet_groups.setdefault(pet.name, []).append((pet, task))

        for _, entries in pet_groups.items():
            pet_obj = entries[0][0]
            lines.append(f"\n  {BOLD}{CYAN}🐾 {pet_obj.name} ({pet_obj.breed}){RESET}")
            lines.append(f"  {'─' * (WIDTH - 4)}")
            for i, (_, task) in enumerate(entries, 1):
                color = PRIORITY_COLOR[task.priority]
                dot = f"{color}●{task.priority.name}{RESET}"
                recur = f"  {DIM}↺ recurring{RESET}" if task.is_recurring else ""
                slot = f"  {DIM}[{task.time_slot.name.lower()}]{RESET}" if task.time_slot != TimeSlot.ANYTIME else ""
                desc = f"{task.description:<22}"
                lines.append(f"   {i}. {desc} {task.duration:>3} min  {dot}{recur}{slot}")

        # footer
        scheduled_time = sum(t.duration for _, t in self.scheduled_tasks if not t.is_recurring)
        lines.append(f"\n{border}")
        skip_note = f"  Skipped: {len(skipped)} task(s)" if skipped else "  All tasks scheduled ✓"
        lines.append(f"  Scheduled: {scheduled_time} min  |{skip_note}")
        if skipped:
            for pet, task in skipped:
                lines.append(f"  {YELLOW}⚠  {task.description} skipped — needs {task.duration} min{RESET}")
        lines.append(border)

        return "\n".join(lines)
