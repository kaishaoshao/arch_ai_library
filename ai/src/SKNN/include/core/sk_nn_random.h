// Based on pcg random number generator (https://www.pcg-random.org)
// Licensed under Apache License 2.0 (NO WARRANTY, etc. see website)
#ifndef __SK_NN_RANDOM_H__
#define __SK_NN_RANDOM_H__

typedef struct sk_nn_random
{
  sk_u64 state;
  sk_u16 inc;
} sk_pcg_state;

void sk_pcg_seed(sk_u64 initstate, sk_u64 initseq);

void sk_pcg_seed_r(sk_pcg_state *rng, sk_u64 initstate, sk_u64 initseq);

sk_u32 sk_pcg_rand(void);

sk_u32 sk_pcg_rand_r(sk_pcg_state *rng);

sk_f32 sk_pcg_randf(void);

sk_f32 sk_pcg_randf_r(sk_pcg_state *rng);

#endif //__SK_NN_RANDOM_H__
