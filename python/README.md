
### first run after initialization

```
uv sync --all-groups
uv run detect-secrets scan > .secrets.baseline

git add .
uv run pre-commit run -a
```

