import { execSync } from "child_process";
import fs from "fs";
import path from "path";

export const SYSTEM_PROMPT = `
You are an expert AI coding assistant.
You have access to the following tools:
1. run_command: Run a bash command and get the output.
2. read_file: Read the contents of a file.
3. write_file: Write contents to a file.

Always use these tools to interact with the system. Think step by step before calling a tool.
`;

export const TOOLS_SCHEMA = [
  {
    type: "function",
    function: {
      name: "run_command",
      description: "Run a bash command on the user's terminal",
      parameters: {
        type: "object",
        properties: {
          command: { type: "string", description: "The bash command to run" }
        },
        required: ["command"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "read_file",
      description: "Read the contents of a file",
      parameters: {
        type: "object",
        properties: {
          filepath: { type: "string", description: "Absolute path to the file" }
        },
        required: ["filepath"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "write_file",
      description: "Write content to a file",
      parameters: {
        type: "object",
        properties: {
          filepath: { type: "string", description: "Absolute path to the file" },
          content: { type: "string", description: "The content to write" }
        },
        required: ["filepath", "content"]
      }
    }
  }
];

export function executeTool(name: string, args: any): string {
  try {
    if (name === "run_command") {
      const output = execSync(args.command, { encoding: "utf-8", stdio: "pipe" });
      return output || "Command executed successfully with no output.";
    } 
    else if (name === "read_file") {
      return fs.readFileSync(args.filepath, "utf-8");
    } 
    else if (name === "write_file") {
      fs.mkdirSync(path.dirname(args.filepath), { recursive: true });
      fs.writeFileSync(args.filepath, args.content, "utf-8");
      return "File written successfully.";
    }
    return `Unknown tool: ${name}`;
  } catch (error: any) {
    return `Error executing tool ${name}: ${error.message}`;
  }
}
