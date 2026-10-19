from pawpal_system import Owner, Pet, CareTask, Scheduler


def main():
    # 1. Create Owner and Pets
    owner = Owner(name="Jordan", contact_info="jordan@example.com")
    pet1 = Pet(name="Crunch", species="Dog", age=3)
    pet2 = Pet(name="Snorkel", species="Cat", age=5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # 2. Add Care Tasks across pets with varying priorities & durations
    pet1.add_task(
        CareTask(title="Walking Pet", duration_minutes=30, priority="high", frequency="daily")
    )
    pet1.add_task(
        CareTask(title="Brushing Fur", duration_minutes=15, priority="low", frequency="weekly")
    )
    
    pet2.add_task(
        CareTask(title="Give Medication", duration_minutes=5, priority="high", frequency="daily")
    )
    pet2.add_task(
        CareTask(title="Play Session", duration_minutes=20, priority="medium", frequency="daily")
    )

    # 3. Schedule tasks with a time budget constraint (e.g., 60 available minutes)
    scheduler = Scheduler(available_time_minutes=60)
    scheduled_plan = scheduler.generate_daily_plan(owner)

    # 4. Formatted Terminal Output
    print("\n" + "=" * 50)
    print(f"🐾 TODAY'S PAWPAL+ SCHEDULE FOR {owner.name.upper()}'S PETS 🐾")
    print("=" * 50)

    if not scheduled_plan:
        print("No tasks could be scheduled.")
    else:
        for idx, item in enumerate(scheduled_plan, 1):
            p_badge = f"[{item['priority'].upper()}]"
            print(
                f"{idx}. {item['pet_name']} — {item['title']} ({item['duration_minutes']} min) {p_badge}"
            )

    print("-" * 50)
    print(scheduler.explain_plan(scheduled_plan))
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()