# LM Studio Automation

![LM Studio Icon](assets/img/lm-studio-64x64.png)

Automation scripts for LM Studio – a powerful desktop and server application for running Large Language Models locally on consumer hardware.

## Features

- **Daemon Automation** (`lmstudio_autostart.sh`): Automatically start the LM Studio daemon, wait for API availability, and optionally load models
- **System Tray Monitor** (`lmstudio_tray.py`): GTK3 system tray integration for real-time model status monitoring and quick daemon management
- **GUI Integration**: Support for launching the LM Studio desktop GUI while managing daemon lifecycle
- **Flexible Model Management**: Interactive model selection, automatic model loading, and status tracking

## Quick Start

```bash
# Start daemon with default settings
./lmstudio_autostart.sh

# Start daemon and load a specific model
./lmstudio_autostart.sh --model qwen2.5:7b-instruct

# Launch GUI (stops daemon first)
./lmstudio_autostart.sh --gui

# Interactive model selection
./lmstudio_autostart.sh --list-models

# Debug mode with verbose output
./lmstudio_autostart.sh --debug
```

## Documentation

For detailed documentation, usage examples, and flow diagrams, see the [comprehensive documentation](docs/index.html).

## Requirements

- **LM Studio Daemon** (llmster v0.0.3+): Headless backend for model inference
- **Python 3** with PyGObject (for GTK3 system tray)
- **Bash 5+** for automation scripts
- Linux system with GNOME/GTK3 support (Pop!_OS, Ubuntu, Fedora, etc.)

## Official Resources

- [LM Studio Blog](https://lmstudio.ai/blog) – Latest updates and announcements
- [LM Studio Documentation](https://lmstudio.ai/docs/app) – Complete API and feature documentation
- [LM Studio Download](https://lmstudio.ai/download) – Get the latest version

## License

[Check repository for license information]

---

**Note:** These automation scripts are designed for the daemon workflow. Make sure the LM Studio daemon is properly installed and the `lms` CLI is available in your PATH.
