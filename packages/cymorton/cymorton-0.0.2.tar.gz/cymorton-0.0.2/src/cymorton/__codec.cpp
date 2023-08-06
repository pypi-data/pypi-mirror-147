#include "__codec.hpp"
#include <algorithm>
#include <iostream>
using namespace std;


uint64_t interleaveToNumber(uint64_t number) {
    number = (number | (number << 16)) & 0x0000FFFF0000FFFF;
    number = (number | (number << 8))  & 0x00FF00FF00FF00FF;
    number = (number | (number << 4))  & 0x0F0F0F0F0F0F0F0F;
    number = (number | (number << 2))  & 0x3333333333333333;
    number = (number | (number << 1))  & 0x5555555555555555;
    return number;
}

uint64_t convertXYLevelToCode(uint32_t x, uint32_t y, uint8_t z) {
    return interleaveToNumber(x) | (interleaveToNumber(y) << 1) | ((uint64_t)1 << (z * 2));
}

double getQuadAngularWidth(uint8_t level) {
    return 360.0 / (1L << level);
}

uint32_t getXMaxValue(uint8_t z) {
    return (uint32_t) ((1L << z) - 1);
}

uint32_t getYMaxValue(uint8_t z) {
    return (uint32_t) (((1L << z) - 1) / 2);
}

double getQuadAngularHeight(uint8_t level) {
    if (level == 0) return 180;
    return 360.0 / (1L << level);
}

uint32_t convertLatLevelToY(double latitude, uint8_t z) {
    uint32_t y = (uint32_t) ((latitude + 90) / getQuadAngularHeight(z));
    y = min(getYMaxValue(z), y);
    return y;
}

uint32_t convertLonLevelToX(double longitude, uint8_t z) {
    uint32_t x = 0;
    if (longitude != -180.0 && longitude != 180.0) {
        x = (uint32_t) ((longitude + 180) / getQuadAngularWidth(z));
        x = min(getXMaxValue(z), x);
    }
    return x;
}

double convertXLevelToLon(uint32_t x, uint8_t z) {
    return x * getQuadAngularWidth(z) - 180;
}

double convertYLevelToLat(uint32_t y, uint8_t z) {
    return y * getQuadAngularHeight(z) - 90;
}

uint64_t convertLatLonLevelToCode(double latitude, double longitude, uint8_t z) {
    return convertXYLevelToCode(convertLonLevelToX(longitude, z), convertLatLevelToY(latitude, z), z);
}
