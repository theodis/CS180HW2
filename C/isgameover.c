#include <stdio.h>
#include "core/heap.h"
#include "core/morph.h"

/*
 * Arg 1 - Player number (1 or 2)
 * StdIn - Board
 * StdOut - 0 for no winner, 1 for player 1 win, 2 for player 2 win
 */

morph m;
heap h;

int main(int argc, char* argv[]) {
	if(argc != 2) return 0;

	int player = argv[1][0] - '1';
	int otherplayer = 2 - player + 1;
	char boardStr[50];

	scanf("%s",boardStr);
	morphInit(&m, boardStr, player);
	morphGenMoves(&m, &h, -1, player);
	if(!morphHasBlackKing(&m)){
		printf("1");
		return 0;
	}
	if(!morphHasWhiteKing(&m)){
		printf("2");
		return 0;
	}
	if(!h.count){
		printf("%i", otherplayer);
		return 0;
	}
	printf("0");
	return 0;
}
