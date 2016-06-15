#!/bin/sh
(cd vulkit && ( \
	python gen_wrapper.py && \
	cc -g -O1 -shared -fPIC -o ../libvulkit.so vulkit_wrapper.c -lvulkan && \
	true \
))

