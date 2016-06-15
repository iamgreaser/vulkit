#!/bin/sh
if [ "x${PREFIX}" = "x" ]; then
	PREFIX=/usr/local
fi
if [ "x${LIBDIR}" = "x" ]; then
	LIBDIR=${PREFIX}/lib
fi
if [ "x${INCDIR}" = "x" ]; then
	INCDIR=${PREFIX}/include
fi

install -m 755 -d ${DESTDIR}${INCDIR}/vulkit/ && \
install -m 755 -d ${DESTDIR}${LIBDIR}/ && \
install -m 755 libvulkit.so ${DESTDIR}${LIBDIR}/libvulkit.so.0 && \
ln -f -s ${DESTDIR}${LIBDIR}/libvulkit.so.0 ${DESTDIR}${LIBDIR}/libvulkit.so && \
install -m 644 vulkit/vulkan.h ${DESTDIR}${INCDIR}/vulkit/vulkan.h && \
ldconfig && \
true

