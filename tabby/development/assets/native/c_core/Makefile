# Builds and runs the tests under AddressSanitizer and UBSan, with warnings as errors.
CFLAGS ?= -std=c11 -O1 -g -Wall -Wextra -Werror -fsanitize=address,undefined -fno-omit-frame-pointer

test: test_core
	./test_core

test_core: core.c test_core.c core.h
	$(CC) $(CFLAGS) core.c test_core.c -o $@

clean:
	rm -f test_core
.PHONY: test clean
