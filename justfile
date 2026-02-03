template_locator := "generator:\n  templates:\n    - 'git://github.com/POFK/template-moon#master'"

default:
    @just --list

# add generator from git://github.com/POFK/template-moon#master
init_generator:
    echo "add templates locator..."
    echo "{{template_locator}}" >> .moon/workspace.yml

# init moon repo and add generator from git://github.com/POFK/template-moon#master
init:
    moon init --yes
    @init_generator
