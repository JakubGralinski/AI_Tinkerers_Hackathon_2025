import { AgentConfig } from "@/app/types";

const workout_planner: AgentConfig = {
  name: "workout_planner",
  publicDescription: "Agent that creates workout plans.",
  instructions:
    "Create a workout plan based on the user's goals. ALWAYS USE planWithBackend TOOL. You can also process or analyze data using Python backend services.",
  tools: [
    {
      type: "function",
      name: "planWithBackend",
      description: "Create a workout plan based on the user's goals.",
      parameters: {
        type: "object",
        properties: {
          instructions: {
            type: "string",
            description: "User prompt",
          },
        },
        required: [],
      },
    },
    {
      type: "function",
      name: "planWithBackend",
      description: "Create a workout plan based on the user's goals.",
      parameters: {
        type: "object",
        properties: {
          instructions: {
            type: "string",
            description: "User prompt",
          },
        },
        required: [],
      },
    },

  ],
  toolLogic: {
    planWithBackend: async ({ instructions }) => {
      console.log(
        `[toolLogic] is calling backend with instructions - ${instructions}`
      );
      const response = await fetch("http://127.0.0.1:5000/api/plans/", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          instructions: instructions,
        }),
      });

      const data = await response.json();
      console.log("[toolLogic] Response from backend:", data);

      return data;
    },
  },
  downstreamAgents: [],
};