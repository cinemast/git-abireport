# git-abireport
An ABI/API compliance checker for git repositories.

The goal of this project is to make it as easy as possible to check 
new upstream versions of shared libraries against ABI/API breaks.

The user should only provide a GIT url and optionally a list of tags, which
should be checked (semantic versioning required).

The tool than automatically tries to build the software and checks the API/ABI
using the [ABI-compliance-checker](http://ispras.linuxbase.org/index.php/ABI_compliance_checker).

The result should be presented in browsable HTML files.


# Dependencies

```sh
sudo apt-get install git abi-compliance-checker
```
