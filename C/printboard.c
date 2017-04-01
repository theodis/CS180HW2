#include <stdio.h>
#include "core/heap.h"
#include "core/morph.h"

/*
 * StdIn - Board
 * StdOut - Resulting Board
 */

morph m;

int main(int argc, char* argv[]) {
	char boardStr[50];

	scanf("%s",boardStr);
	morphInit(&m, boardStr, 1);
	morphPrint(&m);
	return 0;
}
