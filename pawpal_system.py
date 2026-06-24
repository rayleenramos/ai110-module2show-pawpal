from dataclasses import dataclass


@dataclass
class Pet:
    name: str
    breed: str
    species: str

    def get_summary(self) -> str:
        pass


@dataclass
class Task:
    type: str
    priority: str
    duration: int
    is_recurring: bool = False

    def update_priority(self, priority: str) -> None:
        pass

    def update_duration(self, minutes: int) -> None:
        pass

    def get_summary(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_available_time(self, minutes: int) -> None:
        pass

    def update_pets(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass


class Plan:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.task_list: list[Task] = []
        self.available_time: int = owner.available_time
        self.scheduled_tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def edit_task(self, task: Task) -> None:
        pass

    def sort_by_priority(self) -> list[Task]:
        pass

    def generate_plan(self) -> list[Task]:
        pass

    def display_plan(self) -> str:
        pass
