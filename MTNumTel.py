import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class MaquinaTuring:
    def __init__(self):
        self.estados = {'q0', 'q1', 'q2a', 'q2b', 'q2c', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'}
        self.estado_inicial = 'q0'
        self.estados_finales = {'q10'}
        self.simbolos = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' '}
        self.transiciones = {}
        self._inicializar_transiciones()
        
    def _inicializar_transiciones(self):
        self.transiciones[('q0', '9')] = ('q1', '9', 'R')
        self.transiciones[('q1', '1')] = ('q2b', '1', 'R')
        self.transiciones[('q1', '3')] = ('q2b', '3', 'R')
        self.transiciones[('q1', '6')] = ('q2a', '6', 'R')
        self.transiciones[('q1', '9')] = ('q2c', '9', 'R')
        self.transiciones[('q2b', '2')] = ('q3', '2', 'R')
        self.transiciones[('q2b', '4')] = ('q3', '4', 'R')
        self.transiciones[('q2b', '6')] = ('q3', '6', 'R')
        self.transiciones[('q2b', '7')] = ('q3', '7', 'R')
        self.transiciones[('q2b', '8')] = ('q3', '8', 'R')
        self.transiciones[('q2b', '9')] = ('q3', '9', 'R')
        for digito in '123456789':
            self.transiciones[('q2a', digito)] = ('q3', digito, 'R')
        self.transiciones[('q2c', '2')] = ('q3', '2', 'R')
        self.transiciones[('q2c', '4')] = ('q3', '4', 'R')
        for digito in '0123456789':
            self.transiciones[('q3', digito)] = ('q4', digito, 'R')
            self.transiciones[('q4', digito)] = ('q5', digito, 'R')
            self.transiciones[('q5', digito)] = ('q6', digito, 'R')
            self.transiciones[('q6', digito)] = ('q7', digito, 'R')
            self.transiciones[('q7', digito)] = ('q8', digito, 'R')
            self.transiciones[('q8', digito)] = ('q9', digito, 'R')
            self.transiciones[('q9', digito)] = ('q10', digito, 'R')

    def ejecutar(self, entrada):
        entrada = entrada.replace(" ", "")
        
        if len(entrada) != 10:
            return False

        if not entrada.isdigit():
            return False

        if not (entrada.startswith('96') or 
                entrada.startswith('994') or 
                entrada.startswith('992') or 
                entrada.startswith('916') or 
                entrada.startswith('917') or 
                entrada.startswith('918') or 
                entrada.startswith('919') or 
                entrada.startswith('932') or 
                entrada.startswith('934')):
            return False

        if entrada.startswith('96') and entrada[2] == '0':
            return False
            
        cinta = list(entrada + ' ')
        posicion = 0
        estado_actual = self.estado_inicial
        
        while estado_actual not in self.estados_finales and posicion < len(cinta):
            simbolo_actual = cinta[posicion]

            if (estado_actual, simbolo_actual) not in self.transiciones:
                return False

            nuevo_estado, simbolo_escrito, movimiento = self.transiciones[(estado_actual, simbolo_actual)]
            cinta[posicion] = simbolo_escrito
            estado_actual = nuevo_estado

            if movimiento == 'R':
                posicion += 1
            elif movimiento == 'L':
                posicion -= 1
                
            if posicion < 0:
                return False
                
        return estado_actual in self.estados_finales

class InterfazMT:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Números Telefónicos")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a') 
        self.mt = MaquinaTuring()
        self.historial = []    
        self.configurar_estilos()
        self.crear_widgets()
        
    def configurar_estilos(self):
        self.COLOR_FONDO = '#1a1a1a'
        self.COLOR_VERDE = '#2d5a27' 
        self.COLOR_TEXTO = '#ffffff'
        self.COLOR_BOTON = '#1e401b'
    
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview',
                       background=self.COLOR_FONDO,
                       foreground=self.COLOR_TEXTO,
                       fieldbackground=self.COLOR_FONDO,
                       borderwidth=0)
        style.configure('Treeview.Heading',
                       background=self.COLOR_VERDE,
                       foreground=self.COLOR_TEXTO,
                       relief='flat')
        
        style.configure('Custom.TButton',
                       background=self.COLOR_BOTON,
                       foreground=self.COLOR_TEXTO,
                       padding=10,
                       font=('Arial', 11))
        
    def crear_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.COLOR_FONDO)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        titulo = tk.Label(main_frame,
                         text="Validador de Números Telefónicos",
                         font=('Arial', 16, 'bold'),
                         bg=self.COLOR_FONDO,
                         fg=self.COLOR_TEXTO)
        titulo.pack(pady=(0, 20))
        
        entrada_frame = tk.Frame(main_frame, bg=self.COLOR_FONDO)
        entrada_frame.pack(fill='x', pady=10)

        instrucciones = tk.Label(entrada_frame,
                               text="Introduce un número de 10 dígitos:",
                               font=('Arial', 11),
                               bg=self.COLOR_FONDO,
                               fg=self.COLOR_TEXTO)
        instrucciones.pack(side='left', padx=5)
  
        self.entrada = tk.Entry(entrada_frame,
                              font=('Arial', 11),
                              bg=self.COLOR_VERDE,
                              fg=self.COLOR_TEXTO,
                              insertbackground=self.COLOR_TEXTO,
                              width=15)
        self.entrada.pack(side='left', padx=5)

        self.boton_validar = ttk.Button(entrada_frame,
                                      text="Validar",
                                      command=self.validar,
                                      style='Custom.TButton')
        self.boton_validar.pack(side='left', padx=5)

        historial_frame = tk.Frame(main_frame, bg=self.COLOR_FONDO)
        historial_frame.pack(fill='both', expand=True, pady=(20, 0))

        titulo_historial = tk.Label(historial_frame,
                                  text="Historial de Validaciones",
                                  font=('Arial', 12, 'bold'),
                                  bg=self.COLOR_FONDO,
                                  fg=self.COLOR_TEXTO)
        titulo_historial.pack(pady=(0, 10))
        columns = ('No.', 'Número', 'Resultado')
        self.tree = ttk.Treeview(historial_frame, columns=columns, show='headings', height=10)
        
        self.tree.heading('No.', text='No.')
        self.tree.heading('Número', text='Número')
        self.tree.heading('Resultado', text='Resultado')
        self.tree.column('No.', width=50)
        self.tree.column('Número', width=200)
        self.tree.column('Resultado', width=200)
        scrollbar = ttk.Scrollbar(historial_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.contador_pruebas = 0
        
    def validar(self):
        numero = self.entrada.get().strip()
        self.contador_pruebas += 1
        
        if self.mt.ejecutar(numero):
            resultado = "Aceptado"
            messagebox.showinfo("Resultado", "El número es válido", 
                              icon='info')
        else:
            resultado = "Rechazado"
            messagebox.showerror("Resultado", "El número no es válido")

        self.tree.insert('', 0, values=(
            self.contador_pruebas,
            numero,
            resultado
        ))
        
        self.entrada.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazMT(root)
    root.mainloop()