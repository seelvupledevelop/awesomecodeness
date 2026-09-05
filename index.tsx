import { render, useKeyboard } from "@opentui/solid";
import { createCliRenderer } from "@opentui/core";
import { createSignal, For, onMount, onCleanup } from "solid-js";
import { chat } from "./agent";

function App() {
  const [input, setInput] = createSignal("");
  const [theme, setTheme] = createSignal("dark");
  const [messages, setMessages] = createSignal<{role: string, text: string}[]>([]);
  const [showCommands, setShowCommands] = createSignal(false);
  const [isProcessing, setIsProcessing] = createSignal(false);
  const [cursorVisible, setCursorVisible] = createSignal(true);
  
  const dim = () => theme() === "dark" ? "gray" : "#888888";
  const fg = () => theme() === "dark" ? "white" : "black";
  const bg = () => theme() === "dark" ? "black" : "white";

  onMount(() => {
    const interval = setInterval(() => {
      setCursorVisible((c) => !c);
    }, 500);
    onCleanup(() => clearInterval(interval));
  });

  useKeyboard((key) => {
    if (isProcessing()) return;

    if (key.name === "return") {
      const text = input().trim();
      if (!text) return;

      if (text === "/dark") { setTheme("dark"); setInput(""); setShowCommands(false); return; }
      if (text === "/light") { setTheme("light"); setInput(""); setShowCommands(false); return; }
      if (text === "/exit") { process.exit(0); }

      setMessages((prev) => [...prev, { role: "user", text }]);
      setInput("");
      setShowCommands(false);
      setIsProcessing(true);

      const chatHistory = messages().map(m => ({ role: m.role, content: m.text })).filter(m => m.role === "user" || m.role === "assistant");
      chat(chatHistory, (role, text) => {
        setMessages((prev) => [...prev, { role, text }]);
      }).finally(() => {
        setIsProcessing(false);
      });
      
    } else if (key.name === "backspace") {
      if (input() === "") {
        setShowCommands(false);
      } else {
        setInput(input().slice(0, -1));
      }
    } else if (key.name === "tab") {
      setTheme(theme() === "dark" ? "light" : "dark");
    } else if (key.sequence === "/") {
      setInput(input() + "/");
      setShowCommands(true);
    } else if (key.sequence && key.sequence.length === 1 && !key.ctrl && !key.meta && !key.alt) {
      setInput(input() + key.sequence);
    }
  });

  return (
    <box 
      flexDirection="column" 
      alignItems="center" 
      justifyContent="center" 
      width="100%" 
      height="100%"
      backgroundColor={bg()}
    >
      <box marginBottom={0}>
        <text color={dim()}>Awesome</text>
      </box>
      
      <box marginBottom={1}>
        <ascii_font text="AWESOME CODE" color="red" />
      </box>

      {/* Chat History */}
      <box flexDirection="column" width={80} marginBottom={1}>
        <For each={messages()}>
          {(msg) => (
            <box flexDirection="row" marginBottom={1}>
              <text color={msg.role === "user" ? "cyan" : msg.role === "agent" ? "red" : "gray"}>
                {msg.role === "user" ? "You: " : msg.role === "agent" ? "Awesome: " : "System: "}
              </text>
              <text color={msg.role === "error" ? "red" : fg()}>{msg.text}</text>
            </box>
          )}
        </For>
      </box>

      {/* Command Menu Popup */}
      {showCommands() && (
        <box flexDirection="column" width={80} borderStyle="single" borderColor="blue" padding={1} marginBottom={1}>
          <text color="blue" bold>Available Skills / Commands</text>
          <text color={fg()}>/light   - Switch to light mode</text>
          <text color={fg()}>/dark    - Switch to dark mode</text>
          <text color={fg()}>/exit    - Quit application</text>
        </box>
      )}

      {/* Input Box Fixed (No Nested Texts) */}
      <box flexDirection="column" width={80}>
        <box flexDirection="row" marginBottom={1}>
          <text color="red">▎ </text>
          {isProcessing() ? (
            <text color={dim()}>Awesome is thinking...</text>
          ) : (
            <box flexDirection="row">
              {input() === "" ? (
                <text color={dim()}>Type your message... (type / for commands)</text>
              ) : (
                <text color={fg()}>{input()}</text>
              )}
              <text color="red">{cursorVisible() ? "█" : " "}</text>
            </box>
          )}
        </box>
        
        <box flexDirection="row" marginTop={0}>
          <text color="red">Build </text>
          <text color={dim()}>· Nemotron 3 Ultra (free) OpenRouter</text>
        </box>
      </box>

      <box flexDirection="row" width={80} justifyContent="space-between" marginTop={1}>
        <box flexDirection="row"><text bold color={fg()}>tab </text><text color={dim()}> switch mode</text></box>
        <box flexDirection="row"><text bold color={fg()}>ctrl+p </text><text color={dim()}> settings</text></box>
        <box flexDirection="row"><text bold color={fg()}>@ </text><text color={dim()}> attach file</text></box>
        <box flexDirection="row"><text bold color={fg()}>$ </text><text color={dim()}> subagent</text></box>
        <box flexDirection="row"><text bold color={fg()}>/ </text><text color={dim()}> commands</text></box>
      </box>

    </box>
  );
}

async function main() {
  const renderer = await createCliRenderer();
  render(() => <App />, renderer);
}

main().catch(console.error);
