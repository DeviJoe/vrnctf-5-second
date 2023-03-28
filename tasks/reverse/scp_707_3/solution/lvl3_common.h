#ifndef LVL3_COMMON_H
#define LVL3_COMMON_H

#include <stdint.h>

#define BLOCK_SIZE_BYTES          32U
#define BLOCK_PIECES_COUNT        4U
#define SHIFT_COUNT               5
#define ROUND_COUNT               7
#define BLOCK_PAD_SIGN            0xFF

#define IV                        { 0xC0U,  0xC1U,  0xC2U,  0xC3U,  0xC4U,  0xC5U,  0xC6U,  0xC7U,  0xC8U,  0xC9U,  0xCAU,  0xCBU,  0xCCU,  0xCDU,  0xCEU,  0xCFU, \
                                    0xD0U,  0xD1U,  0xD2U,  0xD3U,  0xD4U,  0xD5U,  0xD6U,  0xD7U,  0xD8U,  0xD9U,  0xDAU,  0xDBU,  0xDCU,  0xDDU,  0xDEU,  0xDFU }

typedef uint8_t bc_block[BLOCK_SIZE_BYTES];


// xors two blocks, saves result into block_a
static inline void xor_blocks(bc_block block_a, const bc_block block_b)
{
  uint32_t idx;

  for (idx = 0; idx < BLOCK_SIZE_BYTES; idx++)
  {
    block_a[idx] ^= block_b[idx];
  }
}



#endif /* LVL3_COMMON_H */
