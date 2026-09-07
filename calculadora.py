import tkinter as tk

botao1 = "#363434"
botao2 ="#424345"
visor = "#37474F"
igual = "#FFA840"
fundo = "#e8e6e6"

class Calculadora:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Calculadora")
        self.janela.geometry("352x465")
        self.janela.resizable(False, False)
        self.janela.configure(bg=fundo)
        
        for r in range(9):
            self.janela.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.janela.grid_columnconfigure(c, weight=1)
        
        self.visor = tk.Entry(
            janela, font=("Segoe UI", 20), bg=visor, fg="#ffffff", width=1, bd=0, justify="right"
        )
        self.visor.grid(row=0, column=0, columnspan=4, ipady=15, sticky="NSWE")
        
        botoes = [
            ("√", 1, 0, 1, botao1), ("π", 1, 1, 1, botao1), ("^", 1, 2, 1, botao1), ("!", 1, 3, 1, botao1),
            ("log", 2, 0, 1, botao1), ("sin", 2, 1, 1, botao1), ("cos", 2, 2, 1, botao1), ("tan", 2, 3, 1, botao1),
            ("ln", 3, 0, 1, botao1), ("e", 3, 1, 1, botao1), ("(", 3, 2, 1, botao1), (")", 3, 3, 1, botao1),
            ("C", 4, 0, 2, botao2), ("%", 4, 2, 1, botao2), ("/", 4, 3, 1, botao2),
            ("7", 5, 0, 1, botao1), ("8", 5, 1, 1, botao1), ("9", 5, 2, 1, botao1), ("×", 5, 3, 1, botao2),
            ("4", 6, 0, 1, botao1), ("5", 6, 1, 1, botao1), ("6", 6, 2, 1, botao1), ("-", 6, 3, 1, botao2),
            ("1", 7, 0, 1, botao1), ("2", 7, 1, 1, botao1), ("3", 7, 2, 1, botao1), ("+", 7, 3, 1, botao2),
            ("0", 8, 0, 1, botao1), (".", 8, 1, 1, botao1), ("⌫", 8, 2, 1, botao1), ("=", 8, 3, 1, igual)
        ]
        
        for texto, r, c, span, cor in botoes:
            moldura_btn = tk.Frame(
                janela,
                bg=cor,
                bd=2,
                relief="raised"
            )
            moldura_btn.grid(row=r, column=c, columnspan=span, sticky="NSWE")
            
            if (texto == "="):
                btn = tk.Button(
                    moldura_btn,
                    text=texto,
                    font=("Segoe UI", 12),
                    bg=cor,
                    fg=visor,
                    bd=0,
                    activebackground="#dadada"
                )
            else:
                btn = tk.Button(
                    moldura_btn,
                    text=texto,
                    font=("Segoe UI", 12),
                    bg=cor,
                    fg="#FFFFFF",
                    bd=0,
                    activebackground="#dadada"
                )
            btn.pack(fill="both", expand=True)
              
                
            btn.bind("<Enter>", lambda event, f=moldura_btn: f.config(relief="groove"))
            btn.bind("<Leave>", lambda event, f=moldura_btn: f.config(relief="raised"))
        
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = Calculadora(janela_principal)
    janela_principal.mainloop()