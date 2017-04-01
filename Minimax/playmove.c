#include <stdio.h>
#include "core/heap.h"
#include "core/morph.h"

/*
 * Arg 1 - Player number (1 or 2)
 * Arg 2 - Player move
 * StdIn - Board
 * StdOut - Resulting Board
 */

morph m;

int main(int argc, char* argv[]) {
	if(argc != 3) return 0;

	int player = argv[1][0] - '1';
	char* moveStr = argv[2];
	char boardStr[50];

	int move = morphMoveStringToMove(moveStr);
	scanf("%s",boardStr);
	morphInit(&m, boardStr, player);
	morphPlayMove(&m, move);
	morphPrintString(&m);
	return 0;
}
