# CodePilot CLI

[![CI](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ci.yml)
[![CD](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/cd.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/cd.yml)
[![Code Format](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/black.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/black.yml)
[![Linter](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ruff.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ruff.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/code-pilot-cli?logo=python&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - License](https://img.shields.io/pypi/l/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)

## Introduction

The **CodePilot CLI** is a sophisticated command-line interface designed to empower developers by streamlining and automating essential coding tasks. Leveraging state-of-the-art AI models, CodePilot offers a comprehensive suite of features aimed at enhancing code quality, generating documentation, writing tests, conducting code reviews, and identifying security vulnerabilities.

## Key Features

- **Streamlined Development**: Automate repetitive tasks to focus on more strategic work.
- **Code Quality Enhancement**: Receive suggestions for code improvements and best practices.
- **Documentation Generation**: Quickly generate comprehensive and accurate documentation.
- **Automated Testing**: Save time by creating test cases with minimal effort.
- **Security Scanning**: Detect potential vulnerabilities in your codebase.
- **Real-time Chat**: Engage in real-time discussions with CodePilot for instant assistance.

## Demonstration

To gain a deeper understanding of CodePilot CLI's capabilities, we invite you to watch our [interactive demonstration video](https://youtu.be/XdwqzXIJ_qc) on YouTube.

[![Interactive Demonstration of CodePilot CLI](https://img.youtube.com/vi/XdwqzXIJ_qc/maxresdefault.jpg)](https://youtu.be/XdwqzXIJ_qc)

## Installation

Installing the CodePilot CLI is straightforward. Use the following `pip` command to install the tool:

```bash
pip install code-pilot-cli
```

### Environment Configuration

To authenticate and utilize the CLI effectively, set your Hugging Face token as an environment variable. You can obtain your token from [Hugging Face](https://huggingface.co/settings/tokens).

#### Bash

```bash
export HF_TOKEN=hf_**********************************
```

#### PowerShell

```powershell
$env:HF_TOKEN = "hf_**********************************"
```

## Usage

### Command Structure

```bash
code-pilot [OPTIONS] COMMAND [ARGS]...
```

### Available Commands

- **`ai`**: Interact with CodePilot using natural language prompts.
- **`chat`**: Engage in a real-time chat session with CodePilot.
- **`completions`**: Generate code completions from provided snippets.
- **`document`**: Automatically generate comprehensive documentation for code.
- **`enhance`**: Improve code quality by aligning it with best practices.
- **`review`**: Perform detailed code reviews to identify areas for enhancement.
- **`scan`**: Detect security vulnerabilities within your code.
- **`test`**: Automatically generate tests for your code.

### Command Details

#### `code-pilot ai`

Interact with CodePilot using natural language prompts.

**Usage:**

```bash
code-pilot ai "Build an Expo to-do app using TypeScript and expo-router" -o response.md
```

**Options:**

- `-c, --code FILENAME`: Include a code file in your prompt.
- `-o, --output FILENAME`: Save the response to a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

#### `code-pilot chat`

Initiate a chat session with CodePilot to receive real-time assistance.

**Usage:**

```bash
code-pilot chat -e chat_history.json -h chat_history.json
```

**Options:**

- `-e, --export FILENAME`: Export chat history to a file.
- `-h, --history FILENAME`: Import chat history from a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

#### `code-pilot completions`

Generate code completions from code snippets.

**Usage:**

```bash
code-pilot completions "fn say_hello(name: String) -> String:" -l rust -o code-completions.md
```

**Options:**

- `-c, --code TEXT`: Provide a code snippet.
- `-f, --file FILENAME`: Read code from a file.
- `-l, --lang TEXT`: Specify the programming language.
- `-o, --output FILENAME`: Save the response to a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

#### `code-pilot document`

Generate documentation for specified code files.

**Usage:**

```bash
code-pilot document src/lib.rs -o code-docs.md
```

**Options:**

- `-o, --output FILENAME`: Save the documentation to a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

#### `code-pilot enhance`

Improve code quality by applying best practices.

**Usage:**

```bash
code-pilot enhance app/models.py -m meta-llama/Llama-3.2-3B-Instruct -o enhancements.md
```

**Options:**

- `-o, --output FILENAME`: Save the improvements to a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

#### `code-pilot review`

Conduct a thorough code review to identify areas for improvement.

**Usage:**

```bash
code-pilot review code.py -m meta-llama/Llama-3.2-3B-Instruct -o code-review.md
```

**Options:**

- `-o, --output FILENAME`: Save the review to a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

#### `code-pilot scan`

Identify security vulnerabilities present in your code.

**Usage:**

```bash
code-pilot scan src/main.rs -m meta-llama/Llama-3.2-3B-Instruct -o code-scan.md
```

**Options:**

- `-o, --output FILENAME`: Save the results to a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

#### `code-pilot test`

Automatically generate tests for your code.

**Usage:**

```bash
code-pilot test App.tsx -m meta-llama/Llama-3.2-3B-Instruct
```

**Options:**

- `-o, --output FILENAME`: Save the generated tests to a file.
- `-m, --model TEXT`: Specify the AI model to use.
- `-t, --max-tokens INTEGER`: Set the maximum number of tokens in the response.

## Contribution Guide

We welcome contributions to the CodePilot CLI project. To get started, please refer to the [Contribution Guide](CONTRIBUTING.md).

## Support and Feedback

If you encounter any issues or have suggestions for improvements, please don't hesitate to reach out to us via our [GitHub Issues](https://github.com/youzarsiph/code-pilot-cli/issues).

## License

The CodePilot CLI is distributed under the [MIT License](LICENSE).
