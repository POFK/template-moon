


nix develop /home/worker/workspace/Proj/template-moon


moon init --yes


### add python project

```bash
moon toolchain add unstable_python
moon toolchain add unstable_uv
```

```bash
mkdir -p packages/exam_py
cd packages/exam_py
uv init
```

add to .moon/workspace.yml
```
generator:
  templates:
    - 'file:///home/worker/workspace/Proj/template-moon/templates'
    - 'git://github.com/moonrepo/templates#master'
```



