### first run after initialization

```
uv sync --all-groups
uv run detect-secrets scan > .secrets.baseline

git add .
uv run pre-commit run -a
```

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
