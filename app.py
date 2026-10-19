import streamlit as st
from pawpal_system import Owner, Pet, CareTask, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, your intelligent pet care planning assistant.
Manage your pets, track daily care tasks, detect schedule conflicts, and generate optimized schedules!
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", contact_info="jordan@example.com")
    
    default_pet = Pet(name="Mochi", species="dog", age=3)
    default_pet.add_task(CareTask(title="Morning walk", duration_minutes=20, priority="high", time_slot="08:00"))
    st.session_state.owner.add_pet(default_pet)

owner = st.session_state.owner

# Household & Pet Management
with st.expander("Manage Household & Pets", expanded=True):
    owner.name = st.text_input("Owner name", value=owner.name)
    
    st.markdown("### Add a New Pet")
    new_pet_name = st.text_input("Pet name", value="", placeholder="e.g. Biscuit")
    new_species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species_select")
    new_age = st.number_input("Age", min_value=0, max_value=30, value=2)

    if st.button("Add Pet"):
        if new_pet_name.strip():
            if not any(p.name.lower() == new_pet_name.strip().lower() for p in owner.pets):
                new_pet = Pet(name=new_pet_name.strip(), species=new_species, age=int(new_age))
                owner.add_pet(new_pet)
                st.success(f"Added {new_pet.name} to your household!")
                st.rerun()
            else:
                st.warning(f"{new_pet_name} is already in your household.")
        else:
            st.error("Please provide a valid pet name.")

if owner.pets:
    st.markdown(f"### Current Pets in {owner.name}'s Household:")
    for pet in owner.pets:
        st.write(f"- **{pet.name}** ({pet.species.capitalize()}, Age {pet.age}) — {len(pet.tasks)} task(s) assigned")

st.divider()

# Conflict Detection Check
scheduler_instance = Scheduler(available_time_minutes=60)
conflicts = scheduler_instance.detect_conflicts(owner)
if conflicts:
    for conflict in conflicts:
        st.warning(f"⚠️ {conflict}")

# Task Management & Smart Filtering UI
st.subheader("Manage Tasks & Smart Schedule")
if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign task to pet", pet_names)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Evening walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        time_slot = st.text_input("Time (HH:MM)", value="09:00")
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add task"):
        target_pet = next((p for p in owner.pets if p.name == selected_pet_name), None)
        if target_pet and task_title.strip():
            new_task = CareTask(
                title=task_title.strip(),
                duration_minutes=int(duration),
                priority=priority,
                time_slot=time_slot.strip(),
                frequency=frequency
            )
            target_pet.add_task(new_task)
            st.success(f"Added '{task_title}' to {target_pet.name}'s schedule!")
            st.rerun()
        else:
            st.error("Please select a valid pet and enter a task title.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.markdown("### All Household Tasks (Chronological & Prioritized):")
        sorted_all_tasks = scheduler_instance.sort_by_time(all_tasks)
        task_table_data = [
            {
                "Pet": p.name,
                "Task": t.title,
                "Time": t.time_slot,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Completed": t.is_completed
            }
            for p, t in sorted_all_tasks
        ]
        st.table(task_table_data)
    else:
        st.info("No tasks added yet.")
else:
    st.warning("Please add at least one pet above before adding tasks.")

st.divider()

# Schedule Generation UI
st.subheader("Build Optimized Daily Plan")
available_time = st.slider("Available time today (minutes)", min_value=15, max_value=300, value=60, step=15)

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("No tasks available to schedule. Please add tasks to your pets first.")
    else:
        scheduler = Scheduler(available_time_minutes=available_time)
        daily_plan = scheduler.generate_daily_plan(owner)
        
        if not daily_plan:
            st.warning("No tasks could fit within your available time window.")
        else:
            st.success("Schedule generated successfully!")
            st.markdown("### 📋 Today's Optimized Plan")
            for idx, item in enumerate(daily_plan, 1):
                p_badge = f"[{item['priority'].upper()}]"
                st.write(f"**{idx}. [{item['time_slot']}] {item['pet_name']}** — {item['title']} ({item['duration_minutes']} min) {p_badge}")
            
            st.markdown("---")
            st.markdown("### 🧠 Scheduler Explanation")
            st.text(scheduler.explain_plan(daily_plan))