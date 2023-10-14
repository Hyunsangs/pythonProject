import tkinter as tk
from tkinter import messagebox, ttk
import yfinance as yf
import matplotlib.pyplot as plt

# 스택 초기화
search_history = []
search_history_stack = []
redo_stack = [] #Redo기능 위한 스택

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")
    
    if data.empty:
        return None
    
    return data['Close']

# 그래프 생성 함수
def plot_stock():
    plt.figure(figsize=(10, 6))
    
    for symbol in search_history:
        prices = get_stock_price(symbol)
        
        if prices is not None:
            prices.plot(label=symbol)
    
    plt.legend()
    plt.show()

def search_stock():
    stock_symbol = entry.get()

    # 이미 검색한 주식인지 확인
    if stock_symbol in search_history:
        messagebox.showinfo("주의", f"{stock_symbol}은(는) 이미 검색된 주식입니다.")
        return
    
     # 주식 가격 가져오기
    price_data= get_stock_price(stock_symbol)

    if price_data is not None: 
         current_price=price_data.iloc[-1]
         result_label.config(text=f"{stock_symbol}의 현재 가격은 ${current_price:.2f} 입니다.")
         
         # 검색 이력에 추가하고, 스택에도 추가
         search_history.append(stock_symbol)
         search_history_stack.append(stock_symbol)
         
         # 새로운 주식 추가 Redo stack 초기화
         redo_stack.clear()
            
    else:
         messagebox_label.config(text=f"{stock_symbol}의 가격을 가져올 수 없습니다.")

def show_popular_stocks():
   stocks=[('삼성전자','005930.ks'),('SK하이닉스','000660.ks'),('LG화학','051910.ks'),('NAVER','035420.ks'),('카카오','035720.ks')]

   tree=ttk.Treeview(window,columns=['1','2'],show='headings')
   tree.pack(side='right')

   tree.heading('1',text='주식 이름')
   tree.heading('2',text='상징코드')

   for name,code in stocks:
       tree.insert('', 'end', values=(name, code))
 
# Undo 기능 함수       
def undo_search():
    if not search_history_stack:
        messagebox.showinfo("주의", "더 이상 삭제할 주식이 없습니다.")
        return

    last_searched = search_history_stack.pop()
    
    # Redo를 위해 삭제된 항목 저장하기
    redo_stack.append(last_searched)
    
    # 검색 이력에서도 삭제합니다.
    search_history.remove(last_searched)

    messagebox_label.config(text=f"{last_searched} 검색이 취소되었습니다.")

# Redo 기능 함수
def redo_search():
   if not redo_stack:
       messagebox.showinfo("주의", "더 이상 되돌릴 검색이 없습니다.")
       return
   
   redone_item = redo_stack.pop()

   # 다시 검색 목록과 스택에 넣기 
   search_history.append(redone_item)
   search_history_stack.append(redone_item)

   messagebox_label.config(text=f"{redone_item} 의 탐색이 복원되었습니다.") 

         
def show_history():
   history_window=tk.Toplevel(window) 
   history_label=tk.Label(history_window,text="이전 검색 기록") 
   history_label.pack() 

   history_text=tk.Text(history_window,height=5,width=30) 
   history_text.pack() 

   for item in search_history:
       history_text.insert(tk.END, f"{item}\n")

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("주식 가격 조회")

# 라벨 및 엔트리 위젯 생성
label = tk.Label(window, text="주식 이름을 입력하세요:")
label.pack()

entry = tk.Entry(window)
entry.pack()

search_button = tk.Button(window, text="주식 추가", command=search_stock)
search_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

messagebox_label = tk.Label(window, text="")
messagebox_label.pack()

plot_button = tk.Button(window, text="그래프 보기", command=plot_stock)
plot_button.pack()

undo_button = tk.Button(window, text="최근 검색 삭제", command=undo_search)
undo_button.pack()

redo_button = tk.Button(window, text="되돌리기", command=redo_search)
redo_button.pack()

# 메뉴 생성 및 추가하기 
menubar=tk.Menu(window)

filemenu=tk.Menu(menubar) 

filemenu.add_command(label='Show History',command=show_history) 
filemenu.add_command(label='Exit',command=window.quit)

menubar.add_cascade(label='Menu', menu=filemenu)

window.config(menu=menubar)

# 국내 주식 인기 주식 5가지 표시
show_popular_stocks() 

# 메인 루프 시작
window.mainloop()
