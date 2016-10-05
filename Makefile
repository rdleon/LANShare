CFLAGS=-O2 -std=c99 -pedantic -Wall -Wextra -Isrc -rdynamic -DNDEBUG $(OPTFLAGS)
SOURCES=src/lanshare.c

all: lanshare

dev: CFLAGS=-g -std=c99 -pedantic -Wall -Isrc -Wall -Wextra $(OPTFLAGS)
dev: all

lanshare: $(SOURCES)
	$(CC) -o $@ $(SOURCES)

valgrind:
	VALGRIND="valgrind --log-file=/tmp/valgrind-%p-.log" $(MAKE)

clean:
	rm -rf lanshare
	find . -name "*.gc*" -exec rm {} \;
	rm -rf `find . -name "*.dSYM" -print`

# The Install
install: all
	@echo NOT IMPLEMENTED

BADFUNCS='[^_.>a-zA-Z0-9](str(n?cpy|n?cat|xfrm|n?dup|str|pbrk|tok|_)|stpn?cpy|a?sn?printf|byte_)'
check:
	@echo File with potentially dangerous functions.
	@egrep $(BADFUNCS) $(SOURCES) || true
