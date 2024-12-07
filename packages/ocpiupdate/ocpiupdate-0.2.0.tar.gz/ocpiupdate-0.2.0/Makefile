at = @
makefile_directory := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: help
help:
	@echo "Usage:"
	@echo "  build"
	@echo "  clean"
	@echo "  clean-dist"
	@echo "  publish-current"

.PHONY: build
build:
	$(at)uv --directory $(makefile_directory) sync \
		&& uv --directory $(makefile_directory) lock \
		&& uv --directory $(makefile_directory) build

.PHONY: clean-dist
clean-dist:
	$(at)rm -rf $(makefile_directory)/dist/

.PHONY: clean
clean: clean-dist
	$(at)rm -rf $(makefile_directory)/src/ocpiupdate/__pycache__
	$(at)rm -rf $(makefile_directory)/src/ocpiupdate.egg-info
	$(at)rm -f $(makefile_directory)/uv.lock

.PHONY: publish-current
publish-current: clean build
	$(at)uv --directory $(makefile_directory) publish
