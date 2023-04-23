import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

class ChessBoard(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # 呼叫父類別的建構函式
        self.parent = parent  # 設定父容器
        self.cell_size = 50  # 設定棋盤格子大小
        self.num_cells = 15  # 設定棋盤格子數
        self.board = [[0 for _ in range(self.num_cells)] for _ in range(self.num_cells)]  # 將每一個位置都初始化為 0
        self.turn = 1  # 設定遊戲開始時，黑方先手
        self.timer = 30  # 設定計時器初值為 30 秒
        self.over = False
        self.is_first_move = True  # 設定是否為第一步
        self.timer_id = None  # 計時器的 ID
        self.draw_board()  # 畫出棋盤
        self.bind("<Button-1>", self.click)  # 綁定滑鼠點擊事件到 click 函式
      
        
        # 新增一個Frame包裝計時器、回合和重置遊戲的按鈕
        control_frame = tk.Frame(parent)
        control_frame.pack(side=tk.TOP, pady=10)

        # 設定計時器
        self.time_var = tk.StringVar(value="00:30")
        timer_label = tk.Label(control_frame, textvariable=self.time_var, font=("Arial", 20))
        timer_label.pack(side=tk.LEFT, padx=10)

        # 設定回合顯示
        self.turn_var = tk.StringVar(value="Black's turn")
        turn_label = tk.Label(control_frame, textvariable=self.turn_var, font=("Arial", 20))
        turn_label.pack(side=tk.LEFT, padx=10)

        # 設定重置遊戲的按鈕
        reset_button = ttk.Button(control_frame, text="Reset", style="C.TButton", command=self.reset_board)
        reset_button.pack(side=tk.LEFT, padx=10)

        # 設定重置按鈕的樣式
        style = ttk.Style()
        style.configure('C.TButton', font=('Arial', 20), padding=10, borderwidth=0, background='#000', foreground='#000')
        style.map('C.TButton', background=[('active', '#000'), ('disabled', '#000')])
        #self.start_timer()
    
    # 繪製棋盤的網格線
    def draw_board(self):
        # 以self.cell_size為間隔，畫出self.num_cells條水平與垂直線
        for i in range(self.num_cells):
            self.create_line(self.cell_size // 2, (i + 0.5) * self.cell_size, 
                             (self.num_cells - 0.5) * self.cell_size, (i + 0.5) * self.cell_size)
            self.create_line((i + 0.5) * self.cell_size, self.cell_size // 2,
                             (i + 0.5) * self.cell_size, (self.num_cells - 0.5) * self.cell_size)
    
    # 啟動倒數計時器
    def start_timer(self):        
        # 如果計時器已經歸零，則直接呼叫計時器時間到期的方法，並結束此函式
        if self.timer == 0:
            self.timer_expired()
            return
        
        # 如果時間還沒到，則先計算出目前的分鐘數和秒數
        minutes = self.timer // 60
        seconds = self.timer % 60
        
        # 將分鐘和秒數格式化後更新時間顯示的變數
        self.time_var.set("{:02d}:{:02d}".format(minutes, seconds))
        
        # 每執行一次就將計時器減1，並設定一秒後再次呼叫此函式
        self.timer -= 1
        self.timer_id = self.after(1000, self.start_timer)

    # 重置倒數計時器
    def reset_timer(self, startT):
        self.after_cancel(self.timer_id)  # 取消之前的計時器
        self.timer = 30  # 重設計時器為30秒
        self.time_var.set("00:30")  # 更新計時器顯示
        if startT:
            self.start_timer()  # 啟動計時器
       
    # 當倒數計時器時間到了的話
    def timer_expired(self):
        # 隨機在目前棋盤上空的位置下一步棋
        empty_cells = []  # 建立一個空的 list，用來儲存棋盤上所有空的位置
        # 表示所有的列
        for row in range(self.num_cells):
            # 表示所有的行
            for col in range(self.num_cells):
                # 將棋盤位置為0的位置加入empty_cells
                if self.board[row][col] == 0: 
                    empty_cells.append((row, col))
        # 判斷是否有空的位置
        if empty_cells:
            row, col = random.choice(empty_cells)  # 從空的位置隨機選擇一個位置
            self.draw_piece(row, col)  # 在選擇的位置下一個棋子            
            self.turn = 3 - self.turn  # 換到另外一方的回合
            self.turn_var.set("Black's turn" if self.turn == 1 else "White's turn")  # 更新回合顯示
            # 判斷遊戲是否結束
            if not self.check_win(row, col):            
                self.reset_timer(startT = True)
    
    # 在棋盤上點擊時會觸發的事件
    def click(self, event):
        x, y = event.x, event.y  # 從event物件中讀取使用者點擊的位置座標
        col, row = x // self.cell_size, y // self.cell_size  # 儲存點擊位置的座標除以self.cell_size得到所在格子的行列索引
        # 檢查該格子是否是空的
        if self.board[row][col] == 0:
            self.draw_piece(row, col)  # 在點擊的位置繪製一個棋子
            self.turn = 3 - self.turn  # 換到另外一方的回合
            self.turn_var.set("Black's turn" if self.turn == 1 else "White's turn")  # 更新回合顯示
            # 判斷遊戲是否結束
            if not self.check_win(row, col):            
                # 判斷是否為第一步，True的話就開始計時，False的話就重製計時器
                if self.is_first_move:
                    self.is_first_move = False
                    self.start_timer()
                else:
                    self.reset_timer(startT = True)
            
    # 繪製棋子
    def draw_piece(self, row, col):
        # 取得棋子座標位置
        x = (col + 0.5) * self.cell_size
        y = (row + 0.5) * self.cell_size
        # 判斷是誰的回合
        if self.turn == 1:
            self.create_oval(x - self.cell_size // 3, y - self.cell_size // 3, 
                              x + self.cell_size // 3, y + self.cell_size // 3, fill="black")  # 畫出一個黑色的圓
            self.board[row][col] = 1  # 將棋盤上的該位置標記為黑色
        else:
            self.create_oval(x - self.cell_size // 3, y - self.cell_size // 3, 
                              x + self.cell_size // 3, y + self.cell_size // 3, fill="white")  # 畫出一個白色的圓
            self.board[row][col] = 2  # 將棋盤上的該位置標記為白色
    
    # 檢查是否達到勝利條件
    def check_win(self, row, col):
        piece = self.board[row][col]  # 取得目前下的棋子是黑色或白色
        # 檢查水平、垂直、對角線(兩種)是否有五個棋子相連
        for dx, dy in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1  # 計數器，紀錄目前已有幾顆同色棋子相連
            for i in range(1, 5):
                r, c = row + i * dy, col + i * dx  # 檢查方向上一格
                if not (0 <= r < self.num_cells and 0 <= c < self.num_cells and self.board[r][c] == piece):
                    # 如果超出邊界或是該格沒有同色棋子，結束檢查該方向
                    break
                count += 1
            for i in range(1, 5):
                r, c = row - i * dy, col - i * dx  # 檢查反方向上一格
                if not (0 <= r < self.num_cells and 0 <= c < self.num_cells and self.board[r][c] == piece):
                    # 如果超出邊界或是該格沒有同色棋子，結束檢查該方向
                    break
                count += 1
            if count >= 5:  # 如果已經有五顆棋子相連
                self.reset_timer(startT = False)
                self.game_over(piece)  # 遊戲結束，顯示勝利者                
                return True
        
        # 檢查是否棋盤已滿
        if all(self.board[i][j] != 0 for i in range(self.num_cells) for j in range(self.num_cells)):
            self.reset_timer(startT = False)
            self.game_over(0)  # 棋盤已滿，遊戲結束，顯示平局            
            return True        

    # 當遊戲結束時執行    
    def game_over(self, winner):
        # 判斷誰是贏家 0: 平手、1:黑色、2:白色
        if winner == 0:
            messagebox.showinfo("Game Over", "Tie!")
        elif winner == 1:
            messagebox.showinfo("Game Over", "Black wins!")
        else:
            messagebox.showinfo("Game Over", "White wins!")
        self.reset_board()  # 重置整個棋盤

    # 重置整個棋盤
    def reset_board(self):
        # 清空棋盤
        self.board = [[0 for _ in range(self.num_cells)] for _ in range(self.num_cells)]  # 將每一個位置都初始化為 0
        self.delete("all")  # 把畫布上所有的東西都刪掉
        self.draw_board()  # 畫出新的棋盤
        self.turn = 1  # 重置為黑色的回合
        self.turn_var.set("Black's turn" if self.turn == 1 else "White's turn")  # 更新回合顯示
        self.reset_timer(startT=False)  # 重置倒數計時器

def main():
    root = tk.Tk()  # 建立視窗物件
    root.title("五子棋")  # 設定視窗標題
    root.iconbitmap('Backgammon_icon.ico')  # 設定視窗圖示
    win_width = 750  # 設定視窗寬度
    win_height = 850  # 設定視窗高度
    root.resizable(width=False, height=False)  # 設定最大化視窗時不改變大小
    screen_width = root.winfo_screenwidth()  # 取得螢幕寬度
    screen_height = root.winfo_screenheight()  # 取得螢幕高度
    x = (screen_width // 2) - (win_width // 2)  # 計算視窗 X 座標
    y = (screen_height // 2) - (win_height // 2)  # 計算視窗 Y 座標
    root.geometry(f"{win_width}x{win_height}+{x}+{y}")  # 設定視窗大小和位置
    board = ChessBoard(root, width=win_width, height=win_height)  # 建立五子棋物件
    board.pack()  # 將五子棋物件加入視窗中
    root.mainloop()  # 啟動視窗主迴圈

# 判斷當前模組是否為主程序執行的模組
if __name__ == "__main__":
    main()