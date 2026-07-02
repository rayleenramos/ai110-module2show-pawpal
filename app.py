import streamlit as st
from pawpal_system import Task, Owner, Pet, Scheduler, Priority, TimeSlot

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling — sort, filter, and detect conflicts in one place.")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ── Owner & Pet Setup ───────────────────────────────────────────────
st.subheader("Owner & Pet Info")
col1, col2 = st.columns(2)
with col1:
    owner_name     = st.text_input("Owner name", value="Jordan")
    available_time = st.number_input("Available time today (minutes)", min_value=1, max_value=480, value=60)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    breed    = st.text_input("Breed", value="Mixed")
    species  = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("Set up owner & pet"):
    pet   = Pet(name=pet_name, breed=breed, species=species)
    owner = Owner(name=owner_name, available_time=int(available_time))
    owner.add_pet(pet)
    st.session_state.owner     = owner
    st.session_state.scheduler = Scheduler(owner)
    st.success(f"Created owner **{owner_name}** with pet **{pet_name}** ({species})")

st.divider()

# ── Add Tasks ───────────────────────────────────────────────────────
st.subheader("Add a Task")

if st.session_state.owner is None:
    st.info("Set up an owner and pet above before adding tasks.")
else:
    owner: Owner = st.session_state.owner
    pets         = owner.get_pets()
    pet_names    = [p.name for p in pets]

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_pet_name = st.selectbox("Pet", pet_names)
        task_title        = st.text_input("Task description", value="Morning walk")
    with col2:
        duration     = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        priority_str = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"])
    with col3:
        time_slot_str = st.selectbox("Time slot", ["MORNING", "AFTERNOON", "EVENING", "ANYTIME"])
        start_time_input = st.text_input("Start time (HH:MM, optional)", value="")
        is_recurring  = st.checkbox("Recurring")
        interval      = st.selectbox("Recurrence interval", ["None", "daily", "weekly"]) if is_recurring else "None"

    start_time = None
    if start_time_input.strip():
        try:
            h, m   = map(int, start_time_input.strip().split(":"))
            start_time = h * 60 + m
        except ValueError:
            st.warning("Start time must be in HH:MM format (e.g. 08:00). Ignoring.")

    if st.button("Add task"):
        selected_pet = next(p for p in pets if p.name == selected_pet_name)
        task = Task(
            description=task_title,
            duration=int(duration),
            priority=Priority[priority_str],
            time_slot=TimeSlot[time_slot_str],
            is_recurring=is_recurring,
            recurrence_interval=interval if interval != "None" else None,
            start_time=start_time,
        )
        st.session_state.scheduler.add_task(selected_pet, task)
        st.success(f"Added **{task_title}** to {selected_pet_name}")

    # Current task list
    all_tasks = st.session_state.scheduler.get_all_tasks()
    if all_tasks:
        st.markdown("**Current tasks (unsorted)**")
        st.table([
            {
                "Pet":          pet.name,
                "Task":         task.description,
                "Duration":     f"{task.duration} min",
                "Priority":     task.priority.name,
                "Time slot":    task.time_slot.name.lower(),
                "Start":        f"{task.start_time // 60:02d}:{task.start_time % 60:02d}" if task.start_time else "—",
                "Recurring":    "Yes" if task.is_recurring else "No",
            }
            for pet, task in all_tasks
        ])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ────────────────────────────────────────────────
st.subheader("Generate Schedule")

if st.session_state.scheduler is None:
    st.info("Set up an owner and pet above before generating a schedule.")
else:
    scheduler: Scheduler = st.session_state.scheduler

    col_a, col_b = st.columns(2)
    sort_mode = col_a.radio("Sort by", ["Priority (high → low)", "Time slot (chronological)"], horizontal=True)
    pet_filter = col_b.selectbox(
        "Filter by pet",
        ["All pets"] + [p.name for p in owner.get_pets()],
    )

    if st.button("Generate schedule"):
        scheduled = scheduler.generate_schedule()

        if not scheduled:
            st.warning("No tasks could be scheduled. Try adding tasks or increasing available time.")
        else:
            # Apply sort
            if sort_mode == "Time slot (chronological)":
                display_tasks = scheduler.sort_by_time_slot(scheduled)
            else:
                display_tasks = scheduler.sort_by_priority(scheduled)

            # Apply pet filter
            if pet_filter != "All pets":
                display_tasks = [(p, t) for p, t in display_tasks if p.name == pet_filter]

            scheduled_time = sum(t.duration for _, t in scheduled if not t.is_recurring)
            budget         = scheduler.available_time
            pct            = int(scheduled_time / budget * 100) if budget else 0

            st.success(f"Scheduled **{len(scheduled)} task(s)** — {scheduled_time} / {budget} min used ({pct}%)")
            st.progress(min(pct, 100))

            if display_tasks:
                st.table([
                    {
                        "Pet":       pet.name,
                        "Task":      task.description,
                        "Duration":  f"{task.duration} min",
                        "Priority":  task.priority.name,
                        "Time slot": task.time_slot.name.lower(),
                        "Start":     f"{task.start_time // 60:02d}:{task.start_time % 60:02d}" if task.start_time else "—",
                        "Recurring": "↺" if task.is_recurring else "—",
                        "Status":    "✓ done" if task.completed else "pending",
                    }
                    for pet, task in display_tasks
                ])
            else:
                st.info(f"No scheduled tasks for {pet_filter}.")

            # Skipped tasks
            scheduled_ids = {id(t) for _, t in scheduled}
            skipped = [(p, t) for p, t in scheduler.get_all_tasks() if id(t) not in scheduled_ids and not t.is_recurring]
            if skipped:
                with st.expander(f"⚠ {len(skipped)} task(s) skipped (budget exceeded)"):
                    for pet, task in skipped:
                        st.warning(f"**{task.description}** ({pet.name}) — needs {task.duration} min")

            # Conflict detection
            st.markdown("---")
            st.markdown("**Conflict detection**")
            conflicts = scheduler.detect_conflicts()
            if conflicts:
                for warning in conflicts:
                    st.warning(warning)
            else:
                st.success("No scheduling conflicts detected ✓")
