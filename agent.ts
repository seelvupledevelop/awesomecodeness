import { TOOLS_SCHEMA, executeTool, SYSTEM_PROMPT } from "./tools";

const API_KEY = process.env.OPENROUTER_API_KEY || "";

export async function chat(
  messages: any[], 
  onUpdate: (role: string, text: string) => void
) {
  let currentMessages = [
    { role: "system", content: SYSTEM_PROMPT },
    ...messages
  ];

  let steps = 0;
  
  while (steps < 10) {
    steps++;
    try {
      const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "nvidia/nemotron-3-super-120b-a12b:free",
          messages: currentMessages,
          tools: TOOLS_SCHEMA
        })
      });

      if (!response.ok) {
        onUpdate("error", `API Error: ${response.statusText}`);
        return;
      }

      const data = await response.json();
      const message = data.choices[0].message;

      if (message.content) {
        onUpdate("agent", message.content);
        currentMessages.push(message);
      }

      if (message.tool_calls && message.tool_calls.length > 0) {
        currentMessages.push(message);
        
        for (const call of message.tool_calls) {
          const name = call.function.name;
          const args = JSON.parse(call.function.arguments || "{}");
          
          onUpdate("agent", `[Tool Call] ${name}(${JSON.stringify(args)})`);
          
          const result = executeTool(name, args);
          
          onUpdate("system", `[Tool Result] ${result.substring(0, 200)}...`);
          
          currentMessages.push({
            role: "tool",
            tool_call_id: call.id,
            name: name,
            content: result
          });
        }
      } else {
        // No tool calls, we're done
        break;
      }

    } catch (e: any) {
      onUpdate("error", `Exception: ${e.message}`);
      break;
    }
  }
}
