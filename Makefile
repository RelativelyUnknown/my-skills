# Checks for this repository. `make check` is free (no model calls) and is the pre-commit gate from HANDOVER.md.
# Needs python3 and node; the C core test needs a C compiler; `validate` needs the `claude` CLI.
.PHONY: check links descriptions selftests c-core validate eval

check: links descriptions selftests c-core

links:
	python3 tools/linkcheck.py

descriptions:
	python3 tools/descriptions.py

selftests:
	python3 tools/eval/smellcheck.py --selftest
	python3 tabby-diagrams/assets/diagram/selftest.py
	node tabby-diagrams/assets/animation/selftest-motion.mjs
	node tabby-frontend/assets/interfaces/selftest-ui.mjs

c-core:
	$(MAKE) -C tabby/development/assets/native/c_core test
	$(MAKE) -C tabby/development/assets/native/c_core clean

# `claude plugin validate .` prints an expected ICON_MISSING warning.
validate:
	claude plugin validate .

# Costs money: make eval OUT=/tmp/run CASES=a,b[,c]. Runs a copy so edits cannot disturb the run.
# Keep CASES to about five per call where this runs inside a ten-minute tool limit.
eval:
	@test -n "$(OUT)" -a -n "$(CASES)" || { echo "usage: make eval OUT=dir CASES=a,b"; exit 2; }
	P=$$(mktemp -d) && mkdir $$P/plugin && tar --exclude=.git -cf - . | tar -xf - -C $$P/plugin && \
	mkdir -p $(OUT) && cd $$P/plugin && \
	python3 tools/eval/run.py --out $(OUT) --cases $(CASES) --plugin $$PWD --plugin-dir $$PWD \
	  --model claude-haiku-5-5 --runs 3 --batch 2 --jobs 2 --keep-temp
