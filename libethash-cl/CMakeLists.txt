# A custom command and target to turn the OpenCL kernel into a byte array header
# The normal build depends on it properly and if the kernel file is changed, then
# a rebuild of libethash-cl should be triggered

#TODO: clean up the copy&pasting here
add_custom_command(
	OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/ethash.h
	COMMAND ${CMAKE_COMMAND} ARGS
	-DBIN2H_SOURCE_FILE="${CMAKE_CURRENT_SOURCE_DIR}/kernels/cl/ethash.cl"
	-DBIN2H_VARIABLE_NAME=ethash_cl
	-DBIN2H_HEADER_FILE="${CMAKE_CURRENT_BINARY_DIR}/ethash.h"
	-P "${CMAKE_CURRENT_SOURCE_DIR}/bin2h.cmake"
	COMMENT "Generating OpenCL Kernel Byte Array"
	DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/kernels/cl/ethash.cl
)
add_custom_target(clbin2h_stable DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/ethash.h ${CMAKE_CURRENT_SOURCE_DIR}/cl/ethash.cl)

set(SOURCES
	CLMiner.h CLMiner.cpp
	${CMAKE_CURRENT_BINARY_DIR}/ethash.h
)

if(APPLE)
	# On macOS use system OpenCL library.
	find_package(OpenCL REQUIRED)
else()
	if(NOT OpenCL_INCLUDE_DIR STREQUAL "")
		# Run cmake .. \
		#           -DOpenCL_INCLUDE_DIR=/home/hosts/amd64-linux/build/MYOWNCL/build/CL/include \
		#           -DOpenCL_LIBRARY=/home/hosts/amd64-linux/build/MYOWNCL/build/CL/lib/libOpenCL.a
		# which sets:
		#    OpenCL_INCLUDE_DIR=/home/hosts/amd64-linux/build/MYOWNCL/build/CL/include
		#    OpenCL_LIBRARY=/home/hosts/amd64-linux/build/MYOWNCL/build/CL/lib/libOpenCL.a

		# Do the things like the hunter package file does
		# see ~/.hunter/_Base/0XXXXXX/0YYYYYY/0ZZZZZ/Install/lib/cmake/OpenCL/* files
		#          starting with OpenCLConfig.cmake
		# If we have a OpenCLConfig.cmake in our own CL build we can try using
		#    find_package(OpenCL CONFIG REQUIRED HINTS /home/hosts/amd64-linux/build/MYOWNCL/build/CL)

		include(CMakeFindDependencyMacro)
		find_dependency(Threads)

		# TODO: check if we link static or the dll
		# Create imported target OpenCL::OpenCL - static
		#add_library(OpenCL::OpenCL STATIC IMPORTED)

		# or as dll (so)
		add_library(OpenCL::OpenCL SHARED IMPORTED)

		set_target_properties(OpenCL::OpenCL PROPERTIES
			INTERFACE_INCLUDE_DIRECTORIES "${OpenCL_INCLUDE_DIR}"
			INTERFACE_LINK_LIBRARIES "\$<LINK_ONLY:Threads::Threads>;\$<LINK_ONLY:dl>"
		)
		set_property(TARGET OpenCL::OpenCL APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
		set_target_properties(OpenCL::OpenCL PROPERTIES
		  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
		  IMPORTED_LOCATION_RELEASE "${OpenCL_LIBRARY}"
		  )

		include_directories(BEFORE "${OpenCL_INCLUDE_DIR}")

		# todo: set OpenCL version

		set(OpenCL_FOUND "1")
		message(STATUS "Using own OPENCL")
		message(STATUS "    Include ${OpenCL_INCLUDE_DIR}")
		message(STATUS "    Library ${OpenCL_LIBRARY}")
	else()
		hunter_add_package(OpenCL)
		find_package(OpenCL CONFIG REQUIRED)
		#message(STATUS "OpenCL Info:")
		message(STATUS "Used OpenCL Package File: ${OpenCL_CONFIG}")
		#message(FATAL_ERROR "ERROR")
	endif()
endif()

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(..)

add_library(ethash-cl ${SOURCES})
target_link_libraries(ethash-cl PUBLIC ethcore ethash::ethash)
target_link_libraries(ethash-cl PRIVATE OpenCL::OpenCL)
target_link_libraries(ethash-cl PRIVATE Boost::filesystem)
