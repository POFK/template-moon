#!/bin/bash
# Install protobuf code generation tools for Go
# Run this script before generating proto code

set -e

echo "Installing protobuf code generation tools..."

# Install protoc-gen-go
echo "Installing protoc-gen-go..."
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

# Install protoc-gen-go-grpc
echo "Installing protoc-gen-go-grpc..."
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Install protoc-gen-gorm
echo "Installing protoc-gen-gorm..."
go install github.com/infobloxopen/protoc-gen-gorm@latest

# Verify installations
echo ""
echo "Verifying installations..."

if command -v protoc-gen-go &>/dev/null; then
	echo "✓ protoc-gen-go installed successfully"
else
	echo "✗ protoc-gen-go installation failed"
	exit 1
fi

if command -v protoc-gen-go-grpc &>/dev/null; then
	echo "✓ protoc-gen-go-grpc installed successfully"
else
	echo "✗ protoc-gen-go-grpc installation failed"
	exit 1
fi

if command -v protoc-gen-gorm &>/dev/null; then
	echo "✓ protoc-gen-gorm installed successfully"
else
	echo "✗ protoc-gen-gorm installation failed"
	exit 1
fi

echo ""
echo "All protobuf tools installed successfully!"
echo "Make sure \$GOPATH/bin is in your PATH environment variable."
