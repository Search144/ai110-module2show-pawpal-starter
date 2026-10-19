from datetime import datetime, timedelta
from pawpal_system import CareTask, Pet, Owner, Scheduler


def test_task_completion():
    """Verify that calling mark_completed() changes the task's is_completed status to True."""
    task = CareTask(title="Morning Walk", duration_minutes=30, priority="high")
    assert task.is_completed is False
    
    task.mark_completed()
    assert task.is_completed is True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Mochi", species="Dog", age=3)
    assert len(pet.tasks) == 0

    task = CareTask(title="Feeding", duration_minutes=10, priority="high")
    pet.add_task(task)
    
    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Feeding"


def test_sort_by_time():
    """Verify that tasks are sorted chronologically by their time slot."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog", age=3)
    owner.add_pet(pet)

    # Add tasks out of chronological order
    task_late = CareTask(title="Evening Grooming", duration_minutes=15, priority="low", time_slot="19:00")
    task_early = CareTask(title="Morning Walk", duration_minutes=30, priority="high", time_slot="07:30")
    task_mid = CareTask(title="Lunch Feeding", duration_minutes=10, priority="medium", time_slot="12:00")

    pet.add_task(task_late)
    pet.add_task(task_early)
    pet.add_task(task_mid)

    scheduler = Scheduler(available_time_minutes=120)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())

    assert sorted_tasks[0][1].time_slot == "07:30"
    assert sorted_tasks[1][1].time_slot == "12:00"
    assert sorted_tasks[2][1].time_slot == "19:00"


def test_recurring_task_generation():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    task = CareTask(
        title="Daily Medication",
        duration_minutes=5,
        priority="high",
        time_slot="09:00",
        frequency="daily",
        due_date=today_str
    )

    next_task = task.mark_completed()
    
    assert task.is_completed is True
    assert next_task is not None
    assert next_task.is_completed is False
    assert next_task.title == "Daily Medication"

    # Verify due date advanced by 1 day
    expected_next_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    assert next_task.due_date == expected_next_date


def test_conflict_detection():
    """Verify that the Scheduler flags duplicate start times across pets."""
    owner = Owner(name="Jordan")
    pet1 = Pet(name="Mochi", species="Dog", age=3)
    pet2 = Pet(name="Whisker", species="Cat", age=5)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = CareTask(title="Morning Walk", duration_minutes=30, priority="high", time_slot="08:00")
    task2 = CareTask(title="Breakfast", duration_minutes=10, priority="high", time_slot="08:00")

    pet1.add_task(task1)
    pet2.add_task(task2)

    scheduler = Scheduler(available_time_minutes=60)
    conflicts = scheduler.detect_conflicts(owner)

    assert len(conflicts) > 0
    assert "Conflict Warning" in conflicts[0]