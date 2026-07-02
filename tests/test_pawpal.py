from pawpal_system import Task, Pet, Owner, Scheduler, Priority, TimeSlot


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


def test_sort_by_time_slot_returns_chronological_order():
    pet = Pet(name="Huey", breed="Dachshund", species="Dog")
    pet.add_task(Task(description="Evening stroll", duration=15, priority=Priority.LOW,    time_slot=TimeSlot.EVENING))
    pet.add_task(Task(description="Afternoon play", duration=20, priority=Priority.MEDIUM, time_slot=TimeSlot.AFTERNOON))
    pet.add_task(Task(description="Morning walk",   duration=20, priority=Priority.HIGH,   time_slot=TimeSlot.MORNING))

    owner = Owner(name="Adam", available_time=120)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    sorted_tasks = scheduler.sort_by_time_slot(scheduler.get_all_tasks())
    slots = [task.time_slot for _, task in sorted_tasks]
    assert slots == sorted(slots, key=lambda s: s.value), "Tasks should be in chronological slot order"


def test_complete_daily_task_queues_next_occurrence():
    pet = Pet(name="Luna", breed="Doberman", species="Dog")
    walk = Task(description="Morning walk", duration=20, priority=Priority.HIGH,
                time_slot=TimeSlot.MORNING, recurrence_interval="daily")
    pet.add_task(walk)

    owner = Owner(name="Adam", available_time=60)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    next_task = scheduler.complete_task(pet, walk)

    assert walk.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.description == walk.description
    assert next_task.recurrence_interval == "daily"
    assert next_task is not walk  # clone, not the same object


def test_detect_conflicts_flags_overlapping_tasks():
    pet = Pet(name="Huey", breed="Dachshund", species="Dog")
    pet.add_task(Task(description="Feed breakfast", duration=10, priority=Priority.HIGH,
                      time_slot=TimeSlot.MORNING, start_time=480))   # 08:00–08:10
    pet.add_task(Task(description="Morning walk",   duration=20, priority=Priority.HIGH,
                      time_slot=TimeSlot.MORNING, start_time=485))   # 08:05–08:25  ← overlaps

    owner = Owner(name="Adam", available_time=60)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "Feed breakfast" in conflicts[0]
    assert "Morning walk" in conflicts[0]
