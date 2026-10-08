
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

### without nix

Install [moon](https://github.com/moonrepo/moon) (official install script or your package manager) and `just`; additionally install the toolchains for the languages you use (`go`, `uv`, `buf` + `protoc-gen-go*`).

Then run what `just init` does:

```bash
moon init --yes
printf "generator:\n  templates:\n    - 'git://github.com/POFK/template-moon#master'\n" >> .moon/workspace.yml
```

Everything else (`moon generate python`, …) works exactly as above.
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

### golang

#### enable gowork

```bash
go work init
```
