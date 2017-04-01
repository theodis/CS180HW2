#include <stdio.h>
#include "core/heap.h"
#include "core/morph.h"

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

	int move = morphMoveStringToMove(moveStr);
	scanf("%s",boardStr);
	morphInit(&m, boardStr, player);
	morphGenMoves(&m, &h, -1, player);
	for(int i = 0; i < h.count; i++) {
		if(h.value[i] == move) {
			printf("1");
			return 0;
		}
	}
	printf("0");
	return 0;
}
