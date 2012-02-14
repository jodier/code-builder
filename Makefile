all:
	cython --embed codebuilder.py

	gcc `python-config --cflags` -Wno-unused-variable -Wno-unused-function -o codebuilder codebuilder.c `python-config --libs` -Wl,-s

