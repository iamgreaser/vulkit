#!/bin/sh
python vulkit/gen_wrapper.py specs/vk.xml && \
cc -g -O1 -shared -fPIC -o libvulkit.so vulkit_wrapper.c -lvulkan && \
true

