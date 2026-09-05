import sys

with open("main.py", "r") as f:
    content = f.read()

# Replace ChatScreen compose
old_compose = """    def compose(self) -> ComposeResult:
        yield Vertical(
            RichLog(id="chat_log", highlight=True, markup=True, wrap=True),
            Input(placeholder="> Type your message... (type / for commands)", id="chat_input"),
            id="chat_container"
        )"""

new_compose = """    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                RichLog(id="chat_log", highlight=True, markup=True, wrap=True),
                Input(placeholder="> Type your message... (type / for commands)", id="chat_input"),
                id="chat_container"
            ),
            Vertical(
                Label("🌐 Chrome Preview (Terminal)", classes="title"),
                RichLog(id="preview_log", wrap=True),
                id="preview_sidebar"
            )
        )"""
content = content.replace(old_compose, new_compose)

# Update CSS
old_css = """    #chat_container {
        height: 100%;
        border-left: vkey #ff5555;
    }"""
new_css = """    #chat_container {
        height: 100%;
        width: 1fr;
        border-left: vkey #ff5555;
    }
    #preview_sidebar {
        width: 40%;
        height: 100%;
        border-left: solid #ff5555;
        display: none;
        padding: 1;
    }"""
content = content.replace(old_css, new_css)

# Update commands
old_cmd = """            elif user_input == "/clear":
                log.clear()"""
new_cmd = """            elif user_input.startswith("/preview"):
                sidebar = self.query_one("#preview_sidebar", Vertical)
                sidebar.display = not sidebar.display
                log.write("[bold yellow]⚙️ Toggled Chrome Preview Sidebar[/bold yellow]")
            elif user_input.startswith("/fetch "):
                url = user_input[7:].strip()
                if not url.startswith("http"): url = "http://" + url
                sidebar = self.query_one("#preview_sidebar", Vertical)
                sidebar.display = True
                plog = self.query_one("#preview_log", RichLog)
                plog.clear()
                plog.write(f"[bold cyan]Fetching {url}...[/bold cyan]")
                try:
                    r = httpx.get(url, timeout=5)
                    plog.write(f"[bold green]Status: {r.status_code}[/bold green]\n")
                    plog.write(r.text[:3000])
                except Exception as e:
                    plog.write(f"[bold red]Error loading page: {e}[/bold red]")
            elif user_input == "/clear":
                log.clear()"""
content = content.replace(old_cmd, new_cmd)

# Add File System to skills
content = content.replace('"GitHub Repo Search": False', '"GitHub Repo Search": False,\n            "File System Operations": True')
content = content.replace('f"[ {\'X\' if config.skills[\'GitHub Repo Search\'] else \' \'} ] GitHub Repo Search (Ponytail)"', 'f"[ {\'X\' if config.skills[\'GitHub Repo Search\'] else \' \'} ] GitHub Repo Search (Ponytail)",\n                f"[ {\'X\' if config.skills[\'File System Operations\'] else \' \'} ] File System Operations"')

with open("main.py", "w") as f:
    f.write(content)
