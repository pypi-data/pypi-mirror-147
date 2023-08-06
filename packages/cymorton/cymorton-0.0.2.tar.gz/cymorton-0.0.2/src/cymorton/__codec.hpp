#ifndef _MORTON_H_
#define _MORTON_H_

#include <string>
#include <stdint.h>

#define MAX_Z 20

uint64_t interleaveToNumber(uint64_t number);
uint64_t convertXYLevelToCode(uint32_t x, uint32_t y, uint8_t z);
uint64_t convertLatLonLevelToCode(double latitude, double longitude, uint8_t z);
double getQuadAngularWidth(uint8_t level);
double getQuadAngularHeight(uint8_t level);
uint32_t convertLonLevelToX(double longitude, uint8_t z);
uint32_t convertLatLevelToY(double latitude, uint8_t z);
double convertXLevelToLon(uint32_t x, uint8_t z);
double convertYLevelToLat(uint32_t y, uint8_t z);

#endif
