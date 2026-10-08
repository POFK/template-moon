### first run after initialization

```
uv sync --all-groups
uv run detect-secrets scan > .secrets.baseline

git add .
prek run --all-files
```

### 构建 (Build)

#### 纯 Python 模式（默认）

所有 `.py` 源文件直接打包进 wheel，无需 C 编译器：

```bash
uv build
```

#### Cython 编译模式

将 `pyproject.toml` 中 `cython_modules_path` 指定的模块编译为 `.so` 文件，
源码不进入 wheel，从而保护核心算法的源代码。需要系统安装 C 编译器（gcc/clang）。

```bash
BUILD_MODE=cython uv build
```

构建后自动执行 `strip`（移除调试符号）和 `UPX`（压缩），如果工具未安装则跳过并警告。

#### 配置说明

在 `pyproject.toml` 的 `[tool.builder-opt]` 中配置：

```toml
[tool.builder-opt]
# 这些目录下的非 __init__.py 文件在 Cython 模式下编译为 .so
cython_modules_path = [
    "src/{{name}}/utils",
    "src/{{name}}/cli",
]
# 即使在上面的目录中，这些文件也不编译（保留为 .py）
exclude_from_cython = []
# 这些文件任何模式下都不打包进 wheel
exclude_from_package = []
```

| 配置项 | 作用 |
|--------|------|
| `cython_modules_path` | 指定哪些目录的代码需要编译保护 |
| `exclude_from_cython` | 白名单豁免：某些文件不需要保护，保留为可读的 .py |
| `exclude_from_package` | 黑名单：内部调试工具等不应出现在发布版中的文件 |

### 使用内网 PyPI 镜像

如果你在内网环境，需要更快的包下载速度，可以在 `pyproject.toml` 中添加自定义 index：

```toml
[[tool.uv.index]]
name = "ustc-mirror"
url = "https://mirrors.ustc.edu.cn/pypi/simple"
default = true
```

或者在 `uv.toml` / 环境变量中配置：

```bash
export UV_DEFAULT_INDEX="https://mirrors.ustc.edu.cn/pypi/simple"
```
