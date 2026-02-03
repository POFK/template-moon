
### init a new monorepo

```bash
nix develop github:POFK/template-moon
# or
nix develop github:POFK/template-moon#fhs
```

```bash
moon init --yes
```

```bash
moon toolchain add unstable_python
moon toolchain add unstable_uv
```

### using template

edit the `.moon/workspace.yml`
```
generator:
  templates:
    - 'git://github.com/POFK/template-moon#master'
```

#### add a python package

```bash
moon generate python
```

It will create a new package directory at packages/[name]
