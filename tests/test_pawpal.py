from pawpal_system import Task, Pet, Priority


def test_mark_complete_changes_status():
    task = Task(description="Morning walk", duration=20, priority=Priority.HIGH)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Huey", breed="Dachshund", species="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feed breakfast", duration=10, priority=Priority.HIGH))
    assert len(pet.tasks) == 1
    pet.add_task(Task(description="Bath time", duration=45, priority=Priority.MEDIUM))
    assert len(pet.tasks) == 2
