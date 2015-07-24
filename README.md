# git-abireport
An ABI/API compliance checker for git repositories.

The goal of this project is to make it as easy as possible to check 
new upstream versions of shared libraries against ABI/API breaks.

The user should only provide a GIT url and optionally a list of tags, which
should be checked (semantic versioning required).

The tool than automatically tries to build the software and checks the API/ABI
using the [ABI-compliance-checker](http://ispras.linuxbase.org/index.php/ABI_compliance_checker).

The result should be presented in browsable HTML files.

# Specification
Each project needs a specification about where the sources can be found, which tags should be checked and how the binaries are built.

The specification is expressed in YAML.

```yaml
---
url: https://github.com/open-source-parsers/jsoncpp.git
branches: 
    - master
    - develop
recipes: 
    - tag: 0.1.*
      libraries: 
        - libjsoncpp.so.*
      script: |
        mkdir build
        cd build
        cmake -DJSONCPP_LIB_BUILD_SHARED=ON -DCMAKE_BUILD_TYPE=Debug ..
        make

    - tag: 1.0.*
      libraries:
        - libjsoncpp.so.*
      script: |
        scons platform=gcc
        make

```

# Implementation
The implementation will probably be in python.

# Dependencies

```sh
sudo apt-get install git abi-compliance-checker
```
