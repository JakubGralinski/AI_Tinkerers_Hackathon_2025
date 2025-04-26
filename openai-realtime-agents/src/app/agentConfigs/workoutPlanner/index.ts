import profileCollector from './profileCollector';
import profileAnalyzer from './profileAnalyzer';
import workoutPlanner from './workoutPlanner';
import { injectTransferTools } from '../utils';
import injectPersonality from './injectPersonality';

// Set up the agent relationships
profileCollector.downstreamAgents = [profileAnalyzer];
profileAnalyzer.downstreamAgents = [workoutPlanner];
workoutPlanner.downstreamAgents = [profileCollector]; // Optional - allows cycling back for adjustments

// Create the base agents with transfer tools
const baseAgents = injectTransferTools([profileCollector, profileAnalyzer, workoutPlanner]);

// Export a function that returns agents with personality injected
export const getAgentsWithPersonality = (personalityName: string = "") => {
    return injectPersonality(baseAgents, personalityName);
};

// Default export for backward compatibility
export default baseAgents; 