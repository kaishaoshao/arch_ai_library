#ifndef __SK_NN_MODULE_H__
#define __SK_NN_MODULE_H__

typedef enum {
  MV_FLAG_NONE = 0,
  MV_FLAG_REQUIRES_GRAD = (1 << 0),
  MV_FLAG_PARAMETER = (1 << 1),
  MV_FLAG_INPUT = (1 << 2),
  MV_FLAG_OUTPUT = (1 << 3),
  MV_FLAG_DESIRED_OUTPUT = (1 << 4),
  MV_FLAG_COST = (1 << 5),
} model_flags;

typedef struct model_var {
  sk_u32 index;
  sk_u32 flags;

  sk_matrix *val;
  sk_matrix *grad;

  
}

#endif // __SK_NN_MODULE_H__
