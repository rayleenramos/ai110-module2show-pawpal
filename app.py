import streamlit as st
from pawpal_system import Task, Owner, Pet, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# --- Owner + Pet Setup ---
st.subheader("Owner & Pet Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_time = st.number_input("Available time today (minutes)", min_value=1, max_value=480, value=60)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    breed = st.text_input("Breed", value="Mixed")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("Set up owner & pet"):
    pet = Pet(name=pet_name, breed=breed, species=species)
    owner = Owner(name=owner_name, available_time=int(available_time))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.scheduler = Scheduler(owner)
    st.success(f"Created owner **{owner_name}** with pet **{pet_name}** ({species})")

st.divider()

# --- Add Tasks ---
st.subheader("Add Tasks")

if st.session_state.owner is None:
    st.info("Set up an owner and pet above before adding tasks.")
else:
    owner: Owner = st.session_state.owner
    pets = owner.get_pets()
    pet_names = [p.name for p in pets]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        selected_pet_name = st.selectbox("Pet", pet_names)
    with col2:
        task_title = st.text_input("Task description", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority_str = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"], index=0)
    with col5:
        is_recurring = st.checkbox("Recurring")

    if st.button("Add task"):
        selected_pet = next(p for p in pets if p.name == selected_pet_name)
        task = Task(
            description=task_title,
            duration=int(duration),
            priority=Priority[priority_str],
            is_recurring=is_recurring,
        )
        st.session_state.scheduler.add_task(selected_pet, task)
        st.success(f"Added **{task_title}** to {selected_pet_name}")

    # Show current tasks per pet
    all_tasks = st.session_state.scheduler.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        rows = [
            {
                "Pet": pet.name,
                "Task": task.description,
                "Duration (min)": task.duration,
                "Priority": task.priority.name,
                "Recurring": "Yes" if task.is_recurring else "No",
            }
            for pet, task in all_tasks
        ]
        st.table(rows)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")

if st.session_state.scheduler is None:
    st.info("Set up an owner and pet above before generating a schedule.")
else:
    if st.button("Generate schedule"):
        scheduler: Scheduler = st.session_state.scheduler
        scheduled = scheduler.generate_schedule()

        if not scheduled:
            st.warning("No tasks could be scheduled. Try adding tasks or increasing available time.")
        else:
            st.success(f"Scheduled {len(scheduled)} task(s).")
            rows = [
                {
                    "Pet": pet.name,
                    "Task": task.description,
                    "Duration (min)": task.duration,
                    "Priority": task.priority.name,
                    "Recurring": "Yes" if task.is_recurring else "No",
                }
                for pet, task in scheduled
            ]
            st.table(rows)

            scheduled_time = sum(t.duration for _, t in scheduled if not t.is_recurring)
            st.caption(f"Total scheduled time: {scheduled_time} min / {scheduler.available_time} min available")
