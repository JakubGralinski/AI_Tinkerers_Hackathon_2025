import { AgentConfig } from "@/app/types";
import { injectTransferTools } from "./utils";

// Define agents
const haiku: AgentConfig = {
  name: "haiku",
  publicDescription: "Agent that writes haikus.", // Context for the agent_transfer tool
  instructions:
    "Ask the user for a topic, then reply with a haiku about that topic.",
  tools: [],
};

const greeter: AgentConfig = {
  name: "greeter",
  publicDescription: "Agent that greets the user.",
  instructions:
    "Please greet the user and ask them if they'd like a Haiku. If yes, transfer them to the 'haiku' agent.",
  tools: [],
  downstreamAgents: [haiku],
};

const workout_planner: AgentConfig = {
  name: "workout_planner",
  publicDescription: "Agent that creates workout plans.",
  instructions: "Create a workout plan based on the user's goals. You can also process or analyze data using Python backend services.",
  tools: [
    {
      type: "function",
      name: "create_workout_plan",
      description: "Create a workout plan based on the user's goals.",
      parameters: {
        type: "object",
        properties: {},
        required: [],
      },
    },
    {
      type: "function",
      name: "call_python_process",
      description: "Call Python backend to process data",
      parameters: {
        type: "object",
        properties: {
          data: {
            type: "object",
            description: "The data to be processed by the Python backend"
          }
        },
        required: ["data"]
      }
    },
    {
      type: "function",
      name: "call_python_analyze",
      description: "Call Python backend to analyze data",
      parameters: {
        type: "object",
        properties: {
          data: {
            type: "object",
            description: "The data to be analyzed by the Python backend"
          }
        },
        required: ["data"]
      }
    }
  ],
  downstreamAgents: [haiku],
};

// add the transfer tool to point to downstreamAgents
const agents = injectTransferTools([greeter, haiku, workout_planner]);

export default agents;
