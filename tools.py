"""Domain tools for good habits, bad habits, and streak calculations."""  # Describe this module.

from datetime import date, datetime  # Work with validated calendar dates.
from typing import Any, Dict, List, Optional  # Describe JSON-shaped records.

from memory import load_data, save_data  # Use the local JSON persistence layer.

DEFAULT_USER = "u_1024"  # Identify the single local user record.
DATE_FORMAT = "%Y-%m-%d"  # Define the only accepted storage date format.


def compute_streak(dates_sorted_desc: List[date], anchor: Optional[date] = None) -> int:  # Count consecutive completed days.
    if not dates_sorted_desc:  # Handle an empty completion history.
        return 0  # Report no streak.
    if anchor and (anchor - dates_sorted_desc[0]).days > 1:  # Detect an inactive current streak.
        return 0  # Require the latest completion to be today or yesterday.
    streak = 1  # Count the newest completed day.
    for index in range(len(dates_sorted_desc) - 1):  # Compare each neighboring date.
        delta = (dates_sorted_desc[index] - dates_sorted_desc[index + 1]).days  # Measure the calendar gap.
        if delta == 1:  # Continue only for adjacent days.
            streak += 1  # Extend the streak by one day.
        elif delta > 1:  # Stop at the first missed day.
            break  # Preserve the consecutive prefix only.
    return streak  # Return the calculated streak.


def _normalise_type(habit_type: Optional[str]) -> str:  # Normalize a habit classification.
    return "bad" if str(habit_type or "good").lower().strip() == "bad" else "good"  # Allow only good or bad.


def _new_record(habit_type: Optional[str] = None) -> Dict[str, Any]:  # Create a new backward-compatible record.
    return {"created_at": str(date.today()), "type": _normalise_type(habit_type), "log": [], "current_streak": 0, "longest_streak": 0, "milestones_awarded": []}  # Return the initial record.


def _parse_log(record: Dict[str, Any]) -> List[date]:  # Convert valid stored strings into dates.
    parsed: List[date] = []  # Prepare the parsed date collection.
    for value in record.get("log", []):  # Inspect every stored log value.
        try:  # Validate each stored date independently.
            parsed.append(datetime.strptime(str(value), DATE_FORMAT).date())  # Add the valid date.
        except (TypeError, ValueError):  # Ignore malformed legacy values.
            continue  # Continue processing the remaining log.
    return sorted(set(parsed), reverse=True)  # Remove duplicates and sort newest first.


def _calculate_streak(record: Dict[str, Any]) -> int:  # Calculate a good streak or bad-habit clean period.
    logged = _parse_log(record)  # Parse the habit's stored dates.
    if record.get("type", "good") == "bad":  # Treat logged dates as relapse dates for bad habits.
        last_relapse = logged[0] if logged else None  # Find the latest relapse.
        if not last_relapse:  # Handle a bad habit with no relapse recorded.
            created = datetime.strptime(record.get("created_at", str(date.today())), DATE_FORMAT).date()  # Read its start date.
            return max(0, (date.today() - created).days + 1)  # Count clean days since creation.
        return max(0, (date.today() - last_relapse).days)  # Count clean days since relapse.
    return compute_streak(logged, date.today())  # Calculate a normal completion streak.


def _update_milestones(record: Dict[str, Any], current_streak: int) -> List[int]:  # Award newly reached streak milestones.
    awarded = set(record.get("milestones_awarded", []))  # Read previously awarded thresholds.
    newly_awarded = [threshold for threshold in (7, 30, 90) if current_streak >= threshold and threshold not in awarded]  # Find new thresholds.
    record["milestones_awarded"] = sorted(awarded.union(newly_awarded))  # Persist the complete award history.
    return newly_awarded  # Return only awards created by this update.


def add_habit(name: str, habit_type: str = "good") -> Dict[str, Any]:  # Create a typed habit.
    clean_name = str(name or "").lower().strip()  # Normalize the user-provided name.
    if not clean_name:  # Reject an empty name.
        return {"status": "error", "message": "Habit name is required."}  # Return a serializable validation result.
    clean_type = _normalise_type(habit_type)  # Normalize the requested habit type.
    data = load_data()  # Load the current store.
    user_data = data.setdefault(DEFAULT_USER, {"habits": {}})  # Ensure the user container exists.
    habits = user_data.setdefault("habits", {})  # Ensure the habits mapping exists.
    if clean_name in habits:  # Detect duplicate names.
        return {"status": "exists", "message": f"Habit '{clean_name}' already exists."}  # Avoid overwriting existing data.
    habits[clean_name] = _new_record(clean_type)  # Store the new typed record.
    save_data(data)  # Persist the new habit.
    return {"status": "success", "habit": clean_name, "type": clean_type, "message": f"{clean_type.title()} habit '{clean_name}' created successfully!"}  # Confirm creation.


def log_habit(name: str, target_date: Optional[str] = None) -> Dict[str, Any]:  # Toggle a completion or relapse date.
    clean_name = str(name or "").lower().strip()  # Normalize the habit name.
    if not clean_name:  # Reject an empty tool argument.
        return {"status": "error", "message": "Habit name is required."}  # Return a safe validation result.
    log_date = target_date or str(date.today())  # Default to today's date.
    try:  # Validate the requested date before changing data.
        parsed_log_date = datetime.strptime(str(log_date), DATE_FORMAT).date()  # Require an ISO date.
    except (TypeError, ValueError):  # Handle invalid date input.
        return {"status": "error", "message": "Date must use YYYY-MM-DD format."}  # Return a safe validation result.
    if parsed_log_date > date.today():  # Reject future dates strictly.
        return {"status": "error", "message": "Cannot log habits for future dates."}  # Return a validation error.
    data = load_data()  # Load the current store.
    user_data = data.setdefault(DEFAULT_USER, {"habits": {}})  # Ensure the user container exists.
    habits = user_data.setdefault("habits", {})  # Ensure the habits mapping exists.
    if clean_name not in habits:  # Handle chat logging for a new habit.
        habits[clean_name] = _new_record("good")  # Create unknown chat habits as good habits.
    habit_record = habits[clean_name]  # Select the record to update.
    log = habit_record.setdefault("log", [])  # Ensure the log list exists.
    if log_date in log:  # Toggle an existing date off.
        log.remove(log_date)  # Remove the completion or relapse.
        status = "removed"  # Describe the toggle result.
    else:  # Toggle a missing date on.
        log.append(log_date)  # Add the completion or relapse.
        status = "success"  # Describe the toggle result.
    habit_record.setdefault("type", "good")  # Migrate legacy records on write.
    current_streak = _calculate_streak(habit_record)  # Recalculate the current metric.
    habit_record["current_streak"] = current_streak  # Store the current metric.
    habit_record["longest_streak"] = max(habit_record.get("longest_streak", 0), current_streak)  # Preserve the best metric.
    newly_awarded = _update_milestones(habit_record, current_streak)  # Update milestone state.
    save_data(data)  # Persist the updated record.
    label = "Days clean" if habit_record["type"] == "bad" else "Current streak"  # Select the user-facing metric label.
    return {"habit": clean_name, "date_logged": log_date, "status": status, "current_streak": current_streak, "longest_streak": habit_record["longest_streak"], "type": habit_record["type"], "milestones_awarded": newly_awarded, "message": f"Updated '{clean_name}' for {log_date}. {label}: {current_streak}."}  # Return the update.


def get_streak(name: str) -> Dict[str, Any]:  # Return one habit's current metrics and log.
    clean_name = str(name or "").lower().strip()  # Normalize the lookup name.
    data = load_data()  # Load the current store.
    habits = data.get(DEFAULT_USER, {}).get("habits", {})  # Read the user's habits safely.
    habit_record = habits.get(clean_name)  # Find the requested record.
    if not habit_record:  # Handle an unknown habit.
        return {"habit": clean_name, "current_streak": 0, "longest_streak": 0, "is_active_today": False, "log": []}  # Return an empty result.
    habit_record.setdefault("type", "good")  # Migrate legacy records in memory.
    parsed_dates = _parse_log(habit_record)  # Parse valid log dates.
    latest_date = parsed_dates[0] if parsed_dates else None  # Find the latest event.
    current_streak = _calculate_streak(habit_record)  # Calculate the current metric.
    return {"habit": clean_name, "current_streak": current_streak, "longest_streak": max(habit_record.get("longest_streak", 0), current_streak), "last_logged": str(latest_date) if latest_date else None, "is_active_today": latest_date == date.today(), "type": habit_record["type"], "log": habit_record.get("log", [])}  # Return the complete summary.


def list_habits() -> Dict[str, Any]:  # Return all habits for the dashboard.
    data = load_data()  # Load the current store.
    habits = data.get(DEFAULT_USER, {}).get("habits", {})  # Read the habits safely.
    summaries: Dict[str, Any] = {}  # Prepare the dashboard result.
    for name, record in habits.items():  # Summarize every stored habit.
        summaries[name] = {"type": record.get("type", "good"), "current_streak": _calculate_streak(record), "longest_streak": record.get("longest_streak", 0), "log": record.get("log", []), "created_at": record.get("created_at", str(date.today()))}  # Add one summary.
    return {"habits": summaries}  # Return the dashboard payload.


TOOLS_SCHEMA = [  # Define the functions exposed to Groq tool calling.
    {  # Describe the add_habit tool.
        "type": "function",  # Mark this schema entry as a function.
        "function": {  # Open the function definition.
            "name": "add_habit",  # Expose the creation function name.
            "description": "Create a habit; use good to build it or bad to quit it.",  # Explain when the model should call it.
            "parameters": {  # Define the JSON argument object.
                "type": "object",  # Require an object.
                "properties": {  # Define accepted properties.
                    "name": {"type": "string", "description": "Habit name."},  # Describe the habit name.
                    "habit_type": {"type": "string", "enum": ["good", "bad"], "description": "Habit category."},  # Describe the category.
                },  # Close properties.
                "required": ["name"],  # Require the habit name.
            },  # Close parameters.
        },  # Close function.
    },  # Close add_habit schema.
    {"type": "function", "function": {"name": "log_habit", "description": "Toggle a completion or relapse date.", "parameters": {"type": "object", "properties": {"name": {"type": "string"}, "target_date": {"type": "string", "description": "YYYY-MM-DD date."}}, "required": ["name"]}}},  # Define the log_habit tool.
    {"type": "function", "function": {"name": "get_streak", "description": "Retrieve streak or days-clean metrics.", "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}}},  # Define the get_streak tool.
]  # Finish the tool schema.
