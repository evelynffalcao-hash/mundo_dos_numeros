import tkinter as tk
from tkinter import messagebox
import random
import pyttsx3
import threading

def falar_agora(texto):
    def tarefa():
        try:
            engine_local = pyttsx3.init()
            engine_local.say(texto)
            engine_local.runAndWait()
        except:
            pass 
    threading.Thread(target=tarefa, daemon=True).start()

def por_extenso(n):
    unidades = {0: "ZERO", 1: "UM", 2: "DOIS", 3: "TRÊS", 4: "QUATRO", 5: "CINCO", 
                6: "SEIS", 7: "SETE", 8: "OITO", 9: "NOVE"}
    especiais = {10: "DEZ", 11: "ONZE", 12: "DOZE", 13: "TREZE", 14: "CATORZE", 
                 15: "QUINZE", 16: "DEZESSEIS", 17: "DEZESSETE", 18: "DEZOITO", 19: "DEZENOVE", 20: "VINTE"}
    if n < 10: return unidades[n]
    return especiais.get(n, str(n))

class MundoDosNumeros:
    def __init__(self, root):
        self.root = root
        self.root.title("Mundo dos Números")
        self.root.geometry("850x800")
        self.numero_atual = 0
        self.tentativas = 0
        self.modo_quiz = "ouvindo" # Pode ser "ouvindo" ou "escrevendo"
        
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True, fill="both")
        self.tela_estudo()

    def limpar(self):
        for w in self.container.winfo_children():
            w.destroy()

    def tela_estudo(self):
        self.limpar()
        tk.Label(self.container, text="VAMOS APRENDER!", font=("Arial", 28, "bold")).pack(pady=20)
        cor = "navy" if self.numero_atual % 2 == 0 else "red"
        tk.Label(self.container, text=str(self.numero_atual), font=("Arial", 120, "bold"), fg=cor).pack()
        tk.Label(self.container, text=por_extenso(self.numero_atual), font=("Arial", 50, "bold")).pack(pady=10)

        tk.Button(self.container, text="🔊 OUVIR", command=lambda: falar_agora(str(self.numero_atual)), 
                  font=("Arial", 22), bg="lightgray", width=15).pack(pady=10)

        frame_nav = tk.Frame(self.container)
        frame_nav.pack(pady=15)
        if self.numero_atual > 0:
            tk.Button(frame_nav, text="⬅️ VOLTAR", command=self.voltar, font=("Arial", 18, "bold"), bg="orange", width=12).pack(side="left", padx=10)
        
        # Botão Próximo ou Refresh
        if self.numero_atual < 20:
            tk.Button(frame_nav, text="PRÓXIMO ➡️", command=self.proximo, font=("Arial", 18, "bold"), bg="lightgreen", width=12).pack(side="left", padx=10)
        else:
            tk.Button(frame_nav, text="RECOMEÇAR 🔄", command=self.refresh, font=("Arial", 18, "bold"), bg="yellow", width=12).pack(side="left", padx=10)

        tk.Button(self.container, text="VAMOS PRATICAR? 🎯", command=self.quiz, font=("Arial", 18), bg="lightblue", width=22).pack(pady=20)

    def proximo(self):
        self.numero_atual += 1
        self.tela_estudo()

    def voltar(self):
        self.numero_atual -= 1
        self.tela_estudo()

    def refresh(self):
        self.numero_atual = 0
        self.tela_estudo()

    def quiz(self):
        self.limpar()
        self.tentativas = 0
        self.sorteado = random.randint(0, self.numero_atual)
        self.modo_quiz = random.choice(["ouvindo", "escrevendo"]) # Sorteia o modo de jogo
        
        if self.modo_quiz == "ouvindo":
            tk.Label(self.container, text="OUÇA E DIGITE O NÚMERO:", font=("Arial", 22, "bold")).pack(pady=30)
            tk.Button(self.container, text="🔊 OUVIR", command=lambda: falar_agora(str(self.sorteado)), 
                      font=("Arial", 22), width=15).pack(pady=10)
            self.ent = tk.Entry(self.container, font=("Arial", 80, "bold"), justify='center', width=5)
        else:
            tk.Label(self.container, text="ESCREVA O NOME DO NÚMERO:", font=("Arial", 22, "bold")).pack(pady=20)
            tk.Label(self.container, text=str(self.sorteado), font=("Arial", 100, "bold"), fg="purple").pack()
            self.ent = tk.Entry(self.container, font=("Arial", 40, "bold"), justify='center', width=15)
        
        self.ent.pack(pady=20)
        self.ent.focus_set()
        tk.Button(self.container, text="VERIFICAR ✅", font=("Arial", 22, "bold"), command=self.validar, bg="orange", width=18).pack(pady=10)
        tk.Button(self.container, text="VOLTAR AO ESTUDO", command=self.tela_estudo, font=("Arial", 14)).pack(pady=20)

    def validar(self):
        resposta = self.ent.get().strip().upper()
        objetivo = str(self.sorteado) if self.modo_quiz == "ouvindo" else por_extenso(self.sorteado)
        
        if resposta == objetivo:
            messagebox.showinfo("Muito bem!", "Você acertou! Parabéns!")
            self.quiz()
        else:
            self.tentativas += 1
            if self.tentativas >= 2:
                messagebox.showwarning("Aviso", f"O correto era {objetivo}. Vamos tentar outro!")
                self.quiz()
            else:
                messagebox.showerror("Ops!", "Tente mais uma vez!")
                self.ent.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MundoDosNumeros(root)
    root.mainloop()
