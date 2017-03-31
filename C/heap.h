#ifndef _HEAP
#define _HEAP

#define HEAP_SIZE	64

typedef struct heap {
	int key[HEAP_SIZE];
	int value[HEAP_SIZE];
	int count;
}heap;

void heapInit(heap* h);
void heapClear(heap* h);
void heapInsertMin(heap* h, int k, int v);
void heapRemoveMin(heap* h, int* k, int* v, int cur);
void heapInsertMax(heap* h, int k, int v);
void heapRemoveMax(heap* h, int* k, int* v, int cur);

#endif
