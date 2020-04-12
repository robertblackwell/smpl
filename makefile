NOC_SHEBANG="--python-shebang='/usr/bin/env python'"
MYNAME="Robert Blackwell"
MYEMAIL="rob@whiteacorn.com"
PROJECT_NAME="duh"
LICENSE=MIT
PREFIX=$(HOME)/.local

# this is rag-tap collection of convenience options, without any systematic
# set for buildiing and distributing. Sorry

install:
	python setup.py install --prefix=$(PREFIX) 

clean:
	python setup.py clean
	rm -rfv ./build
	rm *whl 
	rm *.pex

push:
	git status
	git add -A
	git commit -a

_license:
	licenser -n $(MYNAME) -e $(MYEMAIL) -l "MIT" -p "duh"

bumppatch:
	bumpversion --current-version `python setup.py --version` patch

bumpminor:
	bumpversion --current-version `python setup.py --version` minor

bumpmajor:
	bumpversion --current-version `python setup.py --version` major

git_push_tags:
	git push --tags origin master

git_push: git_commit
	git push --tags origin master

git_commit:
	git add -A | true
	git commit -a | true

git_list_tags:
	git show-ref --tags -d

readme:
	pandoc --from=markdown --to=rst --output=README.rst README.md

.PHONY: dist
dist:
	rm -rfv duh.egg*
	make readme
	make git_commit
	make bumpminor
	python setup.py sdist

upload: 
	make dist
	python setup.py upload