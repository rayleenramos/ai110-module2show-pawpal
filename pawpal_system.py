from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    description: str
    duration: int           # minutes
    priority: Priority
    is_recurring: bool = False
    completed: bool = False

    def update_priority(self, priority: Priority) -> None:
        self.priority = priority

    def update_duration(self, minutes: int) -> None:
        self.duration = minutes

    def mark_complete(self) -> None:
        self.completed = True

    def get_summary(self) -> str:
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
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)

    def get_summary(self) -> str:
        return f"{self.name} ({self.breed}, {self.species}) — {len(self.tasks)} task(s)"


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time  # total minutes available today
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def update_available_time(self, minutes: int) -> None:
        self.available_time = minutes

    def update_pets(self, pet: Pet) -> None:
        """Replace or re-add a pet (e.g. after editing pet details)."""
        for i, p in enumerate(self.pets):
            if p.name == pet.name:
                self.pets[i] = pet
                return
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
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
        """Sort (pet, task) pairs highest priority first, then by shortest duration."""
        return sorted(tasks, key=lambda pt: (-pt[1].priority.value, pt[1].duration))

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

    def add_task(self, pet: Pet, task: Task) -> None:
        pet.add_task(task)

    def remove_task(self, pet: Pet, task: Task) -> None:
        pet.remove_task(task)

    def edit_task(self, task: Task, description: str = None,
                  priority: Priority = None, duration: int = None,
                  is_recurring: bool = None) -> None:
        if description is not None:
            task.description = description
        if priority is not None:
            task.update_priority(priority)
        if duration is not None:
            task.update_duration(duration)
        if is_recurring is not None:
            task.is_recurring = is_recurring

    def display_schedule(self) -> str:
        if not self.scheduled_tasks:
            return "No schedule generated yet. Call generate_schedule() first."

        lines = [f"Daily Plan for {self.owner.name}'s pets "
                 f"({self.available_time} min available):"]
        current_pet = None
        for pet, task in self.scheduled_tasks:
            if pet != current_pet:
                lines.append(f"\n  {pet.name} ({pet.species}):")
                current_pet = pet
            lines.append(f"    • {task.get_summary()}")

        scheduled_time = sum(
            t.duration for _, t in self.scheduled_tasks if not t.is_recurring
        )
        lines.append(f"\nTotal scheduled time: {scheduled_time} min")
        return "\n".join(lines)
