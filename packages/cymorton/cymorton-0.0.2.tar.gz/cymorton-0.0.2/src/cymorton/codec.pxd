# codec.pyx
# distutils: language = c++

from libcpp.string cimport string

cdef extern from "stdint.h" nogil:
    ctypedef unsigned char uint8_t
    ctypedef unsigned long uint32_t
    ctypedef unsigned long long uint64_t


cdef extern from '__codec.hpp' nogil:
    cdef:
        uint64_t interleaveToNumber(uint64_t)
        uint64_t convertXYLevelToCode(uint32_t, uint32_t, unsigned char)
        uint64_t convertLatLonLevelToCode(double, double, unsigned char)
        double getQuadAngularWidth(unsigned char);
        double getQuadAngularHeight(unsigned char);
        uint32_t convertLonLevelToX(double, unsigned char);
        uint32_t convertLatLevelToY(double, unsigned char);
        double convertXLevelToLon(uint32_t, unsigned char);
        double convertYLevelToLat(uint32_t, unsigned char);
        unsigned char getCLZ(uint64_t);
        uint32_t getQuadX(uint64_t);
        uint32_t getQuadY(uint64_t);
        unsigned char getQuadZ(uint64_t);
        uint8_t MAX_Z;

