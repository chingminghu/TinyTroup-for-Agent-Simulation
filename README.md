# TinyTroupe Research Extensions

This repository is our laboratory fork of TinyTroupe. It contains extensions
used in our experiments and may include additional experimental features in the
future.

## API provider support

TinyTroupe selects its model provider through `API_TYPE` in the `[OpenAI]`
section of `config.ini`. This fork supports OpenAI, Azure OpenAI, Gemini,
OpenRouter, and Ollama.

| Provider | `API_TYPE` | Required credential | Model-name format |
| --- | --- | --- | --- |
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-...` |
| Azure OpenAI | `azure` | `AZURE_OPENAI_KEY` and `AZURE_OPENAI_ENDPOINT` | Azure deployment name |
| Gemini API | `gemini` | `GEMINI_API_KEY` | `gemini-...` |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | `provider/model` |
| Ollama | `ollama` | None for a local server | Ollama model tag |

### General usage

Create `config.ini` in the directory from which you start Python. TinyTroupe
first loads its bundled defaults and then overrides them with values from this
file. Keep credentials in environment variables rather than writing them into
`config.ini`.

The main model settings are:

- `MODEL`: normal agent responses.
- `REASONING_MODEL`: operations that request a reasoning model.
- `EMBEDDING_MODEL`: semantic memory and retrieval.

After changing providers, restart the Python process or notebook kernel because
TinyTroupe loads and caches its configuration during import.

### OpenAI

Set the API key:

```bash
export OPENAI_API_KEY="your-key"
```

Example `config.ini`:

```ini
[OpenAI]
API_TYPE=openai
MODEL=gpt-5-mini
REASONING_MODEL=o3-mini
EMBEDDING_MODEL=text-embedding-3-small
```

### Azure OpenAI

Set the Azure resource endpoint and API key:

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_KEY="your-key"
```

If `AZURE_OPENAI_KEY` is not set, TinyTroupe attempts Microsoft Entra ID
authentication through `DefaultAzureCredential`.

Azure model settings are deployment names, which may differ from the underlying
model IDs:

```ini
[OpenAI]
API_TYPE=azure
AZURE_API_VERSION=2024-12-01-preview
MODEL=your-chat-deployment
REASONING_MODEL=your-reasoning-deployment
EMBEDDING_MODEL=your-embedding-deployment
AZURE_EMBEDDING_MODEL_API_VERSION=2023-05-15
```

Use API versions supported by your Azure resource and deployments.

### Gemini API

Set the Gemini API key:

```bash
export GEMINI_API_KEY="your-key"
```

Use Gemini's native model IDs without an OpenRouter-style `google/` prefix:

```ini
[OpenAI]
API_TYPE=gemini
MODEL=your-gemini-chat-model
REASONING_MODEL=your-gemini-reasoning-model
EMBEDDING_MODEL=gemini-embedding-001
```

Gemini uses Google's OpenAI-compatible endpoint. If you change the embedding
model, rebuild existing vector indexes because vectors produced by different
embedding models are not interchangeable.

### OpenRouter

Set the OpenRouter API key:

```bash
export OPENROUTER_API_KEY="your-key"
```

OpenRouter model IDs include the provider prefix:

```ini
[OpenAI]
API_TYPE=openrouter
MODEL=provider/your-chat-model
REASONING_MODEL=provider/your-reasoning-model
EMBEDDING_MODEL=openai/text-embedding-3-small
```

Select `EMBEDDING_MODEL` from OpenRouter's embedding catalog. A chat model
cannot be used for embeddings unless it explicitly supports the embeddings
endpoint.

### Ollama

Ollama support is experimental. Pull a model and start the local server:

```bash
ollama pull gemma3:1b
ollama serve
```

Configure its local OpenAI-compatible endpoint:

```ini
[OpenAI]
API_TYPE=ollama
BASE_URL=http://localhost:11434/v1
MODEL=gemma3:1b
```

The current Ollama client switches chat generation only. Features that require
embeddings still need a separately supported embedding setup.

## Example workflow

1. Export the credential for the selected provider.
2. Copy the corresponding example above into a `config.ini` file in the
   directory where Python or Jupyter will be started.
3. Replace the example model names with models or deployments available from
   that provider.
4. Start Python or restart the notebook kernel.
5. Run a TinyTroupe interaction, for example:

```python
from tinytroupe.factory import TinyPersonFactory

factory = TinyPersonFactory(
    context="A research laboratory studying human decision-making."
)
participant = factory.generate_person(
    "A graduate student who is careful, curious, and analytical."
)
participant.listen_and_act(
    "Describe the factors you would consider before joining an experiment."
)
```

When switching embedding models, rebuild stored vector indexes. Do not reuse
vectors created by a different embedding model, even when their dimensions are
the same.

For more details, see [Switching API Providers](./docs/guides/api-providers.md)
and the experimental [Ollama guide](./docs/guides/ollama.md).
