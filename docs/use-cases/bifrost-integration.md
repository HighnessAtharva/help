---
title: AccuKnox <> Bifrost Integration
description: Guide to integrate AccuKnox LLM Defense with Bifrost using a custom Go plugin.
---

# AccuKnox <> Bifrost Integration Guide

This guide demonstrates how to integrate AccuKnox LLM Defense with Bifrost using a custom plugin written in Go.

## Step 1: Install Dependencies

### Clone the Bifrost Repository

```bash
git clone https://github.com/maximhq/bifrost.git
cd bifrost
```

### Build the Bifrost HTTP Binary

!!! note
    We are using the `bifrost-http` binary to test out the config. However, you can use this config with any Bifrost deployment method.

```bash
go build -o bifrost-http transports/bifrost-http/main.go
```

## Step 2: Create the AccuKnox Plugin

### Initialize the Plugin Directory

Create a new directory for your plugin and initialize the Go module:

```bash
mkdir accuknox-bifrost-plugin
cd accuknox-bifrost-plugin
go mod init github.com/username/bifrost-plugin
```

### Create the Main Plugin File


Create `main.go` with the plugin code. The plugin implements hooks for intercepting LLM requests and responses. Put the following code in `main.go`:

!!! tip "Plugin Implementation"
    The AccuKnox plugin integrates with Bifrost's lifecycle hooks to scan prompts and responses through the AccuKnox LLM Defense API.

<script src="https://gist.github.com/HighnessAtharva/7d0266266961f3196657de8f52b9f6b1.js"></script>

### Create the Go Module File

Create `go.mod` with the Bifrost core dependency:

```go
module github.com/accuknox/bifrost-poc

go 1.24.0

toolchain go1.24.10

require github.com/maximhq/bifrost/core v1.2.19

// Use local bifrost/core to match the bifrost-http binary
replace github.com/maximhq/bifrost/core => ./bifrost/core

require (
	github.com/bytedance/gopkg v0.1.3 // indirect
	github.com/bytedance/sonic v1.14.1 // indirect
	github.com/bytedance/sonic/loader v0.3.0 // indirect
	github.com/cloudwego/base64x v0.1.6 // indirect
	github.com/klauspost/cpuid/v2 v2.3.0 // indirect
	github.com/twitchyliquid64/golang-asm v0.15.1 // indirect
	golang.org/x/arch v0.22.0 // indirect
	golang.org/x/sys v0.37.0 // indirect
)
```

## Step 3: Build the Plugin

### Create a Makefile

Create a `Makefile` for easy building:

```makefile
.PHONY: build clean

build:
	@echo "Building AccuKnox Bifrost plugin..."
	go mod tidy
	go build -buildmode=plugin -o accuknox-plugin.so main.go
	@echo "Plugin built successfully: accuknox-plugin.so"

clean:
	rm -f accuknox-plugin.so
	go clean
```

### Build the Plugin

Build the plugin:

```bash
make build
```

This will generate `accuknox-plugin.so` file.

## Step 4: Configure Bifrostost

Create a configuration file for Bifrost with your plugin settings:

```json
{
  "log_level": "debug",
  "server": {
    "port": 8080,
    "host": "0.0.0.0"
  },
  "plugins": [
    {
      "enabled": true,
      "name": "accuknox-logger",
      "path": "./accuknox-plugin.so",
      "config": {
        "enabled": true,
        "api_key": "<YOUR_ACCUKNOX_JWT_TOKEN>",
        "user_info": "<username@accuknox.com>"
      }
    }
  ],
  "providers": {
    "openai": {
      "keys": [
        {
          "value": "<YOUR_OPENAI_API_KEY>",
          "models": ["gpt-3.5-turbo"],
          "weight": 1.0
        }
      ]
    }
  }
}
```

### Configuration Detailsils

#### Plugin Configuration

- `enabled`: Set to `true` to activate the plugin
- `name`: Plugin identifier (must match the name returned by `GetName()`)
- `path`: Path to the compiled `.so` file
- `api_key`: Your AccuKnox LLM Defense JWT token (obtained from AccuKnox dashboard)
- `user_info`: Your email or username for tracking

#### AccuKnox API Endpoint

The plugin automatically determines the AccuKnox API endpoint by decoding the JWT token's `iss` field:

- **dev**: <https://cwpp.dev.accuknox.com/llm-defence/application-query>
- **stage**: <https://cwpp.stage.accuknox.com/llm-defence/application-query>
- **demo**: <https://cwpp.demo.accuknox.com/llm-defence/application-query>
- **prod**: <https://cwpp.prod.accuknox.com/llm-defence/application-query>

#### Provider Configuration

- Add your LLM provider credentials (OpenAI, Anthropic, etc.)
- Each key can be restricted to specific models
- Use `weight` for load balancing across multiple keys

## Step 5: Run Bifrost Serverver

### Copy the Plugin

Copy the plugin to your Bifrost directory:

```bash
cp accuknox-plugin.so /path/to/bifrost/
cd /path/to/bifrost/
```

### Start the Server

Start the Bifrost HTTP server:

```bash
./bifrost-http -app-dir . -log-level debug -log-style pretty
```

!!! success "Server Running"
    The Bifrost server will now be running on port 8080 with the AccuKnox plugin active.

## Step 6: Test the Integrationion

Send a test request using curl:

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 50
  }'
```

!!! info "Expected Behavior"
    The plugin will intercept the request, scan the prompt through AccuKnox LLM Defense API, forward it to OpenAI, and then scan the response before returning it to the client. Check the server logs to see the plugin in action.
