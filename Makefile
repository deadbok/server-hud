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
all: $(PACKAGE_FILE)

# Actual rule that builds a new package.
$(PACKAGE_FILE): $(SRC)
		python3 setup.py bdist_wheel
