# {{name}}

## 环境要求

- Go 1.25.0+
- Moonrepo 2.0.1+

## 快速开始

### 安装依赖

```bash
go mod tidy
```

### 运行测试

```bash
# 运行所有测试
moon run :test

# 运行带竞态检测的测试
moon run :test-race

# 运行测试覆盖率
moon run :test-coverage
```

### 构建

```bash
# Debug 构建
moon run :build-debug

# Release 构建（优化）
moon run :build-release
```

### 代码检查

```bash
# 格式化代码
moon run :lint

# 运行所有检查
moon run :check
```

## 项目结构

```
{{name}}/
├── go.mod
├── moon.yml
└── README.md
```

## 开发指南

### 测试驱动开发（TDD）

1. **RED**: 先编写失败的测试
2. **GREEN**: 实现最小化代码使测试通过
3. **REFACTOR**: 重构代码并验证测试仍通过

### 代码风格

```go
// 导入顺序：标准库 → 第三方 → 项目内部
import (
    "context"
    "time"

    "gorm.io/gorm"

    "github.com/google/uuid"
)

// 错误处理
if err != nil {
    return nil, fmt.Errorf("context: %w", err)
}
```
