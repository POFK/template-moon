# [name]

Basic TypeScript package template for moon monorepo.

## Requirements

Ensure `.moon/toolchains.yml` in your workspace root contains:

```yaml
javascript:
  packageManager: 'pnpm'
node: {}
pnpm: {}
```

Or add via CLI:

```bash
moon toolchain add unstable_pnpm
```

## Usage

```bash
# Generate a new package from this template
moon generate typescript
# → Package name? my-package

# Install dependencies (workspace root)
pnpm install

# Run tasks
# Run tasks (syntax: moon run <project>:<task>)
moon run my-package:typecheck
moon run my-package:lint
moon run my-package:check
moon run my-package:build
```

## Structure

- `src/` — source code
- `tests/` — vitest tests
- `tsconfig.json` — standalone TypeScript config (no root extends)
- `eslint.config.js` — ESLint flat config with typescript-eslint

## Notes

- **pnpm workspace**: 仓库根需要 `pnpm-workspace.yaml`（pnpm 不读取 package.json 的 workspaces 字段）：
  ```yaml
  packages:
    - 'packages/*'
  ```
- **跨项目引用**: 使用 `paths` + `include` 直接引用源码（如 `"@scope/shared": ["../shared/src"]`），避免 `composite`/`references` 的 build 顺序问题。
- **moon run 语法**: `moon run <project>:<task>`（如 `moon run my-package:typecheck`）
- **moon generate**: 需要交互式终端（TTY），非交互环境（CI/脚本）需手动模拟或等待 moon 版本更新。
