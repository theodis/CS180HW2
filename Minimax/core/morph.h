#ifndef _MORPH
#define _MORPH

#define PACKMOVE(x1,y1,x2,y2)		( (x1 << 0) | ( y1 << 3) | (x2 << 6) | (y2 << 9) )
#define OWNERSHIP(m,x,y)		( (m)->board[(m)->turn][(y)][(x)] ? (((m)->board[(m)->turn][(y)][(x)] & 8 ) ? 0 : 1) : -1 )
#define ONBOARD(x,y)			( (x) >= 0 && (x) < 6 && (y) >= 0 && (y) < 8 )

#define CANMOVE(m,x,y)			( ONBOARD(x,y) && !(m)->board[(m)->turn][(y)][(x)] )
#define CANATTACK(m,x1,y1,x2,y2)	( ONBOARD(x2,y2) && (m)->board[(m)->turn][(y2)][(x2)] && OWNERSHIP(m,x1,y1) != OWNERSHIP(m,x2,y2) )
#define CANMOVEORATTACK(m,x1,y1,x2,y2)	( ONBOARD(x2,y2) && OWNERSHIP(m,x1,y1) != OWNERSHIP(m,x2,y2) )

#define MAX_MOVES	100
#define WIN	 1000000000
#define LOSE	-1000000000

typedef struct morph {
	int curPlayer;
	int board[MAX_MOVES][8][6];
	int turn;
} morph;


void morphInit(morph* m, char* boardState, int player);
void morphPrint(morph* board);
void morphPrintString(morph* m);
void morphLoadWeights(char* file);
int morphEval(morph* m, int ep);
int morphHasBlackKing(morph* m);
int morphHasWhiteKing(morph* m);
void morphPlayMove(morph* m, int move);
void morphUndoMove(morph* m);
void morphGenMoves(morph* m, heap* h, int max, int ep);
void morphMoveString(char* buffer, int move, int reverse);
int morphMoveStringToMove(char* moveStr);

#endif
