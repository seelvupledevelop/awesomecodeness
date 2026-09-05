import { render } from "@opentui/solid";
import { createCliRenderer } from "@opentui/core";
import { createSignal } from "solid-js";

function App() {
  const [theme] = createSignal("dark");
  
  const dim = () => theme() === "dark" ? "gray" : "#888888";
  const fg = () => theme() === "dark" ? "white" : "black";

  return (
    <box 
      flexDirection="column" 
      alignItems="center" 
      justifyContent="center" 
      width="100%" 
      height="100%" 
    >
      <box marginBottom={0}>
        <text color={dim()}>Awesome</text>
      </box>
      
      <box marginBottom={1}>
        <ascii_font text="AWESOME CODE" color="red" />
      </box>

      <box flexDirection="column" width={80}>
        <box flexDirection="row" marginBottom={1}>
          <text color="red">▎ </text>
          <input 
            placeholder="Type your message... (type / for commands)"
            flexGrow={1}
            color={fg()}
          />
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

      <box flexDirection="row" marginTop={2}>
        <text color="red">● Tip </text>
        <text color={dim()}>Run /dark for dark mode or /light for light mode</text>
      </box>

    </box>
  );
}

async function main() {
  const renderer = await createCliRenderer();
  render(() => <App />, renderer);
}

main().catch(console.error);
