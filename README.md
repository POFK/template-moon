
### init a new monorepo

```bash
nix develop github:POFK/template-moon
# or
nix develop github:POFK/template-moon#fhs
```

and the run

```bash
just init
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

You can use the following commands to add python related toolchains for moon@2.0.0-rc.0

```bash
moon toolchain add unstable_python
moon toolchain add unstable_uv
```

