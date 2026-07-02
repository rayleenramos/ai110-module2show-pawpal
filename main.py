from pawpal_system import Task, Owner, Pet, Scheduler, Priority

owner = Owner(name="Adam", available_time=45)

huey = Pet(name="Huey", breed="Dachshund", species="Dog")
luna = Pet(name="Luna", breed="Doberman", species="Dog")
owner.add_pet(huey)
owner.add_pet(luna)

huey.add_task(Task("Morning walk", duration=20, priority=Priority.HIGH))
huey.add_task(Task("Feed breakfast", duration=10, priority=Priority.HIGH))
huey.add_task(Task("Bath time", duration=45, priority=Priority.MEDIUM))


luna.add_task(Task("Brush Teeth", duration=10, priority=Priority.MEDIUM))
luna.add_task(Task("Cut Nails", duration=15, priority=Priority.HIGH, is_recurring=True))

scheduler = Scheduler(owner)
scheduler.generate_schedule()
print(scheduler.display_schedule())