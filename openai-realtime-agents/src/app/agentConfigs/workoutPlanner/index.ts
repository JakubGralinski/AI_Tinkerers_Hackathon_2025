import profileCollector from './profileCollector';
import profileAnalyzer from './profileAnalyzer';
import workoutPlanner from './workoutPlanner';
import { injectTransferTools } from '../utils';

// Set up the agent relationships
profileCollector.downstreamAgents = [profileAnalyzer];
profileAnalyzer.downstreamAgents = [workoutPlanner];
workoutPlanner.downstreamAgents = [profileCollector]; // Optional - allows cycling back for adjustments

// Add the transfer tools
const agents = injectTransferTools([profileCollector, profileAnalyzer, workoutPlanner]);

export default agents; 