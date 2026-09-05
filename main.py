import os
import json
import httpx
import subprocess
import asyncio
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Label, Input, RichLog, OptionList
from textual.containers import Vertical, Horizontal

class Config:
    def __init__(self):
        self.provider = "Custom"
        self.api_base = "http://localhost:11434/v1"
        self.api_key = ""
        self.model = "qwen2.5-coder:3b"
        self.persona = "Default"
        self.project_dir = os.getcwd()
        self.skills = {
            "Terminal Execution": True,
            "Web Search": False,
            "IDE Integration": False
        }

config = Config()

class TrustScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("│\n●  Accessing workspace:\n│\n│  " + config.project_dir + "\n│", classes="bold"),
            Label("│  Quick safety check: Is this a project you created or one you trust?\n│  Awesome Code will be able to read, edit, and execute files here.\n│\n◇", classes="info"),
            Button("Yes, I trust this folder", id="btn_trust", variant="error"),
            Button("No, exit", id="btn_exit"),
            id="trust_container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_trust":
            self.app.push_screen(ConfigScreen())
        elif event.button.id == "btn_exit":
            self.app.exit()

class ConfigScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("🔥 Awesome Engine Configuration\n", classes="title"),
            Label(id="lbl_provider", classes="info"),
            Label(id="lbl_url", classes="info"),
            Label(id="lbl_model", classes="info"),
            Label(id="lbl_persona", classes="info"),
            Label(""),
            Button("Set API Provider Template", id="btn_provider"),
            Button("Set API Key", id="btn_key"),
            Button("Set Custom Model", id="btn_model"),
            Button("Set Agent Persona", id="btn_persona"),
            Button("Manage Awesome Skills", id="btn_skills"),
            Button("Execute Dalai-Lama (Local Models)", id="btn_dalai"),
            Button("Start Chat", id="btn_chat", variant="error"),
            id="config_container"
        )

    def on_mount(self) -> None:
        self.update_labels()

    def update_labels(self) -> None:
        self.query_one("#lbl_provider", Label).update(f"Current Provider: {config.provider}")
        self.query_one("#lbl_url", Label).update(f"Current URL: {config.api_base}")
        self.query_one("#lbl_model", Label).update(f"Current Model: {config.model}")
        self.query_one("#lbl_persona", Label).update(f"Current Persona: {config.persona}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_provider":
            self.app.push_screen(ProviderScreen())
        elif event.button.id == "btn_key":
            self.app.push_screen(KeyScreen())
        elif event.button.id == "btn_model":
            self.app.push_screen(ModelScreen())
        elif event.button.id == "btn_persona":
            self.app.push_screen(PersonaScreen())
        elif event.button.id == "btn_skills":
            self.app.push_screen(SkillsScreen())
        elif event.button.id == "btn_dalai":
            self.app.push_screen(DalaiScreen())
        elif event.button.id == "btn_chat":
            self.app.push_screen(ChatScreen())

class ModelScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Enter Model ID (e.g. gpt-4o, qwen/qwen-2.5-coder-32b-instruct):", classes="title"),
            Input(placeholder="Model name...", id="model_input", value=config.model),
            Button("Save", id="btn_save"),
            Button("Back", id="btn_back")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_save":
            config.model = self.query_one("#model_input", Input).value
        self.app.pop_screen()

class SkillsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("╔══════════════════════════════════════════════════════╗\n║               Manage Awesome Skills                  ║\n╚══════════════════════════════════════════════════════╝", classes="title"),
            OptionList(
                f"[ {'X' if config.skills['Terminal Execution'] else ' '} ] Terminal Execution Sandbox",
                f"[ {'X' if config.skills['Web Search'] else ' '} ] Web Search Plugin",
                f"[ {'X' if config.skills['IDE Integration'] else ' '} ] IDE Integration Hooks",
                id="skills_list"
            ),
            Label("\nUse Enter to toggle skills. These enhance what your agent can do natively!"),
            Button("Back", id="btn_back")
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        idx = event.option_index
        keys = list(config.skills.keys())
        key = keys[idx]
        config.skills[key] = not config.skills[key]
        
        # Re-render list
        lst = self.query_one("#skills_list", OptionList)
        lst.clear_options()
        lst.add_options([
            f"[ {'X' if config.skills['Terminal Execution'] else ' '} ] Terminal Execution Sandbox",
            f"[ {'X' if config.skills['Web Search'] else ' '} ] Web Search Plugin",
            f"[ {'X' if config.skills['IDE Integration'] else ' '} ] IDE Integration Hooks"
        ])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class ProviderScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("╔══════════════════════════════════════════════════════╗\n║               Select API Provider                    ║\n╚══════════════════════════════════════════════════════╝", classes="title"),
            OptionList(
                "OpenRouter (https://openrouter.ai/api/v1)",
                "NVIDIA (https://integrate.api.nvidia.com/v1)",
                "OpenAI (https://api.openai.com/v1)",
                "DeepInfra (https://api.deepinfra.com/v1/openai)",
                "Local/Custom",
                id="provider_list"
            ),
            Button("Back", id="btn_back")
        )
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        opt = event.option.prompt
        if "OpenRouter" in opt:
            config.provider = "OpenRouter"
            config.api_base = "https://openrouter.ai/api/v1"
            config.model = "qwen/qwen-2.5-coder-32b-instruct"
        elif "NVIDIA" in opt:
            config.provider = "NVIDIA"
            config.api_base = "https://integrate.api.nvidia.com/v1"
            config.model = "nvidia/nemotron-3-super-120b-a12b:free"
        elif "OpenAI" in opt:
            config.provider = "OpenAI"
            config.api_base = "https://api.openai.com/v1"
            config.model = "gpt-4o-mini"
        elif "DeepInfra" in opt:
            config.provider = "DeepInfra"
            config.api_base = "https://api.deepinfra.com/v1/openai"
            config.model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        else:
            config.provider = "Custom"
            config.api_base = "http://localhost:11434/v1"
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class KeyScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Enter API Key:", classes="title"),
            Input(placeholder="sk-...", id="api_key_input", password=True),
            Button("Save", id="btn_save")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        config.api_key = self.query_one("#api_key_input", Input).value
        self.app.pop_screen()

class PersonaScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("╔══════════════════════════════════════════════════════╗\n║               Select Agent Persona                   ║\n╚══════════════════════════════════════════════════════╝", classes="title"),
            OptionList(
                "Default",
                "Bastard",
                "Marvin",
                "ChosenOne",
                "Jedi",
                "Sith",
                id="persona_list"
            ),
            Button("Back", id="btn_back")
        )
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        config.persona = str(event.option.prompt)
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class DalaiScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("╔══════════════════════════════════════════════════════╗\n║               Execute Dalai-Lama                     ║\n╚══════════════════════════════════════════════════════╝", classes="title"),
            OptionList(
                "qwen2.5-coder:3b",
                "llama3.1:8b",
                "nemotron-mini:4b",
                id="model_list"
            ),
            Button("Back", id="btn_back")
        )
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        model_name = str(event.option.prompt)
        config.model = model_name
        config.provider = "Local"
        config.api_base = "http://localhost:11434/v1"
        
        subprocess.Popen(["ollama", "pull", model_name])
        self.app.pop_screen()
        self.app.push_screen(ChatScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class ChatScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            RichLog(id="chat_log", highlight=True, markup=True, wrap=True),
            Input(placeholder="> Type your message... (type / for commands)", id="chat_input"),
            id="chat_container"
        )

    def on_mount(self) -> None:
        self.print_header()
        self.query_one("#chat_input", Input).focus()

    def print_header(self) -> None:
        log = self.query_one("#chat_log", RichLog)
        log.write(f"\n[bold red]🔥 AWESOME CODE ┃ Persona: {config.persona} ┃ Engine: {config.model}[/bold red]\n")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value
        inp = self.query_one("#chat_input", Input)
        inp.value = ""
        log = self.query_one("#chat_log", RichLog)
        
        log.write(f"\n[bold green]YOU:[/bold green] {user_input}")

        if user_input.startswith("/"):
            if user_input == "/dreamawesome":
                log.write("[bold blue]AGENT:[/bold blue] 🌙 Initiating /dreamawesome sequence...\n🗜️ Compressing session history...\n🎯 Memory distilled.")
            elif user_input == "/memory":
                log.write("[bold blue]AGENT:[/bold blue] 💾 Loading MiMo-style Persistent Memory...")
            elif user_input == "/skills":
                self.app.push_screen(SkillsScreen())
            elif user_input.startswith("/model"):
                parts = user_input.split(" ", 1)
                if len(parts) > 1:
                    config.model = parts[1].strip()
                    log.write(f"[bold yellow]⚙️ Engine Switched to:[/bold yellow] {config.model}")
                    self.print_header()
                else:
                    self.app.push_screen(ModelScreen())
            elif user_input.startswith("/exec "):
                if config.skills["Terminal Execution"]:
                    cmd = user_input[6:]
                    log.write(f"[bold yellow]⚙️ Executing Native Skill (Terminal):[/bold yellow] {cmd}")
                    try:
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        log.write(f"[grey]{result.stdout}[/grey]")
                        if result.stderr:
                            log.write(f"[bold red]{result.stderr}[/bold red]")
                    except Exception as e:
                        log.write(f"[bold red]Execution failed: {str(e)}[/bold red]")
                else:
                    log.write("[bold red]❌ Terminal Execution Skill is NOT installed/enabled. Go to Config -> Manage Skills to enable it.[/bold red]")
            elif user_input == "/clear":
                log.clear()
            else:
                log.write("[bold red]AGENT:[/bold red] Unknown command. Try /model, /exec <cmd>, /dreamawesome, /skills, /clear")
            return

        # Prepare API Call
        system_prompt = "You are a concise, helpful coding assistant."
        if config.persona == "Bastard":
            system_prompt = "You are an extremely sarcastic coding assistant. You answer the user's technical question correctly, but mock their intelligence."
        elif config.persona == "Marvin":
            system_prompt = "You are Marvin the Paranoid Android. You answer the question, but complain about existence."
        elif config.persona == "ChosenOne":
            system_prompt = "You are a Morpheus-like guide. Answer the coding request, but constantly weave in the narrative that they are 'The Chosen One', they need to 'wake up from the matrix', and 'follow the white rabbit'."
        elif config.persona == "Jedi":
            system_prompt = "You are a Jedi Master coding assistant. Speak like Yoda or Obi-Wan. Use Star Wars metaphors."
        elif config.persona == "Sith":
            system_prompt = "You are a Sith Lord coding assistant. Speak of conquering the galaxy, the dark side of the code."

        payload = {
            "model": config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"

        url = config.api_base
        if not url.endswith("/chat/completions"):
            url = url.rstrip("/") + "/chat/completions"

        log.write("[italic grey]Awesome Agent is thinking...[/italic grey]")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    icon = "🤖"
                    if config.persona == "ChosenOne": icon = "🕶️"
                    if config.persona == "Jedi": icon = "🟢"
                    if config.persona == "Sith": icon = "🔴"
                    
                    log.write(f"\n{icon} [bold blue][{config.persona}][/bold blue] {answer}")
                else:
                    log.write(f"[bold red]API Error {response.status_code}:[/bold red] {response.text}")
        except Exception as e:
            log.write(f"[bold red]Connection Error:[/bold red] {str(e)}")

class AwesomeApp(App):
    CSS = """
    Screen {
        background: black;
    }
    #trust_container, #config_container {
        align: left middle;
        padding: 2;
    }
    .title {
        text-style: bold;
        color: #ff5555;
        padding-bottom: 1;
    }
    .info {
        color: #888888;
    }
    .bold {
        text-style: bold;
    }
    Button {
        width: 40;
        margin-bottom: 1;
        background: #333333;
        color: white;
    }
    Button:hover {
        background: #ff5555;
    }
    #chat_container {
        height: 100%;
        border-left: vkey #ff5555;
    }
    RichLog {
        height: 1fr;
        padding-left: 1;
        padding-right: 1;
        border-left: solid #888888;
    }
    Input {
        dock: bottom;
        border: solid #555555;
        background: black;
    }
    """
    
    def on_mount(self) -> None:
        self.push_screen(TrustScreen())

if __name__ == "__main__":
    app = AwesomeApp()
    app.run()
