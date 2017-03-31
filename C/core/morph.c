#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "heap.h"
#include "morph.h"
#include "textcolor.h"

/*Piece indicies*/
/*Bit 4 used to determine ownership*/
#define SPACE		0
#define B_KING		1
#define	B_KNIGHT	2
#define B_BISHOP	3
#define	B_ROOK		4
#define B_PAWN		5
#define W_KING		9
#define	W_KNIGHT	10
#define W_BISHOP	11
#define	W_ROOK		12
#define W_PAWN		13

/*Piece representation*/
#define SPACE_CHR	'-'
#define B_KING_CHR	'K'
#define	B_KNIGHT_CHR	'N'
#define B_BISHOP_CHR	'B'
#define	B_ROOK_CHR	'R'
#define B_PAWN_CHR	'P'
#define W_KING_CHR	'k'
#define	W_KNIGHT_CHR	'n'
#define W_BISHOP_CHR	'b'
#define	W_ROOK_CHR	'r'
#define W_PAWN_CHR	'p'

int evalWeights[2][14][8][6];

void morphInit(morph* ret, char* boardState, int player) {
	ret->turn = 0;
	ret->curPlayer = player;

	if(!boardState) boardState = "-K----NBRRBN--PP----------------pp--nbrrbn----k-";
	for(int i = 0; i < 8 * 6; i++){
		switch(boardState[i]){
			case SPACE_CHR: ret->board[0][i/6][i%6] = SPACE; break;
			case B_KING_CHR: ret->board[0][i/6][i%6] = B_KING; break;
			case B_KNIGHT_CHR: ret->board[0][i/6][i%6] = B_KNIGHT; break;
			case B_BISHOP_CHR: ret->board[0][i/6][i%6] = B_BISHOP; break;
			case B_ROOK_CHR: ret->board[0][i/6][i%6] = B_ROOK; break;
			case B_PAWN_CHR: ret->board[0][i/6][i%6] = B_PAWN; break;
			case W_KING_CHR: ret->board[0][i/6][i%6] = W_KING; break;
			case W_KNIGHT_CHR: ret->board[0][i/6][i%6] = W_KNIGHT; break;
			case W_BISHOP_CHR: ret->board[0][i/6][i%6] = W_BISHOP; break;
			case W_ROOK_CHR: ret->board[0][i/6][i%6] = W_ROOK; break;
			case W_PAWN_CHR: ret->board[0][i/6][i%6] = W_PAWN; break;
		}
	}
}

void morphPrint(morph* m) {
	int bg, fg;
	for(int j = 0; j < 8; j++) {
		textcolor(RESET,WHITE,BLACK);
		printf("%c", 8 - j + '0');
		for(int i = 0; i < 6; i++) {
			bg = ((j + i % 2) % 2) ? BLACK : YELLOW;
			fg = m->board[m->turn][j][i] & 8 ? WHITE : CYAN;
			textcolor(BRIGHT,fg,bg);
			switch(m->board[m->turn][j][i]){
				case SPACE: printf(" "); break;
				case B_KING: printf("%c",B_KING_CHR); break;
				case B_KNIGHT: printf("%c",B_KNIGHT_CHR); break;
				case B_BISHOP: printf("%c",B_BISHOP_CHR); break;
				case B_ROOK: printf("%c",B_ROOK_CHR); break;
				case B_PAWN: printf("%c",B_PAWN_CHR); break;
				case W_KING: printf("%c",W_KING_CHR); break;
				case W_KNIGHT: printf("%c",W_KNIGHT_CHR); break;
				case W_BISHOP: printf("%c",W_BISHOP_CHR); break;
				case W_ROOK: printf("%c",W_ROOK_CHR); break;
				case W_PAWN: printf("%c",W_PAWN_CHR); break;
			}
		}
		textcolor(RESET,WHITE,BLACK);
		printf("\n");
	}
	printf(" ABCDEF\n");
}

void morphPrintString(morph* m) {
	for(int j = 0; j < 8; j++) {
		for(int i = 0; i < 6; i++) {
			switch(m->board[m->turn][j][i]){
				case SPACE: printf("%c",SPACE_CHR); break;
				case B_KING: printf("%c",B_KING_CHR); break;
				case B_KNIGHT: printf("%c",B_KNIGHT_CHR); break;
				case B_BISHOP: printf("%c",B_BISHOP_CHR); break;
				case B_ROOK: printf("%c",B_ROOK_CHR); break;
				case B_PAWN: printf("%c",B_PAWN_CHR); break;
				case W_KING: printf("%c",W_KING_CHR); break;
				case W_KNIGHT: printf("%c",W_KNIGHT_CHR); break;
				case W_BISHOP: printf("%c",W_BISHOP_CHR); break;
				case W_ROOK: printf("%c",W_ROOK_CHR); break;
				case W_PAWN: printf("%c",W_PAWN_CHR); break;
			}
		}
	}
}

int hexToInt(char* hex, int count){
	int ret = 0;
	for(int i = 0; i < count; i++){
		if(hex[i] >= '0' && hex[i] <= '9')
			ret |= hex[i] - '0';
		else if(hex[i] >= 'A' && hex[i] <= 'F')
			ret |= hex[i] - 'A' + 10;
		if(i < count - 1)
			ret <<= 4;
	}
	return ret;
}

void morphLoadWeights(char* file) {
	char buffer[2121];
	FILE* fp;
	fp = fopen(file, "r");
	if(!fp) return;
	fgets(buffer, 2121, fp);

	int ind = 8; //First 8 letters are the generation
	int pieceInd;

	for(int piece = 0; piece < 11; piece++){
		switch(piece){
			case 0: pieceInd = SPACE; break;
			case 1: pieceInd = B_KING; break;
			case 2: pieceInd = B_KNIGHT; break;
			case 3: pieceInd = B_BISHOP; break;
			case 4: pieceInd = B_ROOK; break;
			case 5: pieceInd = B_PAWN; break;
			case 6: pieceInd = W_KING; break;
			case 7: pieceInd = W_KNIGHT; break;
			case 8: pieceInd = W_BISHOP; break;
			case 9: pieceInd = W_ROOK; break;
			case 10: pieceInd = W_PAWN; break;
		}
		for(int j = 0; j < 8; j++){
			for(int i = 0; i < 6; i++){
				int val = hexToInt(buffer + ind, 4);
					evalWeights[0][pieceInd][j][i] = val;
					//Player two needs to flip and mirror the positions
					//as well as flip the color of the index
					if(pieceInd == SPACE) // Black space don't modify
						evalWeights[1][pieceInd][7 - j][5 - i] = val;
					else if(pieceInd & 8) // White piece
						evalWeights[1][pieceInd & (~8)][7 - j][5 - i] = val;
					else //Black piece
						evalWeights[1][pieceInd | 8][7 - j][5 - i] = val;
						
				ind += 4;
			}
		}
	}
}

int morphEval(morph* m, int ep) {
	int ret = 0;
	for(int j = 0; j < 8; j++)
		for(int i = 0; i < 6; i++)
			ret += evalWeights[ep][m->board[m->turn][j][i]][j][i];
	return ret;
}

int morphHasWhiteKing(morph* m) {
	for(int i = 0; i < 6; i++)
		if(m->board[m->turn][7][i] == W_KING)
			return -1;
	return 0;
}

int morphHasBlackKing(morph* m) {
	for(int i = 0; i < 6; i++)
		if(m->board[m->turn][0][i] == B_KING)
			return -1;
	return 0;
}

void morphPlayMove(morph* m, int move) {
	//Set up new board
	memcpy(&m->board[m->turn+1][0][0], &m->board[m->turn][0][0], 6*8*sizeof(int));
	m->turn++;
	m->curPlayer = m->curPlayer ? 0 : 1;

	//Unpack move
	int x1 = (move & 0b000000000111) >> 0;
	int y1 = (move & 0b000000111000) >> 3;
	int x2 = (move & 0b000111000000) >> 6;
	int y2 = (move & 0b111000000000) >> 9;

	int piece = m->board[m->turn][y1][x1];
	
	//Figure out changes
	switch(piece) {
		case W_BISHOP: piece = W_KNIGHT; break;
		case W_KNIGHT: piece = W_ROOK; break;
		case W_ROOK: piece = W_BISHOP; break;
		case B_BISHOP: piece = B_KNIGHT; break;
		case B_KNIGHT: piece = B_ROOK; break;
		case B_ROOK: piece = B_BISHOP; break;
	}

	//Remove old piece
	m->board[m->turn][y1][x1] = SPACE;

	//Place new piece
	m->board[m->turn][y2][x2] = piece;
}

void morphUndoMove(morph* m) {
	m->turn--;
	m->curPlayer = m->curPlayer ? 0 : 1;
}

void morphAddMove(morph* m, heap* h, int max, int move, int ep) {
	if(max == -1){
		heapInsertMax(h, 0, move);
	} else {
		morphPlayMove(m, move);
		int key = morphEval(m, ep);
		morphUndoMove(m);
		if(max) heapInsertMax(h, key, move);
		else heapInsertMin(h, key, move);
	}
}

void morphMove(morph* m, heap* h, int max, int x1, int y1, int x2, int y2, int ep) {
	if(CANMOVE(m,x2,y2)) 
		morphAddMove(m,h,max,PACKMOVE(x1,y1,x2,y2), ep);
}

void morphAttack(morph* m, heap* h, int max, int x1, int y1, int x2, int y2, int ep) {
	if(CANATTACK(m,x1,y1,x2,y2))
		morphAddMove(m,h,max,PACKMOVE(x1,y1,x2,y2), ep);
}

void morphMoveOrAttack(morph* m, heap* h, int max, int x1, int y1, int x2, int y2, int ep) {
	if(CANMOVEORATTACK(m,x1,y1,x2,y2))
		morphAddMove(m,h,max,PACKMOVE(x1,y1,x2,y2), ep);
}

void morphTrace(morph* m, heap* h, int max, int x, int y, int dx, int dy, int move, int attack, int ep) {
	int sp = OWNERSHIP(m,x,y);
	int cx = x + dx;
	int cy = y + dy;
	while(ONBOARD(cx,cy)) {
		int cp = OWNERSHIP(m,cx,cy);
		if(sp == cp) break;
		else if(move && CANMOVE(m,cx,cy))
			morphAddMove(m,h,max,PACKMOVE(x,y,cx,cy), ep);
		else if(attack && CANATTACK(m,x,y,cx,cy)){
			morphAddMove(m,h,max,PACKMOVE(x,y,cx,cy), ep);
			break;
		}
		cx += dx;
		cy += dy;
	}
}

void morphGenMoves(morph* m, heap* h, int max, int ep) {
	int piece;

	//Clear the heap if for some reason it wasn't empty
	heapClear(h);

	//Exit if the player is missing their king since they can't
	//move anymore
	if(m->curPlayer == 0 && !morphHasWhiteKing(m)) return;
	if(m->curPlayer == 1 && !morphHasBlackKing(m)) return;

	//Loop over the pieces
	for(int j = 0; j < 8; j++){
		for(int i = 0; i < 6; i++){
			piece = m->board[m->turn][j][i];
			//Skip blank spaces or pieces that don't belong to the player
			if(	!piece ||
				(m->curPlayer == 0 && !(piece & 8)) ||
				(m->curPlayer == 1 && (piece & 8)))
				continue;
			switch(piece) {
				case W_PAWN:
					morphMove(m,h,max,i,j,i,j-1,ep);
					morphAttack(m,h,max,i,j,i-1,j-1,ep);
					morphAttack(m,h,max,i,j,i+1,j-1,ep);
					break;
				case B_PAWN:
					morphMove(m,h,max,i,j,i,j+1,ep);
					morphAttack(m,h,max,i,j,i-1,j+1,ep);
					morphAttack(m,h,max,i,j,i+1,j+1,ep);
					break;
				case W_KING:
					morphMoveOrAttack(m,h,max,i,j,i-1,j,ep);
					morphAttack(m,h,max,i,j,i+1,j,ep);
					break;
				case B_KING:
					morphMoveOrAttack(m,h,max,i,j,i+1,j,ep);
					morphAttack(m,h,max,i,j,i-1,j,ep);
					break;
				case W_KNIGHT:
					morphMoveOrAttack(m,h,max,i,j,i-1,j-2,ep);
					morphAttack(m,h,max,i,j,i-1,j+2,ep);
					morphMoveOrAttack(m,h,max,i,j,i+1,j-2,ep);
					morphAttack(m,h,max,i,j,i+1,j+2,ep);
					morphMoveOrAttack(m,h,max,i,j,i-2,j-1,ep);
					morphAttack(m,h,max,i,j,i-2,j+1,ep);
					morphMoveOrAttack(m,h,max,i,j,i+2,j-1,ep);
					morphAttack(m,h,max,i,j,i+2,j+1,ep);
					break;
				case B_KNIGHT:
					morphAttack(m,h,max,i,j,i-1,j-2,ep);
					morphMoveOrAttack(m,h,max,i,j,i-1,j+2,ep);
					morphAttack(m,h,max,i,j,i+1,j-2,ep);
					morphMoveOrAttack(m,h,max,i,j,i+1,j+2,ep);
					morphAttack(m,h,max,i,j,i-2,j-1,ep);
					morphMoveOrAttack(m,h,max,i,j,i-2,j+1,ep);
					morphAttack(m,h,max,i,j,i+2,j-1,ep);
					morphMoveOrAttack(m,h,max,i,j,i+2,j+1,ep);
					break;
				case W_BISHOP:
					morphTrace(m,h,max,i,j,-1,-1,1,1,ep);
					morphTrace(m,h,max,i,j,1,-1,1,1,ep);
					morphTrace(m,h,max,i,j,-1,1,0,1,ep);
					morphTrace(m,h,max,i,j,1,1,0,1,ep);
					break;
				case B_BISHOP:
					morphTrace(m,h,max,i,j,-1,1,1,1,ep);
					morphTrace(m,h,max,i,j,1,1,1,1,ep);
					morphTrace(m,h,max,i,j,-1,-1,0,1,ep);
					morphTrace(m,h,max,i,j,1,-1,0,1,ep);
					break;
				case W_ROOK:
					morphTrace(m,h,max,i,j,0,-1,1,1,ep);
					morphTrace(m,h,max,i,j,-1,0,1,1,ep);
					morphTrace(m,h,max,i,j,1,0,1,1,ep);
					morphTrace(m,h,max,i,j,0,1,0,1,ep);
					break;
				case B_ROOK:
					morphTrace(m,h,max,i,j,0,1,1,1,ep);
					morphTrace(m,h,max,i,j,-1,0,1,1,ep);
					morphTrace(m,h,max,i,j,1,0,1,1,ep);
					morphTrace(m,h,max,i,j,0,-1,0,1,ep);
					break;
			}
		}
	}
}

void morphMoveString(char* buffer, int move, int reverse){
	int x1 = (move & 0b000000000111) >> 0;
	int y1 = (move & 0b000000111000) >> 3;
	int x2 = (move & 0b000111000000) >> 6;
	int y2 = (move & 0b111000000000) >> 9;

	if(!reverse) {
		y1 = 7 - y1;
		y2 = 7 - y2;
	} else {
		x1 = 5 - x1;
		x2 = 5 - x2;
	}

	buffer[0] = x1 + 'A';
	buffer[1] = y1 + '1';
	buffer[2] = x2 + 'A';
	buffer[3] = y2 + '1';
	buffer[4] = 0;
}
