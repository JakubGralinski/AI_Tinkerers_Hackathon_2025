
I'll start by exploring this OpenAI realtime agents repository to give you a comprehensive understanding of its structure, components, and integration points. Let's first examine the key configuration files to understand the project setup.

Read file: package.json
Let me correct the path and check the package.json file:

Read file: openai-realtime-agents/package.json
Now, let's check the Python component that seems to be part of this project:

Read file: openai-realtime-agents/app.py
Let's examine the README to understand the project's purpose and features:

Read file: openai-realtime-agents/README.md
Let's explore the structure of the `src` directory to understand the codebase organization:

Ran tool
Let's look at the structure of the app directory:

Ran tool
Let's look at the main App.tsx file to understand the core application logic:

Read file: openai-realtime-agents/src/app/App.tsx
Let's explore the agent configurations to understand how they're structured:

Ran tool
Let's examine one of the agent configuration files to understand how agents are defined:

Read file: openai-realtime-agents/src/app/agentConfigs/simpleExample.ts
Let's examine the types.ts file to understand the data structures used in the application:

Read file: openai-realtime-agents/src/app/types.ts
Let's look at the API implementation to understand the backend integration:

Ran tool
Let's examine the session API endpoint:

Ran tool

Read file: openai-realtime-agents/src/app/api/session/route.ts
Let's check the realtime connection implementation:

Read file: openai-realtime-agents/src/app/lib/realtimeConnection.ts
Let's examine the more complex agent examples to understand the multi-agent workflow and orchestration:

Ran tool

Read file: openai-realtime-agents/src/app/agentConfigs/frontDeskAuthentication/index.ts

Read file: openai-realtime-agents/src/app/agentConfigs/frontDeskAuthentication/authentication.ts
Let's see how the Python API integration is implemented:

Ran tool

Read file: openai-realtime-agents/src/app/api/python/route.ts
Let's also examine the hooks implementation to better understand the client-side logic:

Ran tool

Read file: openai-realtime-agents/src/app/hooks/useHandleServerEvent.ts
Based on the comprehensive review of the repository, I'll now provide you with a clear guide to understanding and extending this OpenAI realtime agents application.

# OpenAI Realtime Agents with Next.js: A Developer's Guide

## Repository Architecture Overview

This repository demonstrates a Next.js application that integrates with OpenAI's Realtime API and Agents SDK to create multi-agent voice conversations. Here's the high-level architecture:

1. **Frontend (Next.js + TypeScript)**: 
   - Manages the user interface and WebRTC connections
   - Handles audio streaming and agent interactions

2. **Backend Components**:
   - Next.js API routes for session management and OpenAI integration
   - Optional Python Flask server for additional processing capabilities

3. **OpenAI Integration**:
   - Uses WebRTC for real-time audio streaming
   - Implements agent configurations with tool definitions
   - Supports multi-agent workflows with handoffs between agents

## Key Directories and Files

- `src/app`: Main application code
  - `App.tsx`: Core application component managing WebRTC connections and UI
  - `agentConfigs/`: Defines different agent configurations and behaviors
  - `api/`: Next.js API routes for server-side operations
  - `components/`: UI components for the application
  - `contexts/`: React context providers for state management
  - `hooks/`: Custom React hooks for handling events and logic
  - `lib/`: Utility functions including realtime connection setup
  - `types.ts`: TypeScript type definitions for the application

- `app.py`: Optional Python backend for extended functionality

## OpenAI Integration Points

### 1. Session Establishment

The application establishes a session with OpenAI's Realtime API through the `/api/session` endpoint:

```typescript
// src/app/api/session/route.ts
export async function GET() {
  const response = await fetch(
    "https://api.openai.com/v1/realtime/sessions",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gpt-4o-realtime-preview-2024-12-17",
      }),
    }
  );
  const data = await response.json();
  return NextResponse.json(data);
}
```

### 2. WebRTC Connection

The application establishes a WebRTC connection for real-time audio streaming:

```typescript
// src/app/lib/realtimeConnection.ts
export async function createRealtimeConnection(
  EPHEMERAL_KEY: string,
  audioElement: RefObject<HTMLAudioElement | null>
): Promise<{ pc: RTCPeerConnection; dc: RTCDataChannel }> {
  const pc = new RTCPeerConnection();
  
  // Set up audio handling
  pc.ontrack = (e) => {
    if (audioElement.current) {
      audioElement.current.srcObject = e.streams[0];
    }
  };
  
  // Get user microphone access
  const ms = await navigator.mediaDevices.getUserMedia({ audio: true });
  pc.addTrack(ms.getTracks()[0]);
  
  // Create data channel for events
  const dc = pc.createDataChannel("oai-events");
  
  // Create and set local description (offer)
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);
  
  // Send offer to OpenAI and get answer
  const response = await fetch(`${baseUrl}?model=${model}`, {
    method: "POST",
    body: offer.sdp,
    headers: {
      Authorization: `Bearer ${EPHEMERAL_KEY}`,
      "Content-Type": "application/sdp",
    },
  });
  
  // Set remote description (answer from OpenAI)
  const answerSdp = await response.text();
  await pc.setRemoteDescription({ type: "answer", sdp: answerSdp });
  
  return { pc, dc };
}
```

### 3. Agent Configuration

Agents are defined with instructions, tools, and downstream connections:

```typescript
// Example from src/app/agentConfigs/simpleExample.ts
const haiku: AgentConfig = {
  name: "haiku",
  publicDescription: "Agent that writes haikus.",
  instructions: "Ask the user for a topic, then reply with a haiku about that topic.",
  tools: [],
};

const greeter: AgentConfig = {
  name: "greeter",
  publicDescription: "Agent that greets the user.",
  instructions: "Please greet the user and ask them if they'd like a Haiku. If yes, transfer them to the 'haiku' agent.",
  tools: [],
  downstreamAgents: [haiku],
};
```

### 4. Tool Implementation and Function Calling

Tools are defined and implemented to extend agent capabilities:

```typescript
// Tool definition example
{
  type: "function",
  name: "authenticateUser",
  description: "Checks the caller's information to authenticate...",
  parameters: {
    type: "object",
    properties: {
      firstName: {
        type: "string",
        description: "The caller's first name",
      },
      // Other parameters...
    },
    required: ["firstName", "lastName", "dateOfBirth", "phoneNumber", "email"],
  },
}

// Tool handling in useHandleServerEvent.ts
const handleFunctionCall = async (functionCallParams: {
  name: string;
  call_id?: string;
  arguments: string;
}) => {
  const args = JSON.parse(functionCallParams.arguments);
  const currentAgent = selectedAgentConfigSet?.find(
    (a) => a.name === selectedAgentName
  );

  if (currentAgent?.toolLogic?.[functionCallParams.name]) {
    const fn = currentAgent.toolLogic[functionCallParams.name];
    const fnResult = await fn(args, transcriptItems);
    
    // Send result back to OpenAI
    sendClientEvent({
      type: "conversation.item.create",
      item: {
        type: "function_call_output",
        call_id: functionCallParams.call_id,
        output: JSON.stringify(fnResult),
      },
    });
    sendClientEvent({ type: "response.create" });
  }
  // Other handling...
};
```

## Step-by-Step Modification Guide

### 1. Creating a New Agent

To create a new agent:

1. Create a new file in `src/app/agentConfigs/` (e.g., `myAgent.ts`)
2. Define your agent configuration:

```typescript
import { AgentConfig } from "@/app/types";

const myCustomAgent: AgentConfig = {
  name: "custom_agent",
  publicDescription: "An agent that handles custom tasks",
  instructions: `
    # Personality and Tone
    You are a helpful assistant specialized in [your domain].
    
    # Instructions
    - Help users with [specific tasks]
    - Provide information about [relevant topics]
    
    # Conversation Flow
    [Define how the conversation should progress]
  `,
  tools: [
    {
      type: "function",
      name: "performCustomTask",
      description: "Performs a custom task based on user input",
      parameters: {
        type: "object",
        properties: {
          input: {
            type: "string",
            description: "User input for the custom task"
          }
        },
        required: ["input"]
      }
    }
  ],
  toolLogic: {
    performCustomTask: async (args, transcriptItems) => {
      // Implement your custom logic
      return { result: `Processed: ${args.input}` };
    }
  }
};

export default [myCustomAgent];
```

3. Add your agent to the index file:

```typescript
// src/app/agentConfigs/index.ts
import myCustomAgents from './myAgent';

export const allAgentSets = {
  // Existing agent sets...
  myCustomSet: myCustomAgents,
};

export const defaultAgentSetKey = 'simpleExample';
```

### 2. Implementing Multi-Agent Workflows

To create agents that can hand off to each other:

1. Define multiple agents in separate files
2. Connect them in an index file:

```typescript
// src/app/agentConfigs/myAgentSet/index.ts
import firstAgent from './firstAgent';
import secondAgent from './secondAgent';
import { injectTransferTools } from '../utils';

// Set up downstream relationships
firstAgent.downstreamAgents = [secondAgent];
secondAgent.downstreamAgents = [firstAgent];

// Inject transfer tools based on relationships
const agents = injectTransferTools([firstAgent, secondAgent]);

export default agents;
```

3. Implement the transfer logic in the agent instructions:

```typescript
instructions: `
  # Instructions
  ...
  When the user asks about [specific topic], transfer them to the 'second_agent'.
`
```

### 3. Integrating with Python Backend

To use the Python backend:

1. Make sure Flask is running (`python app.py`)
2. Add tools that call the Python endpoints:

```typescript
tools: [
  {
    type: "function",
    name: "call_python_process",
    description: "Call Python backend to process data",
    parameters: {
      type: "object",
      properties: {
        data: {
          type: "object",
          description: "The data to be processed"
        }
      },
      required: ["data"]
    }
  }
],
toolLogic: {
  call_python_process: async (args) => {
    const response = await fetch('/api/python/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args.data)
    });
    return await response.json();
  }
}
```

### 4. Adding v0.dev UI Components

To integrate UI components from v0.dev:

1. Get the component code from v0.dev
2. Create a new file in `src/app/components/`
3. Paste and adapt the component code
4. Import and use the component in your application

Example:

```tsx
// src/app/components/CustomButton.tsx
import React from 'react';

interface CustomButtonProps {
  text: string;
  onClick: () => void;
}

export default function CustomButton({ text, onClick }: CustomButtonProps) {
  return (
    <button 
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      onClick={onClick}
    >
      {text}
    </button>
  );
}

// Usage in App.tsx or other components
import CustomButton from './components/CustomButton';

// Then in your JSX
<CustomButton text="Connect" onClick={connectToRealtime} />
```

## Testing and Debugging

1. **Local Testing**:
   - Run the application with `npm run dev`
   - Use browser developer tools to monitor network requests and WebRTC connections
   - Check the event log in the application UI for detailed event information

2. **Debugging Tools**:
   - Use the console logs in the application for client-side debugging
   - Check the terminal running Next.js for server-side logs
   - Use the built-in event logging system to track interactions

3. **Common Issues**:
   - OpenAI API key issues: Check the .env file and ensure the key is valid
   - WebRTC connection problems: Check browser permissions for microphone access
   - Agent configuration errors: Verify JSON structure and required fields

## Next Steps

1. Review the official OpenAI documentation for latest API changes
2. Experiment with different agent configurations and tool implementations
3. Extend the Python backend for more advanced processing capabilities
4. Try implementing more complex multi-agent workflows

This guide provides a foundation for understanding and extending the OpenAI Realtime Agents application. The codebase is well-structured and follows modern React and TypeScript patterns, making it a good starting point for building your own agent-based applications.
