# Promptwright - Synthetic Dataset Generation Library

[![Tests](https://github.com/StacklokLabs/promptwright/actions/workflows/test.yml/badge.svg)](https://github.com/StacklokLabs/promptwright/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/promptwright.svg)](https://pypi.org/project/promptwright/)

![promptwright-cover](https://github.com/user-attachments/assets/5e345bda-df66-474b-90e7-f488d8f89032)

Promptwright is a Python library from [Stacklok](https://stacklok.com) designed 
for generating large synthetic  datasets using a local LLM. The library offers
a flexible and easy-to-use set of interfaces, enabling users the ability to
generate prompt led synthetic datasets.

Promptwright was inspired by the [redotvideo/pluto](https://github.com/redotvideo/pluto),
in fact it started as fork, but ended up largley being a re-write, to allow
dataset generation against a local LLM model.

The library interfaces with Ollama, making it easy to just pull a model and run
Promptwright, but other providers could be used, as long as they provide a
compatible API (happy to help expand the library to support other providers,
just open an issue).

## Features

- **Local LLM Client Integration**: Interact with Ollama based models
- **Configurable Instructions and Prompts**: Define custom instructions and system prompts
- **YAML Configuration**: Define your generation tasks using YAML configuration files
- **Command Line Interface**: Run generation tasks directly from the command line
- **Push to Hugging Face**: Push the generated dataset to Hugging Face Hub with automatic dataset cards and tags
- **System Message Control**: Choose whether to include system messages in the generated dataset

## Getting Started

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- Ollama CLI installed and running (see [Ollama Installation](https://ollama.com/)
- A Model pulled via Ollama (see [Model Compatibility](#model-compatibility))
- (Optional) Hugging Face account and API token for dataset upload

### Installation

#### pip

You can install Promptwright using pip:

```bash
pip install promptwright
```

#### Development Installation

To install the prerequisites, you can use the following commands:

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install promptwright and its dependencies
git clone https://github.com/StacklokLabs/promptwright.git
cd promptwright
poetry install
```

### Usage

Promptwright offers two ways to define and run your generation tasks:

#### 1. Using YAML Configuration (Recommended)

Create a YAML file defining your generation task:

```yaml
system_prompt: "You are a helpful assistant. You provide clear and concise answers to user questions."

topic_tree:
  args:
    root_prompt: "Capital Cities of the World."
    model_system_prompt: "<system_prompt_placeholder>"
    tree_degree: 3
    tree_depth: 2
    temperature: 0.7
    model_name: "ollama/mistral:latest"
  save_as: "basic_prompt_topictree.jsonl"

data_engine:
  args:
    instructions: "Please provide training examples with questions about capital cities."
    system_prompt: "<system_prompt_placeholder>"
    model_name: "ollama/mistral:latest"
    temperature: 0.9
    max_retries: 2

dataset:
  creation:
    num_steps: 5
    batch_size: 1
    model_name: "ollama/mistral:latest"
    sys_msg: true  # Include system message in dataset (default: true)
  save_as: "basic_prompt_dataset.jsonl"

# Optional Hugging Face Hub configuration
huggingface:
  # Repository in format "username/dataset-name"
  repository: "your-username/your-dataset-name"
  # Token can also be provided via HF_TOKEN environment variable or --hf-token CLI option
  token: "your-hf-token"
  # Additional tags for the dataset (optional)
  # "promptwright" and "synthetic" tags are added automatically
  tags:
    - "promptwright-generated-dataset"
    - "geography"
```

Run using the CLI:

```bash
promptwright start config.yaml
```

The CLI supports various options to override configuration values:

```bash
promptwright start config.yaml \
  --topic-tree-save-as output_tree.jsonl \
  --dataset-save-as output_dataset.jsonl \
  --model-name ollama/llama3 \
  --temperature 0.8 \
  --tree-degree 4 \
  --tree-depth 3 \
  --num-steps 10 \
  --batch-size 2 \
  --sys-msg true \  # Control system message inclusion (default: true)
  --hf-repo username/dataset-name \
  --hf-token your-token \
  --hf-tags tag1 --hf-tags tag2
```

#### Hugging Face Hub Integration

Promptwright supports automatic dataset upload to the Hugging Face Hub with the following features:

1. **Dataset Upload**: Upload your generated dataset directly to Hugging Face Hub
2. **Dataset Cards**: Automatically creates and updates dataset cards
3. **Automatic Tags**: Adds "promptwright" and "synthetic" tags automatically
4. **Custom Tags**: Support for additional custom tags
5. **Flexible Authentication**: HF token can be provided via:
   - CLI option: `--hf-token your-token`
   - Environment variable: `export HF_TOKEN=your-token`
   - YAML configuration: `huggingface.token`

Example using environment variable:
```bash
export HF_TOKEN=your-token
promptwright start config.yaml --hf-repo username/dataset-name
```

Or pass it in as a CLI option:
```bash
promptwright start config.yaml --hf-repo username/dataset-name --hf-token your-token
```

#### 2. Using Python Code

You can also create generation tasks programmatically using Python code. There
are several examples in the `examples` directory that demonstrate this approach.

Example Python usage:

```python
from promptwright import DataEngine, EngineArguments, TopicTree, TopicTreeArguments

tree = TopicTree(
    args=TopicTreeArguments(
        root_prompt="Creative Writing Prompts",
        model_system_prompt=system_prompt,
        tree_degree=5,
        tree_depth=4,
        temperature=0.9,
        model_name="ollama/llama3"
    )
)

engine = DataEngine(
    args=EngineArguments(
        instructions="Generate creative writing prompts and example responses.",
        system_prompt="You are a creative writing instructor providing writing prompts and example responses.",
        model_name="ollama/llama3",
        temperature=0.9,
        max_retries=2,
        sys_msg=True,  # Include system message in dataset (default: true)
    )
)
```

### Development

The project uses Poetry for dependency management. Here are some common development commands:

```bash
# Install dependencies including development dependencies
make install

# Format code
make format

# Run linting
make lint

# Run tests
make test

# Run security checks
make security

# Build the package
make build

# Run all checks and build
make all
```

### Prompt Output Examples

With sys_msg=true (default):
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are tasked with designing an immersive virtual reality experience that transports users to a fantastical world of wonder."
    },
    {
      "role": "user",
      "content": "Create a descriptive passage about a character discovering their hidden talents."
    },
    {
      "role": "assistant",
      "content": "As she stared at the canvas, Emma's fingers hovered above the paintbrushes, as if hesitant to unleash the colors that had been locked within her. The strokes began with bold abandon, swirling blues and greens merging into a mesmerizing dance of light and shadow. With each passing moment, she felt herself becoming the art – her very essence seeping onto the canvas like watercolors in a spring storm. The world around her melted away, leaving only the vibrant symphony of color and creation."
    }
  ]
}
```

With sys_msg=false:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Create a descriptive passage about a character discovering their hidden talents."
    },
    {
      "role": "assistant",
      "content": "As she stared at the canvas, Emma's fingers hovered above the paintbrushes, as if hesitant to unleash the colors that had been locked within her. The strokes began with bold abandon, swirling blues and greens merging into a mesmerizing dance of light and shadow. With each passing moment, she felt herself becoming the art – her very essence seeping onto the canvas like watercolors in a spring storm. The world around her melted away, leaving only the vibrant symphony of color and creation."
    }
  ]
}
```

## Model Compatibility

The library should work with most LLM models. It has been tested with the
following models so far:

- **Mistral**
- **LLaMA3**
- **Qwen2.5**

## Unpredictable Behavior

The library is designed to generate synthetic data based on the prompts and instructions
provided. The quality of the generated data is dependent on the quality of the prompts
and the model used. The library does not guarantee the quality of the generated data.

Large Language Models can sometimes generate unpredictable or inappropriate
content and the authors of this library are not responsible for the content
generated by the models. We recommend reviewing the generated data before using it
in any production environment.

Large Language Models also have the potential to fail to stick with the behavior
defined by the prompt around JSON formatting, and may generate invalid JSON. This
is a known issue with the underlying model and not the library. We handle these
errors by retrying the generation process and filtering out invalid JSON. The 
failure rate is low, but it can happen. We report on each failure within a final
summary.

## Contributing

If something here could be improved, please open an issue or submit a pull request.

### License

This project is licensed under the Apache 2 License. See the `LICENSE` file for more details.
