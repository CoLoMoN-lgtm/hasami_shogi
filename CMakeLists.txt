cmake_minimum_required(VERSION 3.15)
project(HasamiShogi)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Windows-specific settings
if(MSVC)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreadedDLL")
    
    # Set RPATH settings
    set(CMAKE_SKIP_BUILD_RPATH FALSE)
    set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
endif()

# Find Python
set(Python3_FIND_REGISTRY "LAST")  # Prefer latest version
find_package(Python3 3.12 EXACT COMPONENTS Interpreter Development REQUIRED)

message(STATUS "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
message(STATUS "Python3_LIBRARIES: ${Python3_LIBRARIES}")

# Create the core library
add_library(hasami_shogi_core SHARED
    src/core/src/board.cpp
    src/core/src/game.cpp
    src/core/src/move.cpp
    src/core/src/ai.cpp
)

target_include_directories(hasami_shogi_core
    PUBLIC 
        ${CMAKE_CURRENT_SOURCE_DIR}/src/core/include
)

# Create Python bindings
add_library(hasami_shogi_python MODULE
    src/python_bindings.cpp
)

target_include_directories(hasami_shogi_python
    PRIVATE
        ${Python3_INCLUDE_DIRS}
        ${CMAKE_CURRENT_SOURCE_DIR}/src/core/include
)

target_link_libraries(hasami_shogi_python
    PRIVATE
        hasami_shogi_core
        Python3::Python
)

# Set output properties
set_target_properties(hasami_shogi_python PROPERTIES
    PREFIX ""
    OUTPUT_NAME "hasami_shogi"
    SUFFIX ".pyd"
    RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_SOURCE_DIR}/src/gui/lib"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/gui/lib"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_SOURCE_DIR}/src/gui/lib"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/gui/lib"
)

set_target_properties(hasami_shogi_core PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_SOURCE_DIR}/src/gui/lib"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/gui/lib"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_SOURCE_DIR}/src/gui/lib"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/gui/lib"
)

# Set DLL directory
set_target_properties(hasami_shogi_python PROPERTIES
    VS_DEBUGGER_ENVIRONMENT "PATH=${CMAKE_SOURCE_DIR}/src/gui/lib;$ENV{PATH}"
)