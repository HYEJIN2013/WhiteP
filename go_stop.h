#pragma warning(disable:4996)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


#define DECK 48 //DECK라는 문자를 48이라는 매크로 상수로 정의한다.
#define WIN 3 //3점 이상이면 고나 스톱을 외칠수 있다.

typedef struct card{ //이 고스톱 소스에서 다룰 모든 카드의 종류
	unsigned month; //각 카드가 의미하는 월 
	char cardname[10]; //카드의 이름 
	char type; //'G':광,'D':띠,'A':열끗,'P':피
}Card; //카드들에 대한 모든 종류가 들어있다.

typedef struct node{ 
	struct node *prev; //prev 노드 
	Card data; //카드의 정보가 들어있음 
	struct node *next; //next 노드 
}Node; //플레이어가 각자 가지고 있는 패 1장

typedef struct list{ 
    Node* head;
	Node* tail;
	Node* curr;
}List; //플레이어 리스트에 대한 헤드와 테일 노드를 만들어 안정적인 구조가 되도록 한다

typedef struct score{
int CheongDan; //청단 
int HongDan; //홍단 
int ChoDan; //초단 
int Pee; //피 
int Gwang; //광 
int Five_End; //오끝 
int Ten_End; //열끝 
int Go_stop; //고, 스톱  
int Pee_BakB;//피박
int Pee_BakC; //피박
int Gwang_BakB;//광박
int Gwang_BakC; //광박
int Go_Dori; //고도리
int Gook_Jin; //국진
}Score; //점수 계산에 있어 필요한 모든 경우를 나열한 구조체



void Create_All_Lists(List*,List*,List*,List*,List*,List*,List*,List*); //모든 카드들을 저장할 노드들을 생성한다.
void Create(List* ,int); //리스트 하나를 생성한다.
void Destroy(List*);//리스트 하나를 전부 삭제한다.
void Destroy_All(List*,List*,List*,List*,List*,List*,List*,List*);//모든 리스트들을 전부 삭제한다.



void SetDeck(Card*, List*); //카드뭉치(덱)를 섞는 함수
List* Deck_AddNode(List*,Card); //카드 덱에 대한 리스트들이 순서대로 형성되지만 그 내부의 데이터는 1부터 48까지범위이며 무작위이다.
void Open_Field(List*,List*); //처음에 깔리는 패들의 리스트
void SetOn_Field(List*,List*); //먹고 뽑았을 때에 따라 깔린 패에 있는 리스트들은 계속 변화한다.
void HavingCard(List*,List*); //각 플레이어는 카드를 7장씩 가진다.
void GameReady(Card*,List*,List*,List*,List*,List*); //게임을 시작하기 위한 준비를 한다.
int GetListNum(List*); //리스트 갯수 리턴
Node* Draw_From_Deck(List*); //덱에서 카드 한 장을 드로우한다.

void PlayerA(List*,List*); //플레이어 A의 명령
void PlayerB(List*,List*); //플레이어 B의 명령
void PlayerC(List*,List*); //플레이어 C의 명령
void Display_Player(List*); //플레이어가 들고있는 패의 현재 상황을 보여준다.
void Display_OpenCard(List*); //현재 깔린 패들이 무엇이 있는지 보여준다.
void Display_SaveCard(List*);//현재 플레이어가 먹은 패의 현재 상황을 보여준다.
void Display_DeckCard(List*);//현재 덱의 상태
void Display_Help(); //단축키 명령모음
void Display_Money(int,int,int); //현재의 돈 액수 보여주기
int Display_Score(int); //현재 플레이어의 점수



Node* Search_And_PayPlayerCard(List*,char); //현재 플레이어가 카드 하나를 택했을때 그 카드가 패에 있는지 검사한다. 그리고 그 카드를 선택하여 낸다.
void Search_And_TakeOpenCard(List*,List*,List*,List*,Node*,Node*); //현재 깔린 카드들 중에서 가져갈때 그 카드가 깔린 패에 존재하는지 검사한다 그리고 일치하는게 있으면 가져간다.
                                                                               // 그리고 먹은 카드들을 플레이어가 먹은 카드들 리스트에 추가한다.
 char Command(); //사용자의 명령을 받는다.

 List* StealPee(List*,List*,List*);//상대방 깔린패 리스트에서 피를 뺏어온다.
 int Shake(List*); //플레이어의 패에 같은 월의 카드가 3장 있으면 흔들기를 한다. 이 흔들기를 하고나면 승리 시에 2배의 점수를 얻는다.
 int ChongTong(List*); //각 플레이어의 패를 비교해서 만약 같은 달의 화투가 4장있으면 10점을 얻고 그 플레이어가 승리한다.
 int Nagari(List*,List*,int,int,int); //나가리 
 
 int Score_Calculate(List*,List*,List*,Score*);//점수 계산
 int Bak_Calculate(List*,List*,int,int,int,int,int,int,Score*);//박 계산
 
 
 int Money_Calculate_Get(int,int);//승자 돈 계산
 int Money_Calculate_Minus(int,int);//패자 돈 계산
 int Money_Calculate_Minus2(int,int);//패자 돈 계산

 int Save(Card*,Card*,Card*,Card*,Card*,Card*,Card*,Card*,List*,List*,List*,List*,List*,List*,List*,List*,int*,int*,int*,int*,int*,int*); //저장
 void Load(Card*,Card*,Card*,Card*,Card*,Card*,Card*,Card*,List*,List*,List*,List*,List*,List*,List*,List*,int*,int*,int*,int*,int*,int,int,int,int*); //로드