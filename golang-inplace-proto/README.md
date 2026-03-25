# {{name}}

Go project with integrated buf protobuf toolchain for in-place proto code generation.

## Overview

Go project with integrated buf protobuf toolchain for in-place proto code generation.

## Core Principles

### Project Development
- **TDD** — Write tests first, then implementation
- **Spec-Driven Development** — Define specs before implementation
- **Isolation** — Use git worktrees and subagents for feature isolation

### Proto & API Design
- **Single Source of Truth** — `proto/` is the authoritative source for all data structures and API definitions
- **No Duplication** — Define business structures and APIs only in proto files, never in Go code
- **Generated Code Only** — Import from `gen/`, never hand-write or modify generated files

## Project Structure

```
.
├── proto/                  # Proto source files - single source of truth for data structures and APIs
│   ├── buf.yaml           # Proto lint/breaking config
│   └── <domain>/
│       └── v1/
│           └── <domain>.proto
├── third_party/           # Third-party proto files
│   └── buf.yaml
├── internal/
│   └── gen/              # Generated code (gitignored) - import from here only
│       └── <domain>/
│           └── v1/
│               ├── *.pb.go      # Protobuf types
│               └── *_grpc.pb.go # gRPC service client/server
├── buf.yaml               # Root buf configuration
├── buf.gen.yaml           # Code generation plugins config
├── go.mod
└── go.sum
```

## Usage

### Generate Proto Code

```bash
# Using buf directly
buf generate

# Or using moon task runner
moon run proto:generate
```

### Install Proto Tools

```bash
moon run proto-install-tools
```

## Requirements

- Go 1.25.0+
- buf CLI

## License

MIT
