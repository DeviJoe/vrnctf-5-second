#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "lvl3_common.h"

#define PLAIN_FLAG_PATH "./lvl3_decrypted"
#define CT_FLAG_PATH    "./lvl3_ct"


// blockwise right shift
static void right_shift(uint8_t *buf, const uint8_t buf_size, uint8_t amount)
{
  uint16_t round_idx, subbuf_idx;
  uint8_t subbuf_size = BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT;
  uint8_t last_val[BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT];
  uint8_t tmp[BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT];

  amount %= sizeof(*buf);

  for (round_idx = 0; round_idx < amount; round_idx++)
  {
    // Save last subblock
    memcpy(last_val, &buf[BLOCK_SIZE_BYTES - subbuf_size], subbuf_size);

    for (subbuf_idx = 0; subbuf_idx + 1 < BLOCK_PIECES_COUNT; subbuf_idx++)
    {
      // Store last value in buf
      memcpy(tmp, &buf[(subbuf_idx + 1) * subbuf_size], subbuf_size);

      // Shift
      // buf[subbuf_idx + 1] = buf[subbuf_idx];
      memcpy(&buf[(subbuf_idx + 1) * subbuf_size], &buf[subbuf_idx * subbuf_size], subbuf_size);
      // buf[subbuf_idx] = last_val;
      memcpy(&buf[subbuf_idx * subbuf_size], last_val, subbuf_size);

      // Put last value.
      memcpy(last_val, tmp, subbuf_size);
    }
  }
}


static void left_shift(uint8_t *buf, uint8_t amount)
{
  uint16_t round_idx, subbuf_idx;
  uint8_t subbuf_size = BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT;
  uint8_t last_val[BLOCK_SIZE_BYTES / BLOCK_PIECES_COUNT];

  amount %= BLOCK_PIECES_COUNT;

  for (round_idx = 0; round_idx < amount; round_idx++)
  {
    // Save first subblock (it'll be put into the end)
    memcpy(last_val, buf, subbuf_size);

    // Shift
    for (subbuf_idx = 0; subbuf_idx + 1 < BLOCK_PIECES_COUNT; subbuf_idx++)
    {
      memcpy(&buf[subbuf_idx * subbuf_size], &buf[(subbuf_idx + 1) * subbuf_size], subbuf_size);
    }

    memcpy(&buf[BLOCK_SIZE_BYTES - subbuf_size], last_val, subbuf_size);
  }
}

static void decipher_block(bc_block block, const bc_block prev_block, const bc_block key)
{
  uint8_t round_idx, block_piece, tmp;

  for (round_idx = 0; round_idx < ROUND_COUNT; round_idx++)
  {
    xor_blocks(block, key);
    left_shift(block, SHIFT_COUNT);
  }

  xor_blocks(block, prev_block);
}



static uint8_t remove_tail(bc_block last_buf, const bc_block prev_block, const bc_block key)
{
  int32_t idx;
  decipher_block(last_buf, prev_block, key);

  for (idx = 0; idx < BLOCK_SIZE_BYTES; idx++)
  {
    // found reminder
    if (last_buf[BLOCK_SIZE_BYTES - idx - 1] != BLOCK_PAD_SIGN)
    {
      break;
    }
  }

  return last_buf[BLOCK_SIZE_BYTES - idx - 1];
}

int main (int argc, char** argv)
{
  FILE *pt_file, *ct_file;
  int64_t filesize, offset;
  uint8_t tail_offset;
  bc_block buffs[2], key;

  // Should be reversed =)
  const bc_block iv = IV;

  pt_file = fopen(PLAIN_FLAG_PATH, "wb");
  ct_file = fopen(CT_FLAG_PATH, "rb");

  // Get file size
  fseek(ct_file, - (3 * (int32_t) BLOCK_SIZE_BYTES), SEEK_END);
  offset = ftell(ct_file);

  fseek(pt_file, offset + BLOCK_SIZE_BYTES, SEEK_SET);

  // Read two_buffs and the key
  fread(buffs, 2, BLOCK_SIZE_BYTES, ct_file);
  fread(key, 1, BLOCK_SIZE_BYTES, ct_file);

  tail_offset = remove_tail(buffs[1], buffs[0], key);

  // alloc file
  filesize = offset + tail_offset;

  if (tail_offset != 0)
  {
    fwrite(buffs[1], 1, tail_offset, pt_file);
  }

  memcpy(buffs[1], buffs[0], BLOCK_SIZE_BYTES);

  while(offset >= BLOCK_SIZE_BYTES)
  {
    fseek(ct_file, offset - BLOCK_SIZE_BYTES, SEEK_SET);
    fseek(pt_file, offset, SEEK_SET);

    fread(buffs[0], 1, BLOCK_SIZE_BYTES, ct_file);

    decipher_block(buffs[1], buffs[0], key);
    fwrite(buffs[1], 1, BLOCK_SIZE_BYTES, pt_file);

    memcpy(buffs[1], buffs[0], BLOCK_SIZE_BYTES);

    offset -= 2 * BLOCK_SIZE_BYTES;
  }

  decipher_block(buffs[1], iv, key);

  fseek(pt_file, 0, SEEK_SET);
  fwrite(buffs[1], 1, BLOCK_SIZE_BYTES, pt_file);

  fclose(pt_file);
  fclose(ct_file);
  return 0;
}