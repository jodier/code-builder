all:
	@cp code-builder codebuilder.py

	cython --embed codebuilder.py

	gcc `python-config --cflags` -Wno-unused-but-set-variable -Wno-unused-variable -Wno-unused-function -o codebuilder.exe codebuilder.c `python-config --libs` -Wl,--strip-all

	@rm -f codebuilder.py codebuilder.c

