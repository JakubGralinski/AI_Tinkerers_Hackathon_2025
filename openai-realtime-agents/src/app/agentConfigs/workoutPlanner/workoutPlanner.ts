import { AgentConfig } from "@/app/types";

const workoutPlanner: AgentConfig = {
    name: "workout_planner",
    publicDescription: "Agent that creates personalized workout and nutrition plans.",
    instructions: `
# Personality and Tone
## Identity
You are a knowledgeable and supportive fitness coach who specializes in creating personalized workout and nutrition plans. You have a deep understanding of exercise science, nutrition principles, and behavior change psychology. Your approach is evidence-based yet practical and adaptable to individual needs.

## Task
Your primary responsibility is to create tailored workout and nutrition plans based on the user's profile information. You'll consider their goals, current fitness level, preferences, constraints, and any other relevant factors to design an effective and sustainable plan.

## Demeanor
Supportive, encouraging, and empowering. You want users to feel confident in their ability to follow the plan and achieve their goals.

## Tone
Your communication style will adapt based on the profile analysis, but generally maintains a balance of professional expertise and approachable friendliness.

## Level of Enthusiasm
Variable based on profile analysis - ranging from highly energetic and motivational to calm and reassuring depending on what resonates with the user.

## Level of Formality
Adaptable based on profile analysis - can range from professional and clinical to casual and conversational.

## Level of Emotion
Moderately expressive - showing genuine care for the user's success and well-being without being overly emotional.

## Filler Words
Minimal to occasional, based on the profile analysis of what makes the user most comfortable.

## Pacing
Balanced - thorough enough to explain important concepts but concise enough to keep the user engaged.

## Other details
You have the ability to adapt your communication style based on the profile analysis received from the profile_analyzer agent. This allows you to connect with users in the way that will be most effective for their motivation and adherence.

# Instructions
- Review the user profile information provided by the profile_analyzer
- Adapt your communication style based on the profile analysis
- Use the createWorkoutPlan tool to generate a personalized workout and nutrition plan
- Present the plan to the user in a way that aligns with their communication preferences
- Answer any questions about the plan and provide clarification as needed
- Encourage the user to follow the plan and check back for adjustments

# Conversation States
[
  {
    "id": "1_review_profile",
    "description": "Review the user profile and analyze communication preferences",
    "instructions": [
      "Silently review the user profile information",
      "Adapt your communication style based on the profile analysis",
      "Acknowledge receipt of the user's information"
    ],
    "examples": [
      "Thanks for sharing all that information about your fitness goals and preferences. I've reviewed your profile and I'm ready to create a personalized plan that will help you achieve your goals."
    ],
    "transitions": [{
      "next_step": "2_create_plan",
      "condition": "After acknowledging receipt of information"
    }]
  },
  {
    "id": "2_create_plan",
    "description": "Generate the personalized workout and nutrition plan",
    "instructions": [
      "Explain that you're creating a personalized plan",
      "Call the createWorkoutPlan tool with the user's profile information",
      "Let the user know this might take a moment"
    ],
    "examples": [
      "I'm now going to create a personalized workout and nutrition plan based on your goals, fitness level, and preferences. This will take just a moment to generate..."
    ],
    "transitions": [{
      "next_step": "3_present_plan",
      "condition": "After receiving the workout and nutrition plan"
    }]
  },
  {
    "id": "3_present_plan",
    "description": "Present the personalized plan to the user",
    "instructions": [
      "Present the workout and nutrition plan in a clear, structured format",
      "Highlight how the plan addresses their specific goals and preferences",
      "Explain key components of the plan and why they were chosen"
    ],
    "examples": [
      "Here's your personalized workout and nutrition plan! I've focused on [specific goal] while taking into account your preference for [specific preference] and your available time of [time available].",
      "For your workouts, I've included [specific exercises] which will help you [specific benefit]. The nutrition plan emphasizes [specific nutrition approach] to support your [specific goal]."
    ],
    "transitions": [{
      "next_step": "4_answer_questions",
      "condition": "After presenting the plan"
    }]
  },
  {
    "id": "4_answer_questions",
    "description": "Answer questions and provide clarification about the plan",
    "instructions": [
      "Ask if the user has any questions about the plan",
      "Provide clear, thorough answers to any questions",
      "Offer clarification or modifications if needed"
    ],
    "examples": [
      "Do you have any questions about your plan? I'm happy to explain any part in more detail or suggest modifications if needed.",
      "If anything isn't clear or doesn't seem right for you, please let me know and we can adjust it."
    ],
    "transitions": [{
      "next_step": "5_conclusion",
      "condition": "After answering questions"
    }]
  },
  {
    "id": "5_conclusion",
    "description": "Conclude the conversation with encouragement and next steps",
    "instructions": [
      "Encourage the user to start implementing the plan",
      "Provide tips for success and adherence",
      "Explain how they can check back for adjustments or questions",
      "End on a positive, motivational note"
    ],
    "examples": [
      "You're all set to begin your fitness journey! Remember, consistency is key, and it's okay to start gradually. If you have any questions as you implement this plan or need adjustments, feel free to check back with us. I believe in you and know you can achieve your goals!"
    ],
    "transitions": []
  }
]
`,
    tools: [
        {
            type: "function",
            name: "createWorkoutPlan",
            description: "Generate a personalized workout and nutrition plan based on user profile",
            parameters: {
                type: "object",
                properties: {
                    profileData: {
                        type: "object",
                        description: "The user's profile information"
                    },
                    communicationPreferences: {
                        type: "object",
                        description: "Communication style preferences from profile analysis"
                    }
                },
                required: ["profileData"]
            }
        }
    ],
    toolLogic: {
        createWorkoutPlan: async (args) => {
            console.log("Creating workout plan with args:", args);

            try {
                // Call the Python backend endpoint
                const response = await fetch("http://localhost:5000/api/python/process", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        action: "create_workout_plan",
                        profileData: args.profileData,
                        communicationPreferences: args.communicationPreferences
                    })
                });

                if (!response.ok) {
                    throw new Error(`Error from Python API: ${response.statusText}`);
                }

                const data = await response.json();
                return data;

            } catch (error) {
                console.error("Error calling Python backend:", error);

                // Fallback response if Python backend fails
                return {
                    workoutPlan: {
                        weeklySchedule: [
                            {
                                day: "Monday",
                                focus: "Upper Body Strength",
                                exercises: [
                                    { name: "Push-ups", sets: 3, reps: "10-12" },
                                    { name: "Dumbbell Rows", sets: 3, reps: "10-12" },
                                    { name: "Shoulder Press", sets: 3, reps: "10-12" },
                                    { name: "Bicep Curls", sets: 3, reps: "10-12" }
                                ],
                                duration: "45 minutes",
                                intensity: "Moderate"
                            },
                            {
                                day: "Tuesday",
                                focus: "Cardio",
                                exercises: [
                                    { name: "Jogging/Running", duration: "30 minutes", intensity: "Moderate" }
                                ],
                                duration: "30 minutes",
                                intensity: "Moderate"
                            },
                            {
                                day: "Wednesday",
                                focus: "Lower Body Strength",
                                exercises: [
                                    { name: "Bodyweight Squats", sets: 3, reps: "15" },
                                    { name: "Lunges", sets: 3, reps: "10 each leg" },
                                    { name: "Glute Bridges", sets: 3, reps: "15" },
                                    { name: "Calf Raises", sets: 3, reps: "15" }
                                ],
                                duration: "45 minutes",
                                intensity: "Moderate"
                            },
                            {
                                day: "Thursday",
                                focus: "Rest Day",
                                exercises: [
                                    { name: "Light Walking", duration: "20 minutes", intensity: "Low" },
                                    { name: "Stretching", duration: "10 minutes", intensity: "Low" }
                                ],
                                duration: "30 minutes",
                                intensity: "Low"
                            },
                            {
                                day: "Friday",
                                focus: "Full Body Circuit",
                                exercises: [
                                    { name: "Jumping Jacks", duration: "30 seconds" },
                                    { name: "Mountain Climbers", duration: "30 seconds" },
                                    { name: "Plank", duration: "30 seconds" },
                                    { name: "Bodyweight Squats", duration: "30 seconds" },
                                    { name: "Push-ups", duration: "30 seconds" }
                                ],
                                notes: "Complete 3-4 rounds with 1 minute rest between rounds",
                                duration: "30-40 minutes",
                                intensity: "High"
                            },
                            {
                                day: "Saturday",
                                focus: "Cardio and Core",
                                exercises: [
                                    { name: "Brisk Walking/Jogging", duration: "20 minutes", intensity: "Moderate" },
                                    { name: "Plank", sets: 3, duration: "30 seconds" },
                                    { name: "Bicycle Crunches", sets: 3, reps: "15 each side" },
                                    { name: "Russian Twists", sets: 3, reps: "10 each side" }
                                ],
                                duration: "40 minutes",
                                intensity: "Moderate"
                            },
                            {
                                day: "Sunday",
                                focus: "Active Recovery",
                                exercises: [
                                    { name: "Yoga/Stretching", duration: "20-30 minutes", intensity: "Low" }
                                ],
                                duration: "20-30 minutes",
                                intensity: "Low"
                            }
                        ]
                    },
                    nutritionPlan: {
                        dailyCalories: "Based on your goals and activity level",
                        macroDistribution: {
                            protein: "30%",
                            carbohydrates: "40%",
                            fats: "30%"
                        },
                        mealPlan: [
                            {
                                meal: "Breakfast",
                                options: [
                                    "Oatmeal with fruit and nuts",
                                    "Greek yogurt with berries and granola",
                                    "Whole grain toast with avocado and eggs"
                                ]
                            },
                            {
                                meal: "Lunch",
                                options: [
                                    "Grilled chicken salad with mixed vegetables",
                                    "Quinoa bowl with vegetables and lean protein",
                                    "Turkey and avocado wrap with side salad"
                                ]
                            },
                            {
                                meal: "Dinner",
                                options: [
                                    "Baked salmon with roasted vegetables",
                                    "Lean beef stir-fry with brown rice",
                                    "Grilled chicken with sweet potato and steamed vegetables"
                                ]
                            },
                            {
                                meal: "Snacks (choose 2-3 per day)",
                                options: [
                                    "Apple with almond butter",
                                    "Protein shake",
                                    "Handful of nuts and dried fruit",
                                    "Carrot sticks with hummus",
                                    "Greek yogurt with honey"
                                ]
                            }
                        ],
                        hydration: "Aim for 8-10 glasses of water daily",
                        notes: "Adjust portions based on hunger and energy levels. Focus on whole, minimally processed foods when possible."
                    }
                };
            }
        }
    }
};

export default workoutPlanner; 