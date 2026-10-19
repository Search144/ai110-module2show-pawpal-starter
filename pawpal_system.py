from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str  # e.g., "low", "medium", "high"
    time_slot: str = "08:00"  # Format "HH:MM"
    frequency: str = "daily"  # e.g., "daily", "weekly", "once"
    is_completed: bool = False
    due_date: str = datetime.now().strftime("%Y-%m-%d")

    def mark_completed(self) -> Any:
        """Mark this care task as completed and return a recurring instance if applicable."""
        self.is_completed = True
        
        if self.frequency.lower() == "daily":
            current_due = datetime.strptime(self.due_date, "%Y-%m-%d")
            next_due = current_due + timedelta(days=1)
            return CareTask(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                time_slot=self.time_slot,
                frequency=self.frequency,
                is_completed=False,
                due_date=next_due.strftime("%Y-%m-%d")
            )
        elif self.frequency.lower() == "weekly":
            current_due = datetime.strptime(self.due_date, "%Y-%m-%d")
            next_due = current_due + timedelta(weeks=1)
            return CareTask(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                time_slot=self.time_slot,
                frequency=self.frequency,
                is_completed=False,
                due_date=next_due.strftime("%Y-%m-%d")
            )
        return None


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a care task to the pet's schedule list."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove a task by its title."""
        self.tasks = [t for t in self.tasks if t.title != task_title]


@dataclass
class Owner:
    name: str
    contact_info: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update owner care preferences."""
        pass

    def get_all_tasks(self) -> List[Tuple[Pet, CareTask]]:
        """Return a combined list of every pet's tasks paired with their pet reference."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    def __init__(self, available_time_minutes: int):
        self.available_time_minutes = available_time_minutes

    def sort_by_time(self, tasks: List[Tuple[Pet, CareTask]]) -> List[Tuple[Pet, CareTask]]:
        """Sort tasks chronologically by their time_slot string in 'HH:MM' format."""
        return sorted(tasks, key=lambda item: item[1].time_slot)

    def filter_tasks(self, owner: Owner, pet_name: str = None, status: bool = None) -> List[Tuple[Pet, CareTask]]:
        """Filter tasks by specific pet name or completion status."""
        all_tasks = owner.get_all_tasks()
        filtered = []
        for pet, task in all_tasks:
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            if status is not None and task.is_completed != status:
                continue
            filtered.append((pet, task))
        return filtered

    def detect_conflicts(self, owner: Owner) -> List[str]:
        """Detect if multiple tasks are scheduled at the exact same time slot across pets."""
        time_slot_map = {}
        conflicts = []
        
        for pet, task in owner.get_all_tasks():
            slot = task.time_slot
            if slot in time_slot_map:
                conflicts.append(
                    f"Conflict Warning: '{task.title}' for {pet.name} overlaps at {slot} with '{time_slot_map[slot]['task']}' for {time_slot_map[slot]['pet']}."
                )
            else:
                time_slot_map[slot] = {"task": task.title, "pet": pet.name}
        return conflicts

    def filter_and_prioritize_tasks(self, owner: Owner) -> List[Tuple[Pet, CareTask]]:
        """Retrieve all active tasks, sort them chronologically by time slot, and prioritize them."""
        priority_mapping = {"high": 3, "medium": 2, "low": 1}
        active_tasks = self.filter_tasks(owner, status=False)
        time_sorted = self.sort_by_time(active_tasks)

        # Stable sort giving precedence to priority
        sorted_tasks = sorted(
            time_sorted,
            key=lambda item: priority_mapping.get(item[1].priority.lower(), 1),
            reverse=True
        )
        return sorted_tasks

    def generate_daily_plan(self, owner: Owner) -> List[Dict[str, Any]]:
        """Build an optimized daily schedule fitting sorted tasks within available time."""
        sorted_tasks = self.filter_and_prioritize_tasks(owner)
        daily_plan = []
        time_spent = 0

        for pet, task in sorted_tasks:
            if time_spent + task.duration_minutes <= self.available_time_minutes:
                daily_plan.append({
                    "pet_name": pet.name,
                    "title": task.title,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "time_slot": task.time_slot,
                    "frequency": task.frequency
                })
                time_spent += task.duration_minutes
            else:
                break

        return daily_plan

    def explain_plan(self, scheduled_tasks: List[Dict[str, Any]]) -> str:
        """Provide a clear text breakdown explaining why tasks were chosen."""
        if not scheduled_tasks:
            return "No tasks could be scheduled within the given time limit."
        
        explanation = "Schedule breakdown and reasoning:\n"
        total_time = sum(item["duration_minutes"] for item in scheduled_tasks)
        
        for idx, item in enumerate(scheduled_tasks, 1):
            explanation += (
                f"{idx}. [{item['time_slot']}] [{item['priority'].upper()}] {item['title']} for {item['pet_name']} "
                f"({item['duration_minutes']} min) - Selected based on chronological time and priority.\n"
            )
        explanation += f"\nTotal planned time: {total_time} minutes out of {self.available_time_minutes} minutes available."
        return explanation