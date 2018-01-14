# Package name
PACKAGE_NAME:=serverhud

# Read the version from the file `version`
PACKAGE_VERSION:=$(shell cat version)

# Package platform
PACKAGE_PLATFORM:=py3-none-any

# Package file name
PACKAGE_FILE:=dist/$(PACKAGE_NAME)-$(PACKAGE_VERSION)-$(PACKAGE_PLATFORM).whl

# Source files that the package depends on
SRC:=Makefile setup.py version MANIFEST.in $(wildcard serverhud/ws/*) \
	$(wildcard scripts/*)

# Build all rule, only builds the package
all: $(PACKAGE_FILE) version.yml

# Actual rule that builds a new package.
$(PACKAGE_FILE): $(SRC)
		rm -rf build
		python3 setup.py sdist bdist_wheel

# Put version information in a YAML file for Ansible.
version.yml: version
		echo 'serverhud_version: "$(PACKAGE_VERSION)"' > version.yml
		echo 'serverhud_arch: "$(PACKAGE_PLATFORM)"' >> version.yml
