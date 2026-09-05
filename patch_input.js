const fs = require('fs');
let code = fs.readFileSync('index.tsx', 'utf-8');

// Replace onChange with onInput and add onSubmit
code = code.replace(
  /onChange=\{\(val: string\) => setInput\(val\)\}/,
  `onInput={(val: string) => setInput(val)}
            onSubmit={() => {
              const text = input().trim();
              if (!text) return;
              if (text === "/dark") { setTheme("dark"); setInput(""); setShowCommands(false); return; }
              if (text === "/light") { setTheme("light"); setInput(""); setShowCommands(false); return; }
              if (text === "/exit") { process.exit(0); }
              setMessages((prev) => [...prev, { role: "user", text }]);
              setInput("");
              setShowCommands(false);
              setTimeout(() => {
                setMessages((prev) => [...prev, { role: "agent", text: "Working on: " + text }]);
              }, 500);
            }}`
);
fs.writeFileSync('index.tsx', code);
