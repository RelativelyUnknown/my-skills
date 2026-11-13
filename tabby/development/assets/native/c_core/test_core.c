#include "core.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int failures;
#define CHECK(cond) do { if (!(cond)) { printf("FAIL %s:%d %s\n", __FILE__, __LINE__, #cond); failures++; } } while (0)

int main(void) {
    core_status st;
    arena *a = arena_new(64);
    CHECK(a != NULL);

    int *xs = arena_alloc(a, 4, sizeof *xs, &st);
    CHECK(st == CORE_OK && xs != NULL && ((uintptr_t)xs % 16) == 0);
    for (int i = 0; i < 4; i++) xs[i] = i;

    CHECK(arena_alloc(a, SIZE_MAX / 2, 4, &st) == NULL && st == CORE_ERR_OVERFLOW);  /* overflow is not out-of-memory */
    CHECK(arena_alloc(a, 1000, 1, &st) == NULL && st == CORE_ERR_NOMEM);
    CHECK(arena_alloc(a, 0, 8, &st) != NULL && st == CORE_OK);                       /* zero-size is fine */
    CHECK(arena_alloc(NULL, 1, 1, &st) == NULL && st == CORE_ERR_INVALID);          /* NULL handle: an error, not a crash */
    arena_free(a);
    arena_free(NULL);

    const unsigned char raw[] = {'k', 'e', 'y', '=', 'v', 0, 'x'};               /* an embedded NUL */
    span in = {raw, sizeof raw}, l, r;
    CHECK(span_split(in, '=', &l, &r) == CORE_OK);
    CHECK(l.len == 3 && memcmp(l.ptr, "key", 3) == 0);
    CHECK(r.len == 3 && r.ptr[1] == 0);                                              /* nothing stopped at the NUL */
    span none = {NULL, 0};
    CHECK(span_split(none, '=', &l, &r) == CORE_ERR_RANGE);
    span noeq = {raw, 3};
    CHECK(span_split(noeq, '=', &l, &r) == CORE_ERR_RANGE);

    CHECK(span_split(in, '=', NULL, &r) == CORE_ERR_INVALID);

    if (failures) return 1;
    puts("core: ok");
    return 0;
}
