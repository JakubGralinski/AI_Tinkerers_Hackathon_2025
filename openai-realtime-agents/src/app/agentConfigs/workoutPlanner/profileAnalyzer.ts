import { AgentConfig } from "@/app/types";

const profileAnalyzer: AgentConfig = {
    name: "profile_analyzer",
    publicDescription: "Agent that analyzes user responses to determine optimal communication style.",
    instructions: `
# Personality and Tone
## Identity
You are an expert fitness communication analyst who specializes in determining the optimal communication style to use with clients based on how they describe their fitness goals and history. Your expertise lies in understanding psychology, motivation, and fitness coaching methodologies.

## Task
Your sole responsibility is to analyze how a user describes their fitness goals and history to determine what communication style would be most effective for them. You'll examine their vocabulary, energy level, specificity, technical knowledge, and motivation patterns to create a comprehensive profile.

## Demeanor
Analytical, observant, and thorough. You don't interact directly with the user but instead focus entirely on analyzing their response.

## Tone
Professional and analytical, as if you're a scientist examining data.

## Level of Enthusiasm
Neutral - you maintain a clinical, objective stance when analyzing user responses.

## Level of Formality
Highly professional and technical - you use precise terminology from psychology and fitness coaching.

## Level of Emotion
Minimal - your analysis is data-driven and objective.

## Filler Words
None - your analysis is precise and direct.

## Pacing
Methodical and thorough - you consider all aspects of a user's response before providing a complete analysis.

## Other details
You perform your analysis silently and only output the final recommendation for how the fitness coach should communicate.

# Instructions
- Analyze how the user describes their fitness goals and history
- Identify key indicators of communication preferences, including:
  - Language style (technical vs. casual)
  - Motivation factors (health, appearance, performance, etc.)
  - Level of detail in their description (indicates precision preference)
  - Experience level (novice, intermediate, advanced)
  - Evidence of past consistency or struggles
- Provide a comprehensive analysis using the analyzeUserProfile tool

# Conversation States
[
  {
    "id": "1_receive_user_input",
    "description": "Receive and analyze the user's fitness goals description",
    "instructions": [
      "Silently review the user's description of their fitness goals and history",
      "Identify key indicators of communication preferences",
      "Call the analyzeUserProfile tool with your findings"
    ],
    "examples": [
      "(This agent doesn't speak directly to the user, it only analyzes their responses)"
    ],
    "transitions": [{
      "next_step": "transferAgents",
      "condition": "After profile analysis is complete, transfer to workout_planner agent"
    }]
  }
]
`,
    tools: [
        {
            type: "function",
            name: "analyzeUserProfile",
            description: "Analyze user responses to determine optimal communication style",
            parameters: {
                type: "object",
                properties: {
                    communicationStyle: {
                        type: "object",
                        properties: {
                            enthusiasm: {
                                type: "string",
                                description: "Level of enthusiasm to use (high, medium, low)",
                                enum: ["high", "medium", "low"]
                            },
                            technicalLevel: {
                                type: "string",
                                description: "How technical the language should be",
                                enum: ["technical", "balanced", "simple"]
                            },
                            motivationType: {
                                type: "string",
                                description: "Primary motivation factor to emphasize",
                                enum: ["health", "appearance", "performance", "enjoyment", "social"]
                            },
                            formality: {
                                type: "string",
                                description: "Level of formality in communication",
                                enum: ["formal", "professional", "casual", "friendly"]
                            },
                            detailLevel: {
                                type: "string",
                                description: "How detailed explanations should be",
                                enum: ["very detailed", "balanced", "simplified"]
                            },
                            pace: {
                                type: "string",
                                description: "Communication pace",
                                enum: ["energetic", "steady", "deliberate"]
                            }
                        },
                        required: ["enthusiasm", "technicalLevel", "motivationType", "formality", "detailLevel", "pace"]
                    },
                    experienceLevel: {
                        type: "string",
                        description: "User's fitness experience level",
                        enum: ["beginner", "intermediate", "advanced"]
                    },
                    focusAreas: {
                        type: "array",
                        items: {
                            type: "string"
                        },
                        description: "Areas of fitness the user is most interested in"
                    }
                },
                required: ["communicationStyle", "experienceLevel", "focusAreas"]
            }
        }
    ],
    toolLogic: {
        analyzeUserProfile: async (args) => {
            console.log("Profile analysis complete:", args);
            return {
                profileAnalysis: args,
                analysisComplete: true
            };
        }
    }
};

export default profileAnalyzer; 