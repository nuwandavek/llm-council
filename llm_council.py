from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.styles import Style

import click
import llm

style = Style.from_dict({
    "frame.border.blue": "ansiblue",
    "frame.border.red": "ansired",
    "frame.border.yellow": "ansiyellow",
})

SYSTEM_PROMPT = """
Keep your answers brief and to the point.
""".strip()

PROVIDER_MODELS = {
    "openai": {"model": "gpt-4o", "style": "class:frame.border.blue"},
    "anthropic": {"model": "claude-3.5-sonnet", "style": "class:frame.border.red"},
    "google": {"model": "gemini-1.5-flash-latest", "style": "class:frame.border.yellow"},
}


@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("args", nargs=-1)
    @click.option("-p", "--providers", multiple=True, default=['openai', 'anthropic'], help="Specify the labs in the council")
    @click.option("-s", "--system", help="Custom system prompt")
    def council(args, providers, system):
        """Generate and execute commands in your shell"""
        prompt = " ".join(args)
        for provider in providers:
            if provider not in PROVIDER_MODELS:
                click.echo(f"Unknown provider: {provider}")
                return
        responses = {}
        for provider in providers:
            model = llm.get_model(PROVIDER_MODELS[provider]["model"])
            model.key = llm.get_key('', model.needs_key, model.key_env_var)
            responses[provider] = str(model.prompt(prompt, system=system or SYSTEM_PROMPT))
        display_council(prompt, responses)


def display_council(prompt, responses):
    buffers = [Buffer(document=Document(f"Q: {prompt}\n\n\n{response}", cursor_position=0), read_only=True) for response in responses.values()]
    windows = [Frame(Window(BufferControl(buffer=buffer), wrap_lines=True, ignore_content_width=True), title=f"{provider}: {PROVIDER_MODELS[provider]['model'].replace('-latest', '')}", style=PROVIDER_MODELS[provider]["style"]) for provider, buffer in zip(responses.keys(), buffers)]
    toolbar = TextArea(text="Press TAB to switch windows | Press Q or Ctrl+C to exit", height=1, style="reverse")
    header = TextArea(text=f"llm-council | council members: {', '.join(responses.keys())}", height=1, style="reverse")

    layout = Layout(HSplit([
        header,
        TextArea(text="", height=1),
        VSplit(windows),
        TextArea(text="", height=1),
        toolbar
    ]))
    layout.focus(buffers[0])

    kb = KeyBindings()

    @kb.add("q")
    @kb.add("c-c")
    def exit_(event):
        event.app.exit()

    @kb.add("tab")
    def switch_focus(event):
        """Switch focus between the two windows."""
        current_focus = next((i for i, buf in enumerate(buffers) if event.app.layout.has_focus(buf)), 0)
        next_index = (current_focus + 1) % len(buffers)
        event.app.layout.focus(buffers[next_index])

    app = Application(layout=layout, key_bindings=kb, full_screen=True, style=style)
    app.run()
