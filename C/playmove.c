#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "heap.h"
#include "morph.h"

#define	MAX(X,Y) ( (X) > (Y) ? (X) : (Y) )
#define	MIN(X,Y) ( (X) < (Y) ? (X) : (Y) )

void printHeap(heap* h){
	for(int i = 0; i < h->count; i++)
		printf("%i ", h->key[i]);
	printf("\n");
}

clock_t limit;
heap moves[100];
morph m;

int miniMaxFunc(int eval, int depth, int maxDepth, int isMax, int alpha, int beta){
	if(clock() > limit) return -1; //Ran out of time
	int bestScore, bestMove, k, v, score;
	if(isMax) bestScore = LOSE; else bestScore = WIN;

	morphGenMoves(&m, &moves[depth], isMax);
	if(moves[depth].count == 0) return bestScore * -1;
	if(	(m.curPlayer == 0 && !morphHasBlackKing(&m)) ||
		(m.curPlayer == 1 && !morphHasWhiteKing(&m)))
		return bestScore;
	if(depth > maxDepth)
		return eval;

	while(moves[depth].count){
		if(isMax) heapRemoveMax(&moves[depth],&k,&v,0);
		else heapRemoveMin(&moves[depth],&k,&v,0);
		morphPlayMove(&m, v);
		score = miniMaxFunc(k,depth + 1,maxDepth, !isMax, alpha, beta);
		morphUndoMove(&m);
		if(isMax){
			bestScore = MAX(bestScore, score);
			alpha = MAX(alpha, bestScore);
		}else{
			bestScore = MIN(bestScore, score);
			beta = MIN(beta, bestScore);
		}
		if(beta <= alpha) break;
	}
	return bestScore;
}

int miniMax(double timelimit){
	printf("Hi?\n");
	limit = (clock_t)(clock() + timelimit * CLOCKS_PER_SEC);
	int globalBestMove = -1;
	int bestMove = -1;
	int bestScore = LOSE;
	int maxDepth = 1;
	int k,v,score;
	while(1) {
		printf("%i %i\n", maxDepth, clock());
		morphGenMoves(&m, &moves[0], 1);
		if(globalBestMove != -1){ //Move the best move to the front
			for(int i = 0; i < moves[0].count; i++){
				if(moves[0].value[i] == bestMove){
					heapRemoveMax(&moves[0],&k,&v,i);
					heapInsertMax(&moves[0],WIN-1,globalBestMove);
				}
			}
		}
		while(moves[0].count) {
			heapRemoveMax(&moves[0],&k,&v,0);
			morphPlayMove(&m, v);
			score = miniMaxFunc(k, 1, maxDepth, 0,  LOSE - 1, WIN + 1);
			morphUndoMove(&m);
			if(score == WIN) return v; //Winning move! Yay!
			if(clock() > limit) break; //Ran out of time
			if(score > bestScore){
				bestScore = score;
				bestMove = v;
			}
		}
		if(clock() <= limit){
			//Still time left
			char move[5];
			morphMoveString(move, bestMove, 0);
			printf("%i - %f - %i %s", maxDepth, (limit - clock()) / (double)CLOCKS_PER_SEC, bestScore, move);
			globalBestMove = bestMove;
			maxDepth++;
		} else {
			break;
		}
	}
	return globalBestMove;
}

int main(int argc, char* argv[]) {
	if(argc != 3) return 0;

	int player = argv[1][0] - '1';
	printf("%i\n", player);
	char* evalFile = argv[2];
	char moveStr[5];
	char moveStrRev[5];
	int k,v;

	morphLoadWeights(evalFile);
	morphInit(&m, NULL, player);
	morphPrint(&m);

	miniMax(5);

	return 0;
}
