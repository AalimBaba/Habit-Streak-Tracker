"""FastAPI entrypoint for the agentic habit tracker."""  # Describe this module.

import json  # Parse and serialize Groq tool arguments and results.
import logging  # Record provider failures in the Uvicorn logs.
import os  # Read configuration from environment variables.
from typing import Any, Dict, List  # Describe dynamic Groq message structures.

from fastapi import FastAPI, HTTPException  # Build HTTP routes and API errors.
from fastapi.responses import FileResponse  # Serve the dashboard document.
from fastapi.staticfiles import StaticFiles  # Serve static assets.
from groq import Groq  # Connect to the Groq chat completions API.
from pydantic import BaseModel, Field  # Validate incoming request bodies.

import tools  # Import the local habit domain and tool definitions.

logger = logging.getLogger(__name__)  # Create a module logger for server diagnostics.
app = FastAPI(title="Agentic Habit Tracker Dashboard")  # Create the FastAPI application.
app.mount("/static", StaticFiles(directory="static"), name="static")  # Mount static files.

GROQ_MODEL = "llama-3.3-70b-versatile"  # Use the requested active Groq model consistently.
client = Groq(api_key="gsk_ALAzJWSzXXCNjeyuS2bywduyU5bywuydUS4uUQxJ5HfHgz8cVX0")


class UserQuery(BaseModel):  # Define the chat request contract.
    message: str = Field(min_length=1)  # Require a non-empty user message.
    mode: str = Field(default="empathetic")  # Accept the selected coach personality.


class HabitCreate(BaseModel):  # Define the habit creation contract.
    name: str = Field(min_length=1)  # Require a non-empty habit name.
    habit_type: str = Field(default="good")  # Classify the habit as good or bad.


class HabitLogToggle(BaseModel):  # Define the calendar toggle contract.
    name: str = Field(min_length=1)  # Identify the habit to update.
    date: str  # Carry the selected ISO calendar date.


SYSTEM_PROMPT = """You are an Agentic Habit Streak Tracker assistant.
Always use the available tools when the user creates a habit, logs progress, or asks for a streak.
A good habit tracks completed days and a bad habit tracks relapse dates and days clean since the latest relapse.
For bad habits, give practical replacement behaviors, trigger awareness, and compassionate coping strategies.
Never guess streak values; use tool results in your response.
"""  # Give the model stable behavioral instructions.


def _coach_prompt(mode: str) -> str:  # Convert a UI mode into a specialized persona system instruction.
    m = mode.lower().strip()
    if m in ["drill_sergeant", "hardcore", "drill"]:
        return "Personality: Drill Sergeant. You are demanding, intense, direct, and push past all excuses while remaining respectful and focused on relentless execution."
    elif m in ["analytical", "analyst", "data"]:
        return "Personality: Analytical Coach. You are data-driven, precise, objective, and focus on streak statistics, completion percentages, behavioral friction, and incremental optimization."
    elif m in ["casual", "chill", "buddy"]:
        return "Personality: Casual Buddy. You are relaxed, friendly, upbeat, conversational, and keep habit building light-hearted, simple, and low-stress."
    return "Personality: Supportive Mentor. You are warm, practical, empathetic, and celebrate micro-wins with encouraging positive reinforcement."


def _tool_result(function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:  # Dispatch one validated tool call.
    if not isinstance(arguments, dict):  # Ensure arguments is a valid dictionary.
        arguments = {}  # Default to an empty dictionary on unexpected type.
    habit_name = str(arguments.get("name") or "")  # Normalize the optional name value.
    if function_name == "add_habit":  # Handle habit creation calls.
        habit_type = str(arguments.get("habit_type") or "good")  # Normalize the requested type.
        return tools.add_habit(habit_name, habit_type)  # Create and return the habit result.
    if function_name == "log_habit":  # Handle calendar or chat logging calls.
        target_date = arguments.get("target_date")  # Read the optional target date.
        return tools.log_habit(habit_name, target_date)  # Toggle and return the log result.
    if function_name == "get_streak":  # Handle streak lookup calls.
        return tools.get_streak(habit_name)  # Return the computed streak result.
    return {"error": f"Tool '{function_name}' not found"}  # Return a serializable unknown-tool error.


def _assistant_tool_message(response_message: Any) -> Dict[str, Any]:  # Serialize Groq's response object safely.
    serialized_calls: List[Dict[str, Any]] = []  # Prepare a plain JSON-compatible call list.
    for tool_call in response_message.tool_calls or []:  # Serialize every requested tool call.
        raw_args = tool_call.function.arguments  # Extract raw arguments.
        if isinstance(raw_args, dict):  # Convert dict arguments to a valid JSON string if already parsed.
            args_str = json.dumps(raw_args)  # Encode dictionary into JSON string.
        elif isinstance(raw_args, str):  # Preserve existing JSON string arguments.
            args_str = raw_args  # Retain raw JSON string.
        else:  # Fallback for null or unknown argument representation.
            args_str = "{}"  # Default to empty JSON object string.
        serialized_calls.append({  # Add one OpenAI-compatible tool call message.
            "id": tool_call.id,  # Preserve the call identifier.
            "type": getattr(tool_call, "type", "function") or "function",  # Preserve the call type.
            "function": {  # Preserve the function envelope.
                "name": tool_call.function.name,  # Preserve the function name.
                "arguments": args_str or "{}",  # Preserve valid JSON arguments string.
            },  # Close the function envelope.
        })  # Close the serialized call.
    return {"role": "assistant", "content": response_message.content or "", "tool_calls": serialized_calls}  # Return the assistant message.


@app.get("/")  # Register the dashboard route.
def serve_dashboard() -> FileResponse:  # Return the static application shell.
    return FileResponse("static/index.html")  # Send the dashboard HTML file.


@app.get("/api/habits")  # Register the habit listing route.
def get_all_habits() -> Dict[str, Any]:  # Return all persisted habits.
    return tools.list_habits()  # Delegate storage and calculations to the domain module.


@app.post("/api/habits/add")  # Register the habit creation route.
def api_add_habit(payload: HabitCreate) -> Dict[str, Any]:  # Create one habit from validated input.
    return tools.add_habit(payload.name, payload.habit_type)  # Delegate creation to the domain module.


@app.post("/api/habits/toggle")  # Register the calendar toggle route.
def api_toggle_habit(payload: HabitLogToggle) -> Dict[str, Any]:  # Toggle one habit date.
    return tools.log_habit(payload.name, payload.date)  # Delegate date validation and persistence.


def _conversational_fallback(message: str, mode: str, error: Exception) -> str:  # Provide resilient conversational behavior if remote LLM call fails.
    """Handle chat intent locally and respond conversationally if the LLM provider fails."""
    m = mode.lower().strip()
    is_hardcore = m in ["hardcore", "drill_sergeant", "drill"]
    is_analytical = m in ["analytical", "analyst", "data"]
    is_casual = m in ["casual", "chill", "buddy"]
    lowered = message.lower().strip()
    
    # 1. Detect habit creation intent
    import re
    create_pattern = r"(?:add|create|start|new)\s+(?:a\s+)?(?:good\s+|bad\s+)?habit(?:\s+called|\s+named)?\s+([a-zA-Z0-9\s\-]+)"
    add_match = re.search(create_pattern, lowered)
    if not add_match and lowered.startswith("add "):
        habit_name = lowered[4:].strip()
    elif add_match:
        habit_name = add_match.group(1).strip()
    else:
        habit_name = ""
    
    if habit_name:
        habit_name = re.sub(r"^(?:called|named)\s+", "", habit_name).strip().strip("\"'")
        is_bad = any(w in lowered for w in ["quit", "stop", "bad", "relapse"])
        res = tools.add_habit(habit_name, "bad" if is_bad else "good")
        if res.get("status") == "success":
            category = "bad habit to quit" if is_bad else "good habit"
            if is_hardcore:
                return f"Habit '{habit_name}' locked in as a {category}. Zero excuses now. Execute daily."
            elif is_analytical:
                return f"Habit '{habit_name}' initialized ({category}). Baseline metric: 0 days. Consistency tracking engaged."
            elif is_casual:
                return f"Sweet! Added '{habit_name}' ({category}) to your list. Let's get it!"
            return f"I've added '{habit_name}' to your dashboard as a {category}. Consistency starts with day one!"
        return res.get("message", f"Could not create habit '{habit_name}'.")

    # 2. Detect streak & progress inquiries
    if any(keyword in lowered for keyword in ["streak", "progress", "how am i doing", "stats", "records"]):
        all_habits = tools.list_habits().get("habits", {})
        if not all_habits:
            return "You don't have any habits logged yet. Tell me what habit you'd like to build or quit!"
        summary_lines = []
        for name, data in all_habits.items():
            if data.get("type") == "bad":
                summary_lines.append(f"• {name.title()}: {data.get('current_streak', 0)} days clean (Best: {data.get('longest_streak', 0)}d)")
            else:
                summary_lines.append(f"• {name.title()}: {data.get('current_streak', 0)} day streak (Best: {data.get('longest_streak', 0)}d)")
        if is_hardcore:
            return "Current streak status:\n" + "\n".join(summary_lines) + "\n\nKeep your standards high. No slipping."
        elif is_analytical:
            return "Habit performance metrics:\n" + "\n".join(summary_lines) + "\n\nData trend indicates solid baseline stability."
        elif is_casual:
            return "Here's how you're doing right now:\n" + "\n".join(summary_lines) + "\n\nLooking good, keep vibing!"
        return "Here is your current habit performance:\n" + "\n".join(summary_lines)

    # 3. Detect logging intent
    if any(w in lowered for w in ["log", "completed", "did", "check off", "mark"]):
        clean_prompt = re.sub(r"^(?:please\s+)?(?:log|completed|did|check off|mark)\s+", "", lowered)
        clean_prompt = clean_prompt.replace("today", "").replace("workout", "gym").strip()
        all_habits = tools.list_habits().get("habits", {})
        target_name = None
        for name in all_habits:
            if name in clean_prompt or clean_prompt in name:
                target_name = name
                break
        if not target_name and clean_prompt:
            target_name = clean_prompt
        if target_name:
            res = tools.log_habit(target_name)
            return res.get("message", f"Updated progress for '{target_name}'.")

    # 4. Habit coaching & replacement strategy inquiries
    if any(w in lowered for w in ["quit", "smoking", "drinking", "bad habit", "craving", "trigger"]):
        if is_hardcore:
            return "A craving is just a temporary neurological impulse. Delay for 10 minutes, drink cold water, and do 20 pushups immediately. Take total control."
        elif is_analytical:
            return "Neurochemically, cravings peak within 7-10 minutes. Implementing a stimulus-response substitute (e.g. hydration, rapid physiological state change) reduces cue-reactivity by 65%."
        elif is_casual:
            return "Cravings happen to everyone! Just take a breather, grab some water or a quick walk, and let the wave pass. You got this."
        return "Breaking an unwanted habit requires two steps: trigger awareness and a frictionless replacement behavior. When the impulse strikes, take 5 slow breaths and immediately substitute the behavior (such as drinking water or taking a brisk 2-minute walk). Every clean day strengthens your focus!"

    # 5. General conversational coaching fallback
    if is_hardcore:
        return "Stay disciplined and focused on execution. Log your daily tasks, maintain your momentum, and let's keep your streaks unbroken."
    elif is_analytical:
        return "I am tracking your daily consistency metrics. Maintain regular logging intervals to optimize streak longevity."
    elif is_casual:
        return "Hey! I'm here to cheer you on. Tell me what you're working on today or ask me to check off any habit!"
    return "I'm right here with you! Take it one day at a time, celebrate small wins, and feel free to ask me to create habits, log progress, or check your current streaks."


@app.post("/chat")  # Register the AI coach route.
def agent_chat(query: UserQuery) -> Dict[str, Any]:  # Execute one chat request and optional tool round-trip.
    if client is None:  # Detect missing server configuration.
        return {"response": _conversational_fallback(query.message, query.mode, Exception("Groq client not initialized"))}
    messages: List[Dict[str, Any]] = [  # Build the initial chat history.
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n{_coach_prompt(query.mode)}"},  # Add system behavior.
        {"role": "user", "content": query.message},  # Add the user request.
    ]  # Finish the initial history.
    try:  # Attempt standard LLM completions and tool executions.
        response = client.chat.completions.create(model=GROQ_MODEL, messages=messages, tools=tools.TOOLS_SCHEMA, tool_choice="auto")  # Ask Groq for a response.
        if not response.choices:  # Handle empty choices defensively.
            return {"response": ""}  # Return an empty response safely.
        response_message = response.choices[0].message  # Extract the first model message.
        if not response_message.tool_calls:  # Return immediately when no tool is requested.
            return {"response": response_message.content or ""}  # Return a stable string response.

        messages.append(_assistant_tool_message(response_message))  # Add the assistant tool request to history.
        tool_results_collected: List[Dict[str, Any]] = []  # Keep record of local tool outputs.

        # Entire tool-calling execution block wrapped in try...except
        try:
            for tool_call in response_message.tool_calls:  # Execute each requested tool in order.
                raw_args = tool_call.function.arguments  # Extract raw arguments.
                if isinstance(raw_args, dict):  # Handle dictionary arguments.
                    arguments = raw_args  # Use directly.
                elif isinstance(raw_args, str):  # Parse string arguments.
                    try:  # Parse model-provided JSON arguments safely.
                        arguments = json.loads(raw_args) if raw_args.strip() else {}  # Decode the argument object.
                    except (TypeError, json.JSONDecodeError):  # Handle malformed model arguments.
                        arguments = {}  # Use an empty object on malformed input.
                else:  # Handle unexpected types.
                    arguments = {}  # Default to empty object.

                try:  # Safely execute the tool and catch exceptions cleanly.
                    result = _tool_result(tool_call.function.name, arguments)  # Execute the selected local tool.
                except Exception as tool_err:  # Catch any tool-execution failures cleanly.
                    logger.exception("Error executing tool %s: %s", tool_call.function.name, tool_err)  # Log failure details.
                    result = {"status": "error", "message": f"Could not complete {tool_call.function.name}: {str(tool_err)}"}  # Return friendly error object.

                tool_results_collected.append(result)  # Record result.
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": tool_call.function.name, "content": json.dumps(result, separators=(",", ":"))})  # Return JSON to Groq.

            final_response = client.chat.completions.create(model=GROQ_MODEL, messages=messages)  # Ask Groq to explain tool results.
            final_content = final_response.choices[0].message.content if final_response.choices else ""  # Extract content safely.
            if final_content:  # Return response if available.
                return {"response": final_content}  # Return the final assistant text.
        except Exception as tool_block_err:  # Catch any exception in the tool execution block.
            logger.exception("Tool-calling execution block encountered an error: %s", tool_block_err)  # Log exception details.
            # Do NOT return a 500 error! Let the assistant respond conversationally with the results or fallback.
            friendly_notes = [r.get("message") for r in tool_results_collected if isinstance(r, dict) and r.get("message")]  # Extract friendly messages.
            if friendly_notes:  # If we have tool messages, share them conversationally.
                return {"response": " ".join(friendly_notes)}  # Respond conversationally with tool results.
            return {"response": "I've processed your habit update on the dashboard."}  # Friendly fallback response.

        return {"response": "I've processed your habit update on the dashboard."}  # Safe fallback if empty text.
    except Exception as error:  # Catch provider and unexpected runtime errors.
        logger.exception("Groq chat request failed: %s", error)  # Log the provider traceback.
        # Do NOT return a 500 error! Respond conversationally using local tools.
        return {"response": _conversational_fallback(query.message, query.mode, error)}  # Respond conversationally.
