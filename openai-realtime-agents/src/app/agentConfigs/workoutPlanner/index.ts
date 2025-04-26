import workoutPlanner from './workoutPlanner';
import injectPersonality from './injectPersonality';

// Set up the agent relationships
workoutPlanner.downstreamAgents = []; // Optional - allows cycling back for adjustments


// Export a function that returns agents with personality injected
export const getAgentsWithPersonality = (personalityName: string = "") => {
    return injectPersonality([workoutPlanner], personalityName);
};