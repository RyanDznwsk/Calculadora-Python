import math
import tkinter as tk

botao1 = "#363434"
botao2 ="#424345"
visor = "#37474F"
igual = "#FFA840"
fundo = "#e8e6e6"

class Calculadora:
    def __init__(self, janela):
        self.janela = janela
        self.expressao = ""
        self.limpar_no_próximo_clique = False
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
        
        self.visor.bind("<Key>", lambda e: "break")
        
        botoes = [
            ("√", 1, 0, 1, botao1), ("π", 1, 1, 1, botao1), ("^", 1, 2, 1, botao1), ("!", 1, 3, 1, botao1),
            ("log", 2, 0, 1, botao1), ("sin", 2, 1, 1, botao1), ("cos", 2, 2, 1, botao1), ("tan", 2, 3, 1, botao1),
            ("ln", 3, 0, 1, botao1), ("e", 3, 1, 1, botao1), ("(", 3, 2, 1, botao1), (")", 3, 3, 1, botao1),
            ("C", 4, 0, 2, botao2), ("%", 4, 2, 1, botao2), ("÷", 4, 3, 1, botao2),
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
            
            if texto == "=":
                btn = tk.Button(
                    moldura_btn,
                    text=texto,
                    font=("Segoe UI", 12),
                    bg=cor,
                    fg=visor,
                    bd=0,
                    activebackground="#dadada",
                    command=lambda t=texto: self.clique_botao(t)
                )
            else:
                btn = tk.Button(
                    moldura_btn,
                    text=texto,
                    font=("Segoe UI", 12),
                    bg=cor,
                    fg="#FFFFFF",
                    bd=0,
                    activebackground="#dadada",
                    command=lambda t=texto: self.clique_botao(t)
                )
            btn.pack(fill="both", expand=True)
                
            btn.bind("<Enter>", lambda event, f=moldura_btn: f.config(relief="groove"))
            btn.bind("<Leave>", lambda event, f=moldura_btn: f.config(relief="raised"))
            
        self.janela.focus_set()
        self.janela.bind("<Key>", self.escutar_teclado)
    
    def escutar_teclado(self, evento):
        char = evento.char
        keysym = evento.keysym
        
        if keysym == "BackSpace": self.clique_botao("⌫")
        elif keysym in ["Return", "KP_Enter"]: self.clique_botao("=")
        elif keysym == "Escape": self.clique_botao("C")
        elif char in "0123456789.+-^!%()": self.clique_botao(char)
        elif char == "*": self.clique_botao("×")
        elif char == "/": self.clique_botao("÷")
        return "break"
    
    def clique_botao(self, valor):
        if valor == "C":
            self.expressao = ""
            self.visor.delete(0, tk.END)
        elif valor == "⌫":
            self.expressao = self.expressao[:-1]
            self.visor.delete(0, tk.END)
            self.visor.insert(0, self.expressao)
        elif valor == "=":
            try:
                tokens = self.tokenizar(self.expressao)
                postfix = self.infix_para_postfix(tokens)
                resultado = self.calcular_postfix(postfix)
                self.visor.delete(0, tk.END)
                self.visor.insert(0, str(resultado))
                
                if resultado != "Erro":
                    self.expressao = str(resultado)
                    self.limpar_no_próximo_clique = True
                else:
                    self.expressao = ""
            except Exception:
                self.visor.delete(0, tk.END)
                self.visor.insert(0, "Erro")
                self.expressao = ""
        else:
            operadores_continuidade = ["+", "-", "×", "÷", "^", "%", "!"]
            
            if self.limpar_no_próximo_clique and valor not in operadores_continuidade:
                self.expressao = valor
            else:
                if self.expressao and valor in operadores_continuidade:
                    ultimo_char = self.expressao[-1]
                    if ultimo_char in operadores_continuidade:
                        self.expressao = self.expressao[:-1] + valor
                    else:
                        self.expressao += valor
                else:
                    self.expressao += valor
            
            self.limpar_no_próximo_clique = False
            
            self.visor.delete(0, tk.END)
            self.visor.insert(0, self.expressao)
    
    def preparar_expressao(self, texto_visor):
        expressao_tratada = texto_visor.replace("×", "*")
        expressao_tratada = expressao_tratada.replace("^", "**")
        expressao_tratada = expressao_tratada.replace("÷", "/")
        return expressao_tratada
    
    def tokenizar(self, expressao_texto):
        tokens = []
        numero_atual = ""
        operadores = ["+", "-", "×", "÷", "^", "!", "%", "(", ")", "π", "e"]
        funcoes = ["sin", "cos", "tan", "log", "ln", "√"]
        
        i = 0
        while i < len(expressao_texto):
            char = expressao_texto[i]
            
            if char.isdigit() or char == ".":
                numero_atual += char
                i += 1
            else:
                if numero_atual:
                    tokens.append(numero_atual)
                    numero_atual = ""
                funcao_encontrada = False
                for f in funcoes:
                    if expressao_texto[i:].startswith(f):
                        tokens.append(f)
                        i += len(f)
                        funcao_encontrada = True
                        break
                    
                if funcao_encontrada:
                    continue
                
                if char in operadores:
                    tokens.append(char)
                    i += 1
                else:
                    i += 1
        
        if numero_atual:
            tokens.append(numero_atual)
        return tokens
    
    def infix_para_postfix(self, tokens):
        precedencia = {
            "+": 1, "-": 1,
            "×": 2, "÷": 2,
            "^": 3, "sin": 3, "cos": 3, "tan": 3, "log": 3, "ln": 3, "√": 3, "!": 3, "%": 3
        }
        
        saida = []
        pilha = []
        
        for token in tokens:
            if token.replace(".", "", 1).isdigit() or token in ["π", "e"]:
                saida.append(token)
            elif token in ["sin", "cos", "tan", "log", "ln", "√", "("]:
                pilha.append(token)
            elif token == ")":
                while pilha and pilha[-1] != "(":
                    saida.append(pilha.pop())
                if pilha and pilha[-1] == "(":
                    pilha.pop()
                if pilha and pilha[-1] in ["sin", "cos", "tan", "log", "ln", "√"]:
                    saida.append(pilha.pop())
            elif token in precedencia:
                while (pilha and pilha[-1] != "(" and precedencia.get(pilha[-1], 0) >= precedencia[token]):
                    saida.append(pilha.pop())
                pilha.append(token)
            
        while pilha:
            saida.append(pilha.pop())
        return saida

    def calcular_postfix(self, tokens_postfix):
        pilha = []
        
        for token in tokens_postfix:
            if token.replace(".", "", 1).isdigit():
                pilha.append(float(token))
            elif token == "π":
                pilha.append(math.pi)
            elif token == "e":
                pilha.append(math.e)
            elif token in ["+", "-", "×", "÷", "^"]:
                if len(pilha) < 2: return "Erro"
                
                num2 = pilha.pop()
                num1 = pilha.pop()
                
                if token == "+": pilha.append(num1 + num2)
                elif token == "-": pilha.append(num1 - num2)
                elif token == "×": pilha.append(num1 * num2)
                elif token == "÷":
                    if num2 == 0: return "Erro"
                    pilha.append(num1 / num2)
                elif token == "^": pilha.append(num1 ** num2)
            elif token in ["sin", "cos", "tan", "log", "ln", "√", "!", "%"]:
                if len(pilha) < 1: return "Erro"
                
                num = pilha.pop()
                
                if token == "√":
                    if num < 0: return "Erro"
                    pilha.append(math.sqrt(num))
                elif token == "sin": pilha.append(math.sin(math.radians(num)))
                elif token == "cos": pilha.append(math.cos(math.radians(num)))
                elif token == "tan": pilha.append(math.tan(math.radians(num)))
                elif token == "log":
                    if num <= 0: return "Erro"
                    pilha.append(math.log10(num))
                elif token == "ln":
                    if num <= 0: return "Erro"
                    pilha.append(math.log(num))
                elif token == "!":
                    if num < 0 or not num.is_integer(): return "Erro"
                    pilha.append(math.factorial(int(num)))
                elif token == "%": pilha.append(num / 100)
        
        if len(pilha) == 1:
            resultado = pilha[0]
            
            if isinstance(resultado, (int, float)) and hasattr(resultado, 'is_integer') and resultado.is_integer():
                return int(resultado)
            return round(resultado, 6)
        return "Erro"
                    
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = Calculadora(janela_principal)
    janela_principal.mainloop()