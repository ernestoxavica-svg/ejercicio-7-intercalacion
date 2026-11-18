"""
ADA3 - Ejercicio 7: Fusión de catálogos de sucursales
Método de ordenamiento externo: INTERCALACIÓN (Merge)

El programa toma dos listas de productos previamente ordenadas por código SKU
(Sucursal Norte y Sucursal Sur) y las intercala en un único catálogo maestro
ordenado en una sola pasada secuencial.
"""
import tkinter as tk
from tkinter import ttk, messagebox


def intercalacion(lista_a, lista_b):
    """Intercala dos listas ya ordenadas por SKU (clave[0]) en una sola lista ordenada.

    Recorre ambas listas simultáneamente con dos índices (i, j), comparando sus
    elementos actuales y extrayendo siempre el menor hacia el archivo maestro.
    Regresa (lista_resultado, pasos).
    """
    resultado = []
    pasos = []
    i, j = 0, 0
    comparaciones = 0

    while i < len(lista_a) and j < len(lista_b):
        comparaciones += 1
        if lista_a[i][0] <= lista_b[j][0]:
            elegido = lista_a[i]
            origen = "Norte"
            i += 1
        else:
            elegido = lista_b[j]
            origen = "Sur"
            j += 1
        resultado.append((elegido[0], elegido[1], origen))
        pasos.append(f"Comp {comparaciones}: se toma '{elegido[0]} - {elegido[1]}' (Suc. {origen})")

    # Vaciar remanentes de Sucursal Norte si quedaron elementos
    while i < len(lista_a):
        elegido = lista_a[i]
        resultado.append((elegido[0], elegido[1], "Norte"))
        pasos.append(f"Remanente Norte: se agrega '{elegido[0]} - {elegido[1]}'")
        i += 1

    # Vaciar remanentes de Sucursal Sur si quedaron elementos
    while j < len(lista_b):
        elegido = lista_b[j]
        resultado.append((elegido[0], elegido[1], "Sur"))
        pasos.append(f"Remanente Sur: se agrega '{elegido[0]} - {elegido[1]}'")
        j += 1

    return resultado, pasos


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catálogo Maestro - Intercalación")
        self.geometry("660x620")
        self.resizable(False, False)
        ttk.Style(self).theme_use("clam")

        self.sucursal_norte = []  # lista ordenada de (sku, producto)
        self.sucursal_sur = []    # lista ordenada de (sku, producto)

        ttk.Label(self, text="Fusión de Catálogos de Sucursales",
                  font=("Segoe UI", 16, "bold")).pack(pady=(12, 0))
        ttk.Label(self, text="Ordenamiento externo por método de Intercalación (2 vías)",
                  foreground="#555").pack(pady=(0, 8))

        # --- Formulario para agregar a listas ya ordenadas ---
        form = ttk.Frame(self)
        form.pack(pady=5)
        ttk.Label(form, text="Sucursal:").grid(row=0, column=0, padx=4)
        self.sucursal_cb = ttk.Combobox(form, values=["Norte", "Sur"], width=8, state="readonly")
        self.sucursal_cb.current(0)
        self.sucursal_cb.grid(row=0, column=1, padx=4)

        ttk.Label(form, text="SKU (ej. 105):").grid(row=0, column=2, padx=4)
        self.sku_entry = ttk.Entry(form, width=10)
        self.sku_entry.grid(row=0, column=3, padx=4)

        ttk.Label(form, text="Producto:").grid(row=0, column=4, padx=4)
        self.prod_entry = ttk.Entry(form, width=18)
        self.prod_entry.grid(row=0, column=5, padx=4)

        ttk.Button(form, text="Agregar", command=self.agregar).grid(row=0, column=6, padx=4)
        self.prod_entry.bind("<Return>", lambda e: self.agregar())

        # --- Tablas de origen (F1 y F2) ---
        frame_origen = ttk.Frame(self)
        frame_origen.pack(padx=20, pady=5, fill="x")

        # Tabla Norte
        f_norte = ttk.LabelFrame(frame_origen, text="Archivo F1: Sucursal Norte (Ordenado)")
        f_norte.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.tabla_norte = ttk.Treeview(f_norte, columns=("sku", "prod"), show="headings", height=6)
        self.tabla_norte.heading("sku", text="SKU")
        self.tabla_norte.heading("prod", text="Producto")
        self.tabla_norte.column("sku", width=70, anchor="center")
        self.tabla_norte.column("prod", width=210)
        self.tabla_norte.pack(padx=5, pady=5)

        # Tabla Sur
        f_sur = ttk.LabelFrame(frame_origen, text="Archivo F2: Sucursal Sur (Ordenado)")
        f_sur.pack(side="right", expand=True, fill="both", padx=(5, 0))
        self.tabla_sur = ttk.Treeview(f_sur, columns=("sku", "prod"), show="headings", height=6)
        self.tabla_sur.heading("sku", text="SKU")
        self.tabla_sur.heading("prod", text="Producto")
        self.tabla_sur.column("sku", width=70, anchor="center")
        self.tabla_sur.column("prod", width=210)
        self.tabla_sur.pack(padx=5, pady=5)

        # --- Botones ---
        botones = ttk.Frame(self)
        botones.pack(pady=6)
        ttk.Button(botones, text="Intercalar Catálogos", command=self.ejecutar_intercalacion).pack(side="left", padx=5)
        ttk.Button(botones, text="Cargar ejemplo", command=self.ejemplo).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        # --- Tabla Resultado (Archivo Maestro) ---
        ttk.Label(self, text="Archivo Maestro Consolidado:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20)
        self.tabla_res = ttk.Treeview(self, columns=("sku", "prod", "suc"), show="headings", height=7)
        self.tabla_res.heading("sku", text="SKU")
        self.tabla_res.heading("prod", text="Producto")
        self.tabla_res.heading("suc", text="Origen")
        self.tabla_res.column("sku", width=90, anchor="center")
        self.tabla_res.column("prod", width=390)
        self.tabla_res.column("suc", width=120, anchor="center")
        self.tabla_res.pack(padx=20, pady=4)

        # --- Registro de pasos ---
        self.log = tk.Text(self, height=5, width=76, state="disabled",
                           font=("Consolas", 9), bg="#f5f5f5", relief="flat")
        self.log.pack(padx=20, pady=5)

    def agregar(self):
        suc = self.sucursal_cb.get()
        prod = self.prod_entry.get().strip()
        try:
            sku = int(self.sku_entry.get())
        except ValueError:
            messagebox.showwarning("Dato inválido", "El SKU debe ser un número entero.")
            return
        if not prod:
            messagebox.showwarning("Falta producto", "Escribe el nombre del producto.")
            return

        lista_objetivo = self.sucursal_norte if suc == "Norte" else self.sucursal_sur
        # Mantener la precondición de archivo origen ordenado
        if lista_objetivo and sku < lista_objetivo[-1][0]:
            messagebox.showwarning(
                "Precondición de Intercalación",
                f"Los archivos origen deben estar ordenados.\nIngresa un SKU >= {lista_objetivo[-1][0]}."
            )
            return

        lista_objetivo.append((sku, prod))
        self.sku_entry.delete(0, "end")
        self.prod_entry.delete(0, "end")
        self.sku_entry.focus()
        self.mostrar_origenes()

    def ejecutar_intercalacion(self):
        if not self.sucursal_norte or not self.sucursal_sur:
            messagebox.showinfo("Faltan datos", "Debe haber al menos 1 producto en ambas sucursales.")
            return
        maestro, pasos = intercalacion(self.sucursal_norte, self.sucursal_sur)
        self.tabla_res.delete(*self.tabla_res.get_children())
        for sku, prod, suc in maestro:
            self.tabla_res.insert("", "end", values=(f"SKU-{sku}", prod, suc))
        self.escribir_log(pasos)

    def mostrar_origenes(self):
        self.tabla_norte.delete(*self.tabla_norte.get_children())
        for sku, prod in self.sucursal_norte:
            self.tabla_norte.insert("", "end", values=(f"SKU-{sku}", prod))

        self.tabla_sur.delete(*self.tabla_sur.get_children())
        for sku, prod in self.sucursal_sur:
            self.tabla_sur.insert("", "end", values=(f"SKU-{sku}", prod))

    def escribir_log(self, lineas):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("end", "\n".join(lineas))
        self.log.config(state="disabled")

    def ejemplo(self):
        self.sucursal_norte = [(102, "Laptop Pro 14"), (115, "Teclado Mecánico"),
                               (128, "Monitor 27''"), (145, "Webcam HD")]
        self.sucursal_sur = [(101, "Mouse Inalámbrico"), (110, "Audífonos USB"),
                             (128, "Base Enfriadora"), (150, "Disco SSD 1TB")]
        self.mostrar_origenes()
        self.tabla_res.delete(*self.tabla_res.get_children())
        self.escribir_log(["Catálogos ordenados cargados. Presiona 'Intercalar Catálogos'."])

    def limpiar(self):
        self.sucursal_norte.clear()
        self.sucursal_sur.clear()
        self.mostrar_origenes()
        self.tabla_res.delete(*self.tabla_res.get_children())
        self.escribir_log([])


if __name__ == "__main__":
    App().mainloop()