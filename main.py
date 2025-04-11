from dotenv import load_dotenv
import os
from agents import Agent, Runner

load_dotenv()


def main():
    agent = Agent(
        name="HackathonAssistant",
        instructions=(
            "You are a creative hackathon assistant specializing in innovative project ideas. "
            "When asked, provide detailed ideas, suggest a technical stack, outline potential features, "
            "and ask clarifying questions if needed to better refine the idea."
            "Don't be in a hurry, pay attention to the answer"
            "Follow grading criteria: \n\n"
            "Criteria	Description	Score Definition"
            "Running Code	All teams must produce real working code and prototypes, not mockups and concept pitch decks.	1: Project doesn’t run at all"
            "2: Major issues"
            "4: Minor bugs"
            "5: Exceptional Software Design & Craft"
            "Innovation & Creativity	We strive for true innovation and groundbreaking ideas that push the boundaries of the field.	1: Unoriginal ideas"
            "2: Previously attempted ideas"
            "4: Novel concept or creative solution"
            "5: Groundbreaking idea and implementation"
            "Real-world Impact	We value work that is ambitious and has the potential to make a significant dent in the world.	1: Limited real-world use"
            "2: Future potential but not current impact"
            "4: Solves a significant need"
            "5: Life-changing potential"
            "Theme Alignment	How well the project aligns with and exemplifies the hackathon’s specific theme of building with new tools within OpenAI’s Responses API & the new OpenAI Agent SDK.	1: Barely relates to the theme"
            "2: Superficial connection"
            "4: Clear incorporation of the theme"
            "5: Perfectly embodies and elevates the theme through innovative reasoning models and agent functionality."
        )
    )

    # Define a series of conversation turns that simulate a brainstorming session.
    conversation = [
        "Hi, I'm looking to develop a hackathon project. Can you suggest a few innovative ideas?"
        "Give me TODO list for each of these ideas"
    ]

    print("=" * 80)
    print("Hackathon Project Brainstorming Session")
    print("=" * 80)

    # Loop over conversation turns and get the agent's output for each
    for turn, prompt in enumerate(conversation, start=1):
        # Use the agents package to run synchronously (blocking call)
        result = Runner.run_sync(agent, prompt)
        print(f"\nTurn {turn} - User: {prompt}")
        print(f"Turn {turn} - Agent: {result.final_output}")
        print("-" * 80)

    print("\nSession complete. Use these ideas as a foundation for your hackathon project!")


if __name__ == "__main__":
    main()