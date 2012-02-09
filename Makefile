all:
	@cp code-builder codebuilder.py

	cython --embed codebuilder.py

	gcc `python-config --cflags` -Wno-unused-variable -Wno-unused-function -o codebuilder.exe codebuilder.c `python-config --libs` -Wl,-s

	@rm -f codebuilder.py codebuilder.c

