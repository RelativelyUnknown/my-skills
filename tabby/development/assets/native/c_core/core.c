#include "core.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define ALIGN 16u

struct arena { unsigned char *base; size_t cap; size_t used; };

arena *arena_new(size_t capacity) {
    arena *a = malloc(sizeof *a);
    if (!a) return NULL;
    a->base = malloc(capacity ? capacity : 1);
    if (!a->base) { free(a); return NULL; }
    a->cap = capacity;
    a->used = 0;
    return a;
}

void *arena_alloc(arena *a, size_t count, size_t size, core_status *st) {
    /* Check the multiplication and the alignment padding before trusting either: sizes may come from input. */
    if (size != 0 && count > SIZE_MAX / size) { *st = CORE_ERR_OVERFLOW; return NULL; }
    size_t bytes = count * size;
    size_t start = (a->used + (ALIGN - 1)) & ~(size_t)(ALIGN - 1);
    if (start < a->used || bytes > a->cap || start > a->cap - bytes) { *st = CORE_ERR_NOMEM; return NULL; }
    a->used = start + bytes;
    *st = CORE_OK;
    return a->base + start;
}

void arena_free(arena *a) {
    if (!a) return;
    free(a->base);
    free(a);
}

core_status span_split(span in, unsigned char sep, span *left, span *right) {
    const unsigned char *hit = in.len ? memchr(in.ptr, sep, in.len) : NULL;
    if (!hit) return CORE_ERR_RANGE;
    size_t n = (size_t)(hit - in.ptr);
    left->ptr = in.ptr;
    left->len = n;
    right->ptr = hit + 1;
    right->len = in.len - n - 1;
    return CORE_OK;
}
