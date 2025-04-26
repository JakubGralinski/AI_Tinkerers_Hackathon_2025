import { AllAgentConfigsType } from "@/app/types";
import simpleExample from "./simpleExample";
import workoutPlannerBase from "./workoutPlanner";
import { getAgentsWithPersonality } from "./workoutPlanner";

// Create specific personality versions of the workout planner
const davidGogginsAgents = getAgentsWithPersonality("David Goggins");
const arnoldAgents = getAgentsWithPersonality("Arnold Schawrzenegger");
const annaAgents = getAgentsWithPersonality("Anna Senyszyn");

export const allAgentSets: AllAgentConfigsType = {
  simpleExample,
  workoutPlanner: workoutPlannerBase,
  "David Goggins": davidGogginsAgents,
  "Arnold Schawrzenegger": arnoldAgents,
  "Anna Senyszyn": annaAgents,
};

// Set David Goggins as the default
export const defaultAgentSetKey = "David Goggins";
