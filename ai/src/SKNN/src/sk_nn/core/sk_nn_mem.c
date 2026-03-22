#include "sk_nn.h"

sk_mem* mem_create(sk_u64 reserve_size, sk_u64 commit_size) {

}

void mem_destroy(sk_mem* mem) {

}

void* mem_push(sk_mem* mem, sk_u64 size, sk_bool non_zero)
{

}

void mem_pop(sk_mem* mem, sk_u64 size) {

}

void mem_pop_to(sk_mem* mem, sk_u64 pos) {

}

void mem_clear(sk_mem* mem) {

}

sk_tmp_mem mem_temp_begin(sk_mem* mem) {

}

void mem_temp_end(sk_tmp_mem temp) {

}

sk_tmp_mem mem_scratch_get(sk_mem* conflicts, sk_u32 num_conflicts) {

}

void mem_scratch_release(sk_tmp_mem scratch) {

}
