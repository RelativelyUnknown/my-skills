/* A small C core to put behind a Python binding: explicit status returns, a span (pointer plus length, no NUL),
   and an arena for allocations that share one lifetime. No Python headers here, so it is testable on its own. */
#ifndef CORE_H
#define CORE_H
#include <stddef.h>

/* Values never change once released; CORE_OK is 0. A NULL handle or out-parameter returns CORE_ERR_INVALID. */
typedef enum { CORE_OK = 0, CORE_ERR_INVALID, CORE_ERR_NOMEM, CORE_ERR_OVERFLOW, CORE_ERR_RANGE, CORE_STATUS_MAX_VALUE = 0x7fffffff } core_status;

/* Bytes you do not own. The length travels with the pointer; never depend on a terminating NUL. */
typedef struct { const unsigned char *ptr; size_t len; } span;

/* Fixed capacity, so pointers handed out stay valid until arena_free. */
typedef struct arena arena;
arena *arena_new(size_t capacity);                                /* NULL on failure */
void *arena_alloc(arena *a, size_t count, size_t size, core_status *st); /* NULL with *st set */
void arena_free(arena *a);                                        /* accepts NULL */

/* Split at the first `sep`: left is before it, right is after it. CORE_ERR_RANGE when there is no `sep`.
   Views into `in`; nothing is copied or allocated. */
core_status span_split(span in, unsigned char sep, span *left, span *right);
#endif
