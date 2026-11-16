PYTHON ?= python3

.PHONY: test test-full

test:
	$(PYTHON) -m unittest discover -s tests -v

test-full:
	TOUCH_REMOTE_FULL_BUILD=1 $(MAKE) test
