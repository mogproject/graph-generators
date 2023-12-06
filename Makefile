RM = /bin/rm
MV = /bin/mv
CP = /bin/cp
PYTHON=python3
MKDIR=mkdir

SRC_PY=src/main/python
TEST_PY=src/test/python
STUB_PY=src/stubs

PYTEST_OPTS=""  # --full-trace

export PYTHONPATH=$(PWD)/$(SRC_PY)
export MYPYPATH=$(PWD)/$(STUB_PY)


test: test-py

test-py:
	mypy "$(SRC_PY)"
	$(PYTHON) -m pytest -x $(PYTEST_OPTS) $(TEST_PY)

lab:
	jupyter-lab

.PHONY: test test-py lab
