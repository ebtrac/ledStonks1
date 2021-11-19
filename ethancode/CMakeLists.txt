cmake_minimum_required(VERSION 3.10.2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(DCMAKE_TOOLCHAIN_FILE /home/dietpi/vcpkg/scripts/buildsystems/vcpkg.cmake)
project(json)

find_package(JSONCPP REQUIRED)

add_executable(json
	json.cc
)

target_link_libraries(json

)
