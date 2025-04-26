from agents import Agent, Runner
from app.services.calendar_service import get_planned_dates

class PlanManagerAgent:
    def __init__(self, name, handoffs, model="gpt-4o"):
        self.agent = Agent(
            name=name,
            instructions=(
                "You are a fitness and nutrition manager AI.\n"
                "Based on the user's request, you decide whether to use the Meal Planner agent "
                "or the Exercise Planner agent or both. "
                "Return the correct agent's response or both of thems combined. Always use at least one of them. You can combine their responses, but do not return anything not from those tools."
            ),
            handoffs=handoffs,
            model=model,
        )

    async def run(self, user_prompt: str):
        events = get_planned_dates()

        calendar_summary = ""
        for start, end, title in events:
            calendar_summary += f"{start:%Y-%m-%d %H:%M} — {end:%H:%M} | {title}\n"

        enriched_prompt = f"""
User's Google Calendar Events pls consider it in the planning phase:
{calendar_summary}

User's Instruction:
{user_prompt}
"""
        task = Runner.run(self.agent, enriched_prompt)
        result = await task
        return result.final_output
