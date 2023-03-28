#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define PLAIN_FLAG_PATH "./lvl2_plain"
#define CT_FLAG_PATH    "./lvl2_ct"


uint32_t xor (uint32_t a, uint32_t b) {
  return a ^ b;
}

int main(int argc, char *argv[])
{
  uint8_t buffer[4];
  uint8_t buf_key[4];
  uint32_t buf_32;
  uint32_t i = 12468;
  FILE *file = fopen(PLAIN_FLAG_PATH, "rb");
  FILE *output = fopen(CT_FLAG_PATH, "wb");

  memcpy(buf_key, &i, 4);
  fwrite(buf_key, 1, 4, output);

  while (!feof(file)) // to read file
  {
    uint32_t res_buf = 0;
    i++;
    memset(buffer, 0, 4);
    // function used to read the contents of file
    size_t count = fread(buffer, sizeof(uint8_t), 4, file);
    memcpy(&buf_32, buffer, 4);

    if (i % 42 == 0)
    {
      res_buf = xor(buf_32, 0xFFFFFFFF) - 0x42424242;
    } else if (i % 31 == 0)
    {
      res_buf = xor(buf_32, 0xF0F0F0F0) - 0x31313131;
    } else if (i % 25 == 0)
    {
      res_buf = xor(buf_32, 0x0F0F0F0F) - 0x25252525;
    } else if (i % 13 == 0)
    {
      res_buf = xor(buf_32, 0xFFFF0000) - 0x13131313;
    } else if (i % 7 == 0)
    {
      res_buf = xor(buf_32, 0x0000FFFF) - 0x07070707;
    } else if (i % 5 == 0)
    {
      res_buf = xor(buf_32, 0xF840F840) - 0x05050505;
    } else if (i % 2 == 0)
    {
      res_buf = xor(buf_32, 0b10101010101010101010101010101010) - 0x02020202;
    } else {
      res_buf = xor(buf_32, 0b01010101010101010101010101010101) - 0x01010101;
    }

    memcpy(buffer, &res_buf, 4);

    fwrite(buffer, 1, count, output);
  }

  fclose(output);
}
