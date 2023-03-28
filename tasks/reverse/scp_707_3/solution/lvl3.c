#include <stdio.h>
#include <string.h>

#include "lvl3_common.h"

#define PLAIN_FLAG_PATH "./lvl3_flag"
#define CT_FLAG_PATH    "./lvl3_ct"

#define KEY                       { 0x17U,  0xD0U,  0xCEU,  0xB5U,  0xBDU,  0xC3U,  0xD4U,  0x27U,  0x14U,  0x02U,  0x69U,  0xC5U,  0xEDU,  0x5FU,  0x0AU,  0x06U, \
                                    0x5BU,  0x37U,  0x1BU,  0xE3U,  0x37U,  0x59U,  0x42U,  0xEBU,  0x9BU,  0xD5U,  0x50U,  0x31U,  0x8CU,  0x9EU,  0xF0U,  0x06U }


const bc_block g_key = KEY;


static inline void right_shift(uint8_t *buf, uint8_t amount)
{
  uint16_t round_idx, subbuf_idx;
  uint8_t subbuf_size = BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT;
  uint8_t last_val[BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT];
  uint8_t tmp[BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT];

  amount %= BLOCK_PIECES_COUNT;

  for (round_idx = 0; round_idx < amount; round_idx++)
  {
    memcpy(last_val, &buf[BLOCK_SIZE_BYTES - subbuf_size], subbuf_size);

    for (subbuf_idx = 0; subbuf_idx < BLOCK_PIECES_COUNT; subbuf_idx++)
    {
      memcpy(tmp, last_val, subbuf_size); //
      memcpy(last_val, &buf[subbuf_idx * subbuf_size], subbuf_size);
      // Shift
      // buf[subbuf_idx + 1] = buf[subbuf_idx];
      memcpy(&buf[subbuf_idx * subbuf_size], tmp, subbuf_size);
    }
  }
}


// CBC
static void __attribute__ ((noinline)) process_block(bc_block block, const bc_block prev_block)
{
  uint8_t round_idx, block_piece, tmp;
  xor_blocks(block, prev_block);

  for (round_idx = 0; round_idx < ROUND_COUNT; round_idx++)
  {
    right_shift(block, SHIFT_COUNT);
    xor_blocks(block, g_key);
  }
}


static inline void pad_tail(bc_block block, const bc_block prev_value, int64_t filesize)
{
  filesize %= BLOCK_SIZE_BYTES;

  // Write reminder
  // n FF FF FF
  block[filesize] = filesize;

  if (filesize != BLOCK_SIZE_BYTES - 1)
  {
    memset(&block[filesize + 1], BLOCK_PAD_SIGN, BLOCK_SIZE_BYTES - filesize - 1);
  }

  process_block(block, prev_value);
}


int main (int argc, char** argv)
{
  FILE *pt_file, *ct_file;
  int64_t filesize, offset;
  bc_block buf, prev_value = IV;

  pt_file = fopen(PLAIN_FLAG_PATH, "rb");
  ct_file = fopen(CT_FLAG_PATH, "wb");

  // Get file size
  fseek(pt_file, 0L, SEEK_END);
  filesize = ftell(pt_file);

  fseek(pt_file, 0L, SEEK_SET);

  for (offset = 0; filesize - offset >= BLOCK_SIZE_BYTES ; offset+=BLOCK_SIZE_BYTES)
  {
    fread(buf, 1, BLOCK_SIZE_BYTES, pt_file);

    process_block(buf, prev_value);
    memcpy(prev_value, buf, BLOCK_SIZE_BYTES);

    fwrite(buf, 1, BLOCK_SIZE_BYTES, ct_file);
  }

  if (filesize - offset != 0)
  {
    fread(buf, filesize - offset, 1, pt_file);
  }

  pad_tail(buf, prev_value, filesize);

  fwrite(buf, 1, BLOCK_SIZE_BYTES, ct_file);

  fwrite(g_key, 1, BLOCK_SIZE_BYTES, ct_file);

  printf("key: ");

  for (offset = 0; offset < BLOCK_SIZE_BYTES; offset++)
  {
    printf("%02x", g_key[offset]);
  }

  printf("\n");

  fclose(pt_file);
  fclose(ct_file);
  return 0;
}