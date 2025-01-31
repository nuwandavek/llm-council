# llm-council

Get a council of LLMs to advise consult for you!

## Installation

This plugin should be installed in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-council
```

![council](assets/council.png)
## Usage

I usually run every query on all LLMs just to see what they have to say. And I love the llm library. You can now assemble your own council of advisors by simply running `llm council` like this:

```bash
llm council 'whats the california traffic law around double white lines?'
```

By default, it uses `openai` and `anthropic`. But you can specify the providers by:

```bash
llm council -p openai -p anthropic 'tell me a joke'
```
The models themselves are fixed as of now with:
- openai: gpt-4o
- anthropic: clause-3-5-sonnet-latest

Press Q or Ctrl + C to exit.

## The system prompt

This is the prompt used by this tool:

> Keep your answers brief and to the point.

Feel free to modify it by passing the `--system` arg.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-council
uv venv
source .venv/bin/activate

uv pip install -r pyproject.toml
```
Now install the plugin with:
```bash
llm install -e .
```
