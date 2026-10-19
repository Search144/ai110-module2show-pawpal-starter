from pawpal_system import CareTask, Pet


def test_task_completion():
    """Verify that calling mark_completed() changes the task's is_completed status to True."""
    task = CareTask(title="Walking Pet", duration_minutes=30, priority="high")
    assert task.is_completed is False
    
    task.mark_completed()
    assert task.is_completed is True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Crunch", species="Dog", age=3)
    assert len(pet.tasks) == 0

    task = CareTask(title="Feeding", duration_minutes=10, priority="high")
    pet.add_task(task)
    
    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Feeding"