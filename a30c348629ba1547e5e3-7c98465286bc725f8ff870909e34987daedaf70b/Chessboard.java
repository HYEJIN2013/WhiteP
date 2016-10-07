

public class Chessboard {
	/**
	 * this is an object which shows the process of chess board.
	 */
	int tile=1;
	int size;
	int flag=0;
	static int[][] board;
	//构造函数
	public Chessboard()
	{
	}
	public Chessboard(int size)
	{
		this.size = size;
		init();
	}
	//初始化函数
	public void init()
	{
		board = new int[size][size];
		for(int i=0; i<size; i++)
		{
			for(int j=0; j<size; j++)
				board[i][j]=0;
		}
	}
	//分治法实现棋盘覆盖算法
	public void chessBoard(int tr, int tc, int dr, int dc, int size)
	{
		if(size == 1){
			return;
		}
		int t=tile++;
		int  s = size/2;
		if(dr<tr+s && dc<tc+s){                   //覆盖棋盘左上角
			flag = 1;
			chessBoard(tr,tc,dr,dc,s);
		}
		else {
			//if(board[tr+s-1][tr+s-1]==0)
			board[tr+s-1][tc+s-1] = t;
			System.out.println("*****************");
			showBoard();
			chessBoard(tr,tc,tr+s-1,tc+s-1,s);
		}
		
		if(dr<tr+s && dc>=tc+s){                  //覆盖棋盘右上角
			flag = 2;
			chessBoard(tr,tc+s,dr,dc,s);
		}
		else{
			//if(board[tr+s-1][tc+s]==0)
			board[tr+s-1][tc+s] = t;
			System.out.println("*****************");
			showBoard();
			chessBoard(tr,tc+s,tr+s-1,tc+s,s);
		}
		
		if(dr>=tr+s && dc<tc+s){                  //覆盖棋盘左下角
			flag = 3;
			chessBoard(tr+s,tc,dr,dc,s);
		}
		else{
			//if(board[tr+s][tc+s-1]==0)
			board[tr+s][tc+s-1] = t;
			System.out.println("*****************");
			showBoard();
			chessBoard(tr+s,tc,tr+s,tc+s-1,s);
		}
		
		if(dr>=tr+s && dc>=tc+s){                 //覆盖棋盘右下角
			flag = 4;
			chessBoard(tr+s,tc+s,dr,dc,s);
		}
		else{
			//if(board[tr+s][tc+s]==0)
			board[tr+s][tc+s] = t;
			System.out.println("*****************");
			showBoard();
			chessBoard(tr+s,tc+s,tr+s,tc+s,s);
		}
		
	}
	public void showBoard()
	{
		for(int i=0; i<this.size; i++){
			
			for(int j=0; j<this.size; j++)
				System.out.print(board[i][j]+"\t");

			System.out.println();
		}
			
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Chessboard chess1 = new Chessboard(4);
		chess1.chessBoard(0, 0, 0, 3, chess1.size);
		//chess1.showBoard();
	}

}
