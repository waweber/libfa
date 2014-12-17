
PYVENV ?= virtualenv
VE ?= ve

PYTHON ?= $(VE)/bin/python
VE_TARGET ?= $(VE)/.ve_target
EGG_INFO_TARGET ?= $(VE)/.egg_info_target
DEVELOP_TARGET ?= $(VE)/.develop_target

.PHONY: all
all: $(DEVELOP_TARGET)

$(VE_TARGET):
	$(PYVENV) $(VE) && touch $@

$(EGG_INFO_TARGET): $(VE_TARGET) setup.py
	$(PYTHON) setup.py egg_info && touch $@

$(DEVELOP_TARGET): $(EGG_INFO_TARGET)
	$(PYTHON) setup.py develop && touch $@

.PHONY: clean
clean:
	find libfa -type f -name "*.py[co]" -delete
	find libfa -type d -name "__pycache__" -delete
	rm -rf dist build

.PHONY: distclean
distclean: clean
	rm -rf libfa.egg-info
	rm -rf $(VE)
