#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define PLAIN_FLAG_PATH "./lvl2_decrypted"
#define CT_FLAG_PATH    "./lvl2_ct"

uint32_t xor (uint32_t a, uint32_t b) {
  return a ^ b;
}

int main(int argc, char *argv[])
{
  uint8_t buffer[4];
  uint8_t buf_key[4];
  uint32_t buf_32;
  uint32_t key_init;
  FILE *file = fopen(CT_FLAG_PATH, "rb");
  FILE *output = fopen(PLAIN_FLAG_PATH, "wb");

  size_t count1 = fread(buf_key, 1, 4, file);
  memcpy(&key_init, buf_key, 4);

  while (!feof(file)) // to read file
  {
    uint32_t res_buf = 0;
    key_init++;

    memset(buffer, 0, 4);
    // function used to read the contents of file
    size_t count = fread(buffer, sizeof(uint8_t), 4, file);
    memcpy(&buf_32, buffer, 4);

    if (key_init % 42 == 0)
    {
      res_buf = xor(buf_32 + 0x42424242, 0xFFFFFFFF);
    } else if (key_init % 31 == 0)
    {
      res_buf = xor(buf_32 + 0x31313131, 0xF0F0F0F0);
    } else if (key_init % 25 == 0)
    {
      res_buf = xor(buf_32 + 0x25252525, 0x0F0F0F0F);
    } else if (key_init % 13 == 0)
    {
      res_buf = xor(buf_32 + 0x13131313, 0xFFFF0000);
    } else if (key_init % 7 == 0)
    {
      res_buf = xor(buf_32 + 0x07070707, 0x0000FFFF);
    } else if (key_init % 5 == 0)
    {
      res_buf = xor(buf_32 + 0x05050505, 0xF840F840);
    } else if (key_init % 2 == 0)
    {
      res_buf = xor(buf_32 + 0x02020202, 0b10101010101010101010101010101010);
    } else {
      res_buf = xor(buf_32 + 0x01010101, 0b01010101010101010101010101010101);
    }

    memcpy(buffer, &res_buf, 4);

    fwrite(buffer, 1, count, output);
  }

  fclose(output);
}