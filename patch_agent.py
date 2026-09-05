import sys

with open("main.py", "r") as f:
    lines = f.readlines()

new_logic = """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        tools = []
        if config.skills.get("Terminal Execution"):
            tools.append({
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Execute a bash command on the local system",
                    "parameters": {
                        "type": "object",
                        "properties": {"command": {"type": "string"}},
                        "required": ["command"]
                    }
                }
            })
        if config.skills.get("File System Operations"):
            tools.append({
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            })
            tools.append({
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write contents to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                        "required": ["path", "content"]
                    }
                }
            })

        log.write("[italic grey]Awesome Agent is thinking...[/italic grey]")

        async def agent_loop():
            import json, subprocess, asyncio
            MAX_STEPS = 10
            
            headers = {"Content-Type": "application/json"}
            if config.api_key:
                headers["Authorization"] = f"Bearer {config.api_key}"
            url = config.api_base
            if not url.endswith("/chat/completions"):
                url = url.rstrip("/") + "/chat/completions"

            async with httpx.AsyncClient(timeout=60.0) as client:
                for step in range(MAX_STEPS):
                    payload = {
                        "model": config.model,
                        "messages": messages
                    }
                    if tools:
                        payload["tools"] = tools

                    try:
                        r = await client.post(url, json=payload, headers=headers)
                        
                        if r.status_code != 200:
                            log.write(f"\\n[bold red]API Error {r.status_code}:[/bold red] {r.text}")
                            return
                        
                        data = r.json()
                        message = data["choices"][0]["message"]
                        messages.append(message)
                        
                        if message.get("content"):
                            icon = "🤖"
                            if config.persona == "ChosenOne": icon = "🕶️"
                            if config.persona == "Jedi": icon = "🟢"
                            if config.persona == "Sith": icon = "🔴"
                            log.write(f"\\n{icon} [bold blue][{config.persona}][/bold blue] {message['content']}")
                        
                        if not message.get("tool_calls"):
                            break # Done!
                        
                        for tool_call in message["tool_calls"]:
                            fn_name = tool_call["function"]["name"]
                            args = json.loads(tool_call["function"]["arguments"])
                            log.write(f"\\n[bold yellow]⚙️ Executing Tool:[/bold yellow] {fn_name}({args})")
                            
                            result = ""
                            if fn_name == "run_command":
                                try:
                                    res = subprocess.run(args["command"], shell=True, capture_output=True, text=True)
                                    result = res.stdout + res.stderr
                                except Exception as e:
                                    result = str(e)
                            elif fn_name == "read_file":
                                try:
                                    with open(args["path"], "r") as f:
                                        result = f.read()
                                except Exception as e:
                                    result = str(e)
                            elif fn_name == "write_file":
                                try:
                                    with open(args["path"], "w") as f:
                                        f.write(args["content"])
                                    result = "File written successfully."
                                except Exception as e:
                                    result = str(e)
                            
                            log.write(f"\\n[dim]Result: {result[:200]}...[/dim]")
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "name": fn_name,
                                "content": result
                            })
                    except Exception as e:
                        log.write(f"\\n[bold red]Connection Error:[/bold red] {e}")
                        return

        import asyncio
        asyncio.create_task(agent_loop())
"""

del lines[353:390]
lines.insert(353, new_logic)

with open("main.py", "w") as f:
    f.writelines(lines)
