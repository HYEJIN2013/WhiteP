#include <windows.h>
#include "resource.h"

enum STATE {NONE,BLACK,WHITE};
STATE m_Board[19][19];         //바둑판에 돌이 놓여진 상태 

typedef struct LINKSTONE
{
	int x;                     //연결된 돌들의 좌표
	int y;
}LINKSTONE;
LINKSTONE link[361];           //연결된 돌들을 저장
LINKSTONE queue[361];          //연결된 돌들을 임시로 저장 위한 큐

typedef struct PAE
{
	int x;                     //패의 좌표
	int y;
	bool b_pae;             //패의 상태
}PAE;
PAE pae;                   //패의 정보

HWND hwnd;
HINSTANCE g_hInst;             //LoadBitmap의 인자를 위한 변수
PAINTSTRUCT ps;                //BeginPaint 와 EndPaint를 위한 변수 
HDC hdc, MemDC;                //그리기를 위한 변수
HBITMAP MyBitmap, OldBitmap;   //Bitmap을 위한 변수

int rear_link;				   //링크에 수록할 부분
int front_que;				   //큐에서 추출할 부분
int rear_que;				   //큐의 수록할 부분
int live;					   //연결된 돌의 생사여부
int Chk_live;				   //놓여질 자리에 대한 생사여부
bool m_WhTurn=FALSE;		   //플레이어의 상태
int ax, ay;					   //바둑판 위의 돌의위치

//함수의 선언
void Draw(HDC pDC, int x, int y, STATE dol);  //돌을 그려줄 함수
void CheckLink(int _x, int _y, STATE dol);  //돌의 연결 여부에 따라서 Insert_que함수를 호출
void Insert_que(int _x, int _y);  //큐에 수록하는 함수
void Insert_link();  //큐에서 추출하여 링크에 수록하는 함수
void CheckLive(int _x, int _y);  //링크에 수록된 돌들의 생사여부 
void RemoveDead();  //CheckLive함수에서 체크된 live변수값에 따라 돌을 삭제해줌
bool AllCheck(int user_x, int user_y, int _x, int _y, STATE dol);  //놓여질 자리에 상황 체크 등
void DrawBoard();  //바둑판과 바둑알을 그려준다
void CheckPae();  //패 인지 체크한다 

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
char AppName[] = "바둑";
g_hInst = hInstance;
MSG msg;

WNDCLASSEX wc;

wc.cbClsExtra = 0;
wc.cbSize     = sizeof(wc);
wc.cbWndExtra = 0;
wc.hbrBackground = (HBRUSH)GetStockObject(LTGRAY_BRUSH);
wc.hCursor = LoadCursor(NULL, IDC_ARROW);
wc.hIcon = LoadIcon(hInstance, MAKEINTRESOURCE(IDC_ICON));
wc.hIconSm = LoadIcon(hInstance, MAKEINTRESOURCE(IDC_ICON));
wc.hInstance = hInstance;
wc.lpfnWndProc = WndProc;
wc.lpszClassName = AppName;
wc.lpszMenuName = MAKEINTRESOURCE(IDR_MENU1);
wc.style = CS_HREDRAW | CS_VREDRAW;

RegisterClassEx(&wc);

hwnd = CreateWindow(AppName, AppName, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 580, 620, NULL, NULL, hInstance, NULL);

ShowWindow(hwnd, nShowCmd);
UpdateWindow(hwnd);

while(GetMessage(&msg, NULL, 0, 0))
{
	TranslateMessage(&msg);
	DispatchMessage(&msg);
}
return msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
	POINT point;

	switch(msg)
	{
	case WM_CREATE:  // 게임을 초기화 한다
		{
			int x, y;

			m_WhTurn = false;
			pae.b_pae = false;
			for(x=0; x<=18; x++)
				for(y=0; y<=18; y++)
				{
					m_Board[x][y] = NONE;
				}
			InvalidateRect(hwnd, NULL, TRUE);		
		}
		break;

	case WM_DESTROY:
		{
			PostQuitMessage(0);
		}
		break;

	case WM_LBUTTONDOWN:
		{
			//마우스의 위치를 읽어온다
			point.x = LOWORD(lParam);
			point.y = HIWORD(lParam);

			ax = point.x / 30;
			ay = point.y / 30;

			//바둑돌 이외의 장소에 놓여질 때
			if((ax<0) || (ax>=19) || (ay<0) || (ay>=19))
			{
				return 0;
			}
			//이미 있는 자리에 놓여질 때
			if(m_Board[ax][ay] != NONE)
			{
				return 0;
			}	

			//패의 상태 확인
			if(pae.b_pae==true)
			{
				if((pae.x==ax) && (pae.y==ay))
					return 0;
				else if ((pae.x!=ax) || (pae.y!=ay))
					pae.b_pae = false;
			}
			
			//--------------------------------------------------------------//
			Chk_live = 0;
			if (m_WhTurn==false)
			{
				Chk_live += AllCheck(ax-1, ay, ax, ay, BLACK);
				Chk_live += AllCheck(ax+1, ay, ax, ay, BLACK);
				Chk_live += AllCheck(ax, ay-1, ax, ay, BLACK);
				Chk_live += AllCheck(ax, ay+1, ax, ay, BLACK);
			}
			else
			{
				Chk_live += AllCheck(ax-1, ay, ax, ay, WHITE);
				Chk_live += AllCheck(ax+1, ay, ax, ay, WHITE);
				Chk_live += AllCheck(ax, ay-1, ax, ay, WHITE);
				Chk_live += AllCheck(ax, ay+1, ax, ay, WHITE);
			}
			if (Chk_live==0)
			{
				break;
			}
			//--------------------------------------------------------------//

			//놓을수 있는자리가 확인 되었으면 돌을 놓고 턴을 바꿈
			m_Board[ax][ay] = (m_WhTurn ? WHITE : BLACK);
			m_WhTurn = !m_WhTurn;
			//바둑알을 그려준다
			hdc = GetDC(hwnd);
			Draw(hdc, ax, ay, m_Board[ax][ay]);
			ReleaseDC(hwnd, hdc);

			//--------------------------------------------------------------//
		}
		break;

	case WM_COMMAND:
		{
			switch(LOWORD(wParam))
			{
			case ID_FILE_NEWGAME:
				{
					SendMessage(hwnd, WM_CREATE, wParam, lParam);
				}
				break;
			case ID_FILE_EXITGAME:
				{
					SendMessage(hwnd, WM_DESTROY, wParam, lParam);
				}
				break;
			}
		}
		break;

	case WM_PAINT:
		{
			DrawBoard();
		}
		break;
	}
	return DefWindowProc(hwnd, msg, wParam, lParam);
}

//바둑알을 그려준다
void Draw(HDC dc, int x, int y, STATE dol)
{
	if(dol == BLACK)
		SelectObject(dc, GetStockObject(BLACK_BRUSH));
	else
		SelectObject(dc, GetStockObject(WHITE_BRUSH));
	if(dol != NONE)
		Ellipse(dc, x*30+2, y*30+2, x*30+28, y*30+28);
}

void CheckLink(int _x, int _y, STATE dol)
{
	//상하좌우 연결된 돌이 있으면 큐에 수록하는 함수를 호출
	if ((_x-1>=0) && (m_Board[_x-1][_y]==dol))
	{
		Insert_que(_x-1, _y);
	}
	if ((_x+1<=18) && (m_Board[_x+1][_y]==dol))
	{
		Insert_que(_x+1, _y);
	}
	if ((_y-1>=0) && (m_Board[_x][_y-1]==dol))
	{
		Insert_que(_x, _y-1);
	}
	if ((_y+1<=18) && (m_Board[_x][_y+1]==dol))
	{
		Insert_que(_x, _y+1);
	}
}

void Insert_que(int _x, int _y)
{
	//이미 수록된 큐와 중복 되었는지 체크
	for (int i=0; i<rear_que; i++)
	{
		if ((queue[i].x==_x) && (queue[i].y==_y))
		{
			return;
		}
	}
	//중복되지 않으면 큐에 수록 
	queue[rear_que].x = _x;
	queue[rear_que].y = _y;
	++rear_que;
}

void Insert_link()
{
	//이미 수록된 링크와 중복 되었는지 체크
	for (int i=0; i<rear_link; i++)
	{
		if ((link[i].x==queue[front_que].x) && (link[i].y==queue[front_que].y))
		{
			return;
		}
	}
	//중복되지 않으면 큐에 첫번째 값을 링크에 수록
	link[rear_link].x = queue[front_que].x;
	link[rear_link].y = queue[front_que].y;
	++rear_link;
	++front_que;
}	

void CheckLive(int _x, int _y)
{
	live = 0;
	for (int i=0; i<rear_link; i++)
	{
		if ((m_Board[link[i].x-1][link[i].y]==NONE) && (link[i].x-1>=0))
		{
			if ((link[i].x-1==_x) && (link[i].y==_y))
			{   //놓여질 자리는 계산하지 않는다
			}
			else
			{
				++live; 
			}           
		}
		if ((m_Board[link[i].x+1][link[i].y]==NONE) && (link[i].x+1<=18))
		{
			if ((link[i].x+1==_x) && (link[i].y==_y))
			{
			}
			else
			{
				++live;
			}
		}
		if ((m_Board[link[i].x][link[i].y-1]==NONE) && (link[i].y-1>=0))
		{
			if ((link[i].x==_x) && (link[i].y-1==_y))
			{
			}
			else
			{
				++live;
			}
		}
		if ((m_Board[link[i].x][link[i].y+1]==NONE) && (link[i].y+1<=18))
		{
			if ((link[i].x==_x) && (link[i].y+1==_y))
			{
			}
			else
			{
				++live;
			}
		}
	}
}

void RemoveDead()
{
	if (live==0)
	{
		CheckPae();  //패 인지 체크한다
		for (int i=0; i<rear_link; i++)
		{
			//죽은돌을 설정한다
			m_Board[(link[i].x)][(link[i].y)] = NONE;
			//무효화 영역을 정하고 새로 그린다
			RECT rect;
			SetRect(&rect, link[i].x*30, link[i].y*30, link[i].x*30+30, link[i].y*30+30);
			InvalidateRect(hwnd, &rect, TRUE);
		}
	}
}

bool AllCheck(int user_x, int user_y, int _x, int _y, STATE dol)
{
	if ((m_Board[user_x][user_y]!=NONE) && (user_x>=0) && (user_x<=18) && (user_y>=0) && (user_y<=18))
	{
		rear_link = 0;
		front_que = 0;
		rear_que = 0;
		Insert_que(user_x, user_y);
		while (front_que!=rear_que)
		{
			CheckLink(queue[front_que].x, queue[front_que].y, m_Board[user_x][user_y]);
			Insert_link();
		}
		CheckLive(_x, _y);
		if ((m_Board[user_x][user_y]!=dol) && (live==0))
		{
			RemoveDead();
			return true;
		}
		else if ((m_Board[user_x][user_y]==dol) && (live>0)) 
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	else if ((m_Board[user_x][user_y]==NONE) && (user_x>=0) && (user_x<=18) && (user_y>=0) && (user_y<=18))
	{
		return true;
	}
	else
	{
		return false;
	}
}

void DrawBoard()
{
	//--------------------------------------------------------------//
	hdc = BeginPaint(hwnd, &ps);
	MemDC = CreateCompatibleDC(hdc);
	MyBitmap = LoadBitmap(g_hInst, MAKEINTRESOURCE(IDB_BITMAP1));
	OldBitmap = (HBITMAP) SelectObject (MemDC, MyBitmap);
	BitBlt(hdc, 0, 0, 570, 570, MemDC, 0, 0, SRCCOPY);
	SelectObject(MemDC, OldBitmap);
	DeleteObject(MyBitmap);
	DeleteDC(MemDC);
	EndPaint(hwnd, &ps);
	//--------------------------------------------------------------//
	
	//바둑판을 그려준다
	hdc = GetDC(hwnd);
	int x,y;
	for(x=0; x<19; x++)
	{
		MoveToEx(hdc, 15 ,15+x*30, NULL);
		LineTo(hdc, 555, 15+x*30);
	}
	for(x=0; x<19; x++)
	{
		MoveToEx(hdc, 15+x*30, 15, NULL);
		LineTo(hdc, 15+x*30, 555);
	}
	//화점을 그려준다
	SelectObject(hdc, GetStockObject(BLACK_BRUSH));
	Ellipse(hdc, 101, 101, 110, 110);
	Ellipse(hdc, 461, 101, 470, 110);
	Ellipse(hdc, 101, 461, 110, 470);
	Ellipse(hdc, 461, 461, 470, 470);
	Ellipse(hdc, 281, 281, 290, 290);
	Ellipse(hdc, 281, 101, 290, 110);
	Ellipse(hdc, 101, 281, 110, 290);
	Ellipse(hdc, 461, 281, 470, 290);
	Ellipse(hdc, 281, 461, 290, 470);
	//바둑알을 다시 그려준다
	for(x=0; x<19; x++)
		for(y=0; y<19; y++)
		{
			Draw(hdc, x, y, m_Board[x][y]);
		}
	ReleaseDC(hwnd, hdc);
}

void CheckPae()
{
	STATE dol;
	int tmp_live=0;
	dol = (m_WhTurn ? BLACK : WHITE); //현재 플레이어 상태와 반대
	if(rear_link==1)
	{
		//놓여질 자리의 상하좌우 체크
		if((ax-1<0) || (m_Board[ax-1][ay]==dol))
		{
			++tmp_live;
		}
		if((ax+1>18) || (m_Board[ax+1][ay]==dol))
		{
			++tmp_live;
		}
		if((ay-1<0) || (m_Board[ax][ay-1]==dol))
		{
			++tmp_live;
		}
		if((ay+1>18) || (m_Board[ax][ay+1]==dol))
		{
			++tmp_live;
		}
		if(tmp_live==4) //놓여질 자리가 패의 상태 
		{		
			pae.b_pae = true;
			pae.x = link[0].x;
			pae.y = link[0].y;
		}
	}
}


