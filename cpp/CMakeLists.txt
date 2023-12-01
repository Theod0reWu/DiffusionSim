cmake_minimum_required(VERSION 3.1...3.20)
project(DiffusionSim)

#CGAL_Qt5 is needed for the drawing.
find_package(CGAL REQUIRED OPTIONAL_COMPONENTS Qt5)
if(CGAL_Qt5_FOUND)
    #required to use basic_viewer
    add_definitions(-DCGAL_USE_BASIC_VIEWER -DQT_NO_KEYWORDS)
else()
    message(FATAL_ERROR "qt not found")
endif()
#create the executable of the application
create_single_source_cgal_program("point_locality.cpp")
if(CGAL_Qt5_FOUND)
    #link it with the required CGAL libraries
    target_link_libraries(point_locality PUBLIC CGAL::CGAL_Qt5)
else()
    message(FATAL_ERROR "qt not found")
endif()

set(CGAL_DO_NOT_WARN_ABOUT_CMAKE_BUILD_TYPE TRUE)
#end of the file