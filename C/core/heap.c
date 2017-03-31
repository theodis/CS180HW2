#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "heap.h"

void heapInit(heap* ret) {
	ret->count = 0;
}

void heapClear(heap* h) {
	h->count = 0;
}

void swap(int* a, int* b) {
	int tmp = *a;
	*a = *b;
	*b = tmp;
}

void heapSwap(heap* h, int i, int j) {
	swap(&h->key[i], &h->key[j]);
	swap(&h->value[i], &h->value[j]);
}

void heapInsertMin(heap* h, int k, int v) {
	int cur = h->count++;
	int next;
	next = (cur - 1) / 2;
	while(cur && h->key[next = (cur - 1) >> 1] > k) {
		h->key[cur] = h->key[next];
		h->value[cur] = h->value[next];
		cur = next;
	}
	h->key[cur] = k;
	h->value[cur] = v;
}

void heapRemoveMin(heap* h, int* k, int* v, int cur) {
	int left, right, largest;

	*k = h->key[cur];
	*v = h->value[cur];

	h->count--;
	h->key[cur] = h->key[h->count];
	h->value[cur] = h->value[h->count];

	while(1){
		largest = cur;
		left = cur * 2 + 1;
		right = cur * 2 + 2;
		if(left < h->count && h->key[left] < h->key[cur]) largest = left;
		if(right < h->count && h->key[right] < h->key[largest]) largest = right;
		if(largest == cur) break;
		heapSwap(h,largest,cur);
		cur = largest;
	}
}
void heapInsertMax(heap* h, int k, int v) {
	int cur = h->count++;
	int next;
	next = (cur - 1) / 2;
	while(cur && h->key[next = (cur - 1) >> 1] < k) {
		h->key[cur] = h->key[next];
		h->value[cur] = h->value[next];
		cur = next;
	}
	h->key[cur] = k;
	h->value[cur] = v;
}

void heapRemoveMax(heap* h, int* k, int* v, int cur) {
	int left, right, largest;

	*k = h->key[cur];
	*v = h->value[cur];

	h->count--;
	h->key[cur] = h->key[h->count];
	h->value[cur] = h->value[h->count];

	while(1){
		largest = cur;
		left = cur * 2 + 1;
		right = cur * 2 + 2;
		if(left < h->count && h->key[left] > h->key[cur]) largest = left;
		if(right < h->count && h->key[right] > h->key[largest]) largest = right;
		if(largest == cur) break;
		heapSwap(h,largest,cur);
		cur = largest;
	}
}
