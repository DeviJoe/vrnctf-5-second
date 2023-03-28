#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <openssl/sha.h>

#define PLAIN_FLAG_PATH "./lvl1_plain"
#define CT_FLAG_PATH    "./lvl1_ct"

#define SHA1_LENGTH     20
#define PORTION_SIZE    2
#define PAD_SIGNATURE   0xFFU

int main(void)
{
  FILE *pt_file, *ct_file;
  char buf[PORTION_SIZE];
  pt_file = fopen(PLAIN_FLAG_PATH, "r");
  ct_file = fopen(CT_FLAG_PATH, "w");
  uint8_t hash[SHA1_LENGTH];
  size_t ret;

  while (1)
  {
    int i = 0;

    ret = fread(buf, 1, PORTION_SIZE, pt_file);

    if (ret == 0)
    {
      break;
    }

    if (ret != PORTION_SIZE)
    {
      memset(buf, PAD_SIGNATURE, PORTION_SIZE - ret);
    }

    SHA1(buf, PORTION_SIZE, hash);
    fwrite(hash, SHA1_LENGTH, 1, ct_file);
  }

  fclose(ct_file);
  fclose(pt_file);
  return 0;
}