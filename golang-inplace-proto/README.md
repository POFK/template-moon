# {{name}}

Go project with integrated buf protobuf toolchain for in-place proto code generation.

## Quick Start

### 1. Install buf

```bash
# macOS
brew install bufbuild/buf/buf

# Linux
curl -sSL "https://github.com/bufbuild/buf/releases/latest/download/buf-$(uname -s)-$(uname -m)" -o "$HOME/bin/buf" && chmod +x "$HOME/bin/buf"
```

### 2. Install Proto Generation Tools

```bash
# Install all required protoc plugins using moon
moon run proto-install-tools
```

This installs:
- `protoc-gen-go` - Protocol Buffers Go implementation
- `protoc-gen-go-grpc` - gRPC Go plugin
- `protoc-gen-gorm` - GORM ORM plugin

### 3. Generate Proto Code

```bash
# Using buf directly
buf generate

# Or using moon task runner
moon run proto:generate
```

Generated code will be placed in `internal/gen/`

## Project Structure

```
.
├── proto/                  # Proto source files
│   ├── buf.yaml           # Proto lint/breaking config
│   └── user/
│       └── v1/
│           └── user.proto # Example proto definition
├── third_party/           # Third-party proto files
│   ├── buf.yaml
│   └── gorm/
│       ├── options.proto  # GORM ORM options
│       └── types.proto    # GORM custom types
├── internal/
│   └── gen/              # Generated code (gitignored)
│       └── user/
│           └── v1/
│               ├── user.pb.go      # Protobuf types
│               ├── user_grpc.pb.go # gRPC service client/server
│               └── user_gorm.go    # GORM ORM models
├── buf.yaml               # Root buf configuration
├── buf.gen.yaml           # Code generation plugins config
├── go.mod
└── go.sum
```

## Available Commands

### Moon Tasks

```bash
# Generate proto code
moon run proto:generate

# Install proto tools
moon run proto-install-tools

# Clean generated code
moon run proto-clean

# Run tests
moon run test

# Run tests with race detection
moon run test-race

# Run tests with coverage
moon run test-coverage

# Format code
moon run lint

# Tidy dependencies
moon run tidy

# Build
moon run build

# Build release (optimized)
moon run build-release

# Run all checks
moon run check
```

### Direct Commands

```bash
# Install tools
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
go install github.com/infobloxopen/protoc-gen-gorm@latest

# Generate code
buf generate

# Run tests
go test -v ./...

# Format
go fmt ./...

# Tidy
go mod tidy
```

## Adding New Proto Files

1. Create new `.proto` file in `proto/` directory:

```proto
// proto/user/v1/my_service.proto
syntax = "proto3";

package myservice.v1;

import "gorm/options.proto";

message MyModel {
  option (gorm.opts).ormable = true;
  string id = 1;
  string name = 2;
}

service MyService {
  rpc GetMyModel(GetMyModelRequest) returns (GetMyModelResponse);
}

message GetMyModelRequest {
  string id = 1;
}

message GetMyModelResponse {
  MyModel model = 1;
}
```

2. Generate code:

```bash
buf generate
```

3. Use generated types in your Go code:

```go
import (
    pb "git.pangu.datalab/{{user}}/{{project_name}}/{{name}}/internal/gen/user/v1"
)

func main() {
    model := &pb.MyModel{
        Id:   "123",
        Name: "Example",
    }
}
```

## Configuration

### buf.yaml

Controls linting and breaking change detection. See [Buf documentation](https://docs.buf.build/configuration/v2/buf-yaml).

### buf.gen.yaml

Configures code generation plugins. Current plugins:
- `protoc-gen-go` - Protobuf types
- `protoc-gen-go-grpc` - gRPC stubs
- `protoc-gen-gorm` - GORM models

## Requirements

- Go 1.25.0+
- buf CLI
- protoc-gen-go
- protoc-gen-go-grpc
- protoc-gen-gorm

## License

MIT
