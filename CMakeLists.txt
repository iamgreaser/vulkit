cmake_minimum_required (VERSION 2.6)
project (vulkit)

find_package (PythonInterp REQUIRED)

add_custom_command (
	OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/vulkan.h ${CMAKE_CURRENT_BINARY_DIR}/vulkit_wrapper.c
	COMMAND ${PYTHON_EXECUTABLE} ${PROJECT_SOURCE_DIR}/vulkit/gen_wrapper.py ${PROJECT_SOURCE_DIR}/specs/vk.xml
	)

add_library (vulkit SHARED
	${CMAKE_CURRENT_BINARY_DIR}/vulkan.h
	${CMAKE_CURRENT_BINARY_DIR}/vulkit_wrapper.c)

target_link_libraries (vulkit vulkan)

install (FILES ${CMAKE_CURRENT_BINARY_DIR}/vulkan.h DESTINATION include/vulkit)
install (FILES ${CMAKE_CURRENT_BINARY_DIR}/libvulkit.so DESTINATION lib)

