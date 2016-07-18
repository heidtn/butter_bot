cmake_minimum_required (VERSION 2.6)

link_libraries(apriltags ${raspicam_CV_LIBS} ${raspicam_LIBS})

add_executable(apriltags_demo apriltags_demo.cpp Serial.cpp)
pods_install_executables(apriltags_demo)

add_executable(rpitags rpitags.cpp)
pods_install_executables(rpitags)

add_executable(imu imu.cpp Serial.cpp)
pods_install_executables(imu)
