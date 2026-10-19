from dataclasses import dataclass, field
from typing import List


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str  # e.g., "low", "medium", "high"
    is_completed: bool = False

    def mark_completed(self) -> None:
        """Mark this care task as completed."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a care task to the pet's schedule list."""
        pass

    def remove_task(self, task_title: str) -> None:
        """Remove a task by its title."""
        pass


@dataclass
class Owner:
    name: str
    contact_info: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        pass

    def update_preferences(self, preferences: dict) -> None:
        """Update owner care preferences."""
        pass


class Scheduler:
    def __init__(self, available_time_minutes: int):
        self.available_time_minutes = available_time_minutes

    def filter_and_prioritize_tasks(self, tasks: List[CareTask]) -> List[CareTask]:
        """Filter and sort tasks based on priority and constraints."""
        pass

    def generate_daily_plan(self, pet: Pet) -> List[CareTask]:
        """Generate an optimized daily schedule for the pet."""
        pass

    def explain_plan(self, scheduled_tasks: List[CareTask]) -> str:
        """Provide a clear explanation of why each task was chosen and scheduled."""
        pass