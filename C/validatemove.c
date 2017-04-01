#include <stdio.h>
#include "core/morph.h"
#include "core/heap.h"

/*
 * Arg 1 - Player number (1 or 2)
 * Arg 2 - Player move
 * StdIn - Board
 * StdOut - 1 for good, 0 for bad
 */

morph m;
heap h;

int main(int argc, char* argv[]) {
	if(argc != 3) return 0;

	int player = argv[1][0] - '1';
	int k,v;
	char* moveStr = argv[2];
	char boardStr[50];

	scanf("%s",boardStr);
	morphInit(&m, boardStr, player);
	morphGenMoves(&m, &h, -1, player);

	return 0;
}
