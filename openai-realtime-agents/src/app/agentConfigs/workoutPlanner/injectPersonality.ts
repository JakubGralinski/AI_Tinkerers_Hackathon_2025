import { AgentConfig } from "@/app/types";
import personalities, { WorkoutPersonality } from "./personalities";

/**
 * Injects personality-specific instructions into agent configs
 * @param agents Array of agent configs
 * @param personalityName Name of the personality to inject
 * @returns Array of modified agent configs
 */
export function injectPersonality(
    agents: AgentConfig[],
    personalityName: string
): AgentConfig[] {
    // If no personality selected or invalid, return original agents
    if (!personalityName || !personalities[personalityName]) {
        return agents;
    }

    const personality = personalities[personalityName];

    return agents.map(agent => {
        // Create a copy of the agent config
        const updatedAgent = { ...agent };

        // Get the appropriate personality instructions based on agent name
        let personalityInstructions: string | undefined;

        switch (agent.name) {
            case "profile_collector":
                personalityInstructions = personality.profileCollectorInstructions;
                break;
            case "profile_analyzer":
                personalityInstructions = personality.profileAnalyzerInstructions;
                break;
            case "workout_planner":
                personalityInstructions = personality.workoutPlannerInstructions;
                break;
            default:
                personalityInstructions = undefined;
        }

        // If we have personality instructions for this agent, modify the instructions
        if (personalityInstructions) {
            // Add personality instructions at the top of the instructions for clearer priority
            updatedAgent.instructions = personalityInstructions + "\n\n" + updatedAgent.instructions;
        }

        return updatedAgent;
    });
}

export default injectPersonality; 