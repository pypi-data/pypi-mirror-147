# morton.pyx
# distutils: sources = src/cymorton/__codec.cpp
# cython: embed=True
# cython: linetrace=True, language_level=3
# distutils: define_macros=CYTHON_TRACE=1
# distutils: language = c++


def max_z():
    return MAX_Z


def interleave_to_number(uint64_t number):
    return interleaveToNumber(number)


def get_quad_angular_width(unsigned char z):
    return getQuadAngularWidth(z)


def get_quad_angular_height(unsigned char z):
    return getQuadAngularHeight(z)


def convert_lon_level_to_x(double longitude, unsigned char z):
    return convertLonLevelToX(longitude, z);


def convert_lat_level_to_y(double latitude, unsigned char z):
    return convertLatLevelToY(latitude, z);


def convert_x_level_to_lon(uint32_t x, unsigned char z):
    return convertXLevelToLon(x, z)


def convert_y_level_to_lat(uint32_t y, unsigned char z):
    return convertYLevelToLat(y, z)


def convert_xy_level_to_code(uint32_t x, uint32_t y, unsigned char z):
    return convertXYLevelToCode(x, y, z)


def convert_lat_lon_level_to_code(double latitude, double longitude, unsigned char z):
    return convertLatLonLevelToCode(latitude, longitude, z)

