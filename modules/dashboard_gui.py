
import tkinter as tk
from tkinter import ttk, messagebox

from modules.dashboard_db import (
    obtener_indicadores,
    obtener_pipeline_por_estado
)

from modules.clientes_gui import ClientesApp


class DashboardApp:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title("ZEROCOOL CRM - Dashboard")
        self.ventana.geometry("1150x750")
        self.ventana.minsize(950, 650)
        self.ventana.configure(bg="#102A43")

        self.crear_interfaz()
        self.actualizar_dashboard()

    def crear_interfaz(self):

        # ENCABEZADO

        tk.Label(
            self.ventana,
            text="ZEROCOOL CRM",
            bg="#102A43",
            fg="#FF3333",
            font=("Arial", 27, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            self.ventana,
            text="DASHBOARD COMERCIAL",
            bg="#102A43",
            fg="white",
            font=("Arial", 13, "bold")
        ).pack(pady=(0, 20))

        # CONTENEDOR DE INDICADORES

        self.contenedor_kpi = tk.Frame(
            self.ventana,
            bg="#102A43"
        )

        self.contenedor_kpi.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.tarjetas = {}

        indicadores = [
            ("Clientes", "clientes"),
            ("Clientes activos", "clientes_activos"),
            ("Oportunidades", "oportunidades"),
            ("Oportunidades ganadas", "ganadas"),
            ("Valor ganado", "valor_ganado"),
            ("Pipeline comercial", "pipeline")
        ]

        for indice, (titulo, clave) in enumerate(indicadores):

            fila = indice // 3
            columna = indice % 3

            tarjeta = tk.Frame(
                self.contenedor_kpi,
                bg="#243B53",
                padx=15,
                pady=15,
                highlightbackground="#526D82",
                highlightthickness=1
            )

            tarjeta.grid(
                row=fila,
                column=columna,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            tk.Label(
                tarjeta,
                text=titulo.upper(),
                bg="#243B53",
                fg="#BCCCDC",
                font=("Arial", 10, "bold")
            ).pack(pady=(5, 10))

            valor = tk.Label(
                tarjeta,
                text="0",
                bg="#243B53",
                fg="white",
                font=("Arial", 23, "bold")
            )

            valor.pack(pady=5)

            self.tarjetas[clave] = valor

        for columna in range(3):
            self.contenedor_kpi.grid_columnconfigure(
                columna,
                weight=1
            )

        # GRÁFICO DE PIPELINE

        grafico_frame = tk.LabelFrame(
            self.ventana,
            text=" PIPELINE POR ESTADO ",
            bg="#243B53",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        grafico_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        self.canvas = tk.Canvas(
            grafico_frame,
            bg="#243B53",
            highlightthickness=0,
            height=230
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # BOTONES

        botones = tk.Frame(
            self.ventana,
            bg="#102A43"
        )

        botones.pack(
            fill="x",
            padx=30,
            pady=15
        )

        tk.Button(
            botones,
            text="GESTIONAR CLIENTES",
            bg="#2874A6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            pady=12,
            command=self.abrir_clientes
        ).pack(side="left", padx=5)

        tk.Button(
            botones,
            text="ACTUALIZAR INDICADORES",
            bg="#16803C",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            pady=12,
            command=self.actualizar_dashboard
        ).pack(side="left", padx=5)

        tk.Label(
            self.ventana,
            text="ZEROCOOL CRM | PostgreSQL",
            bg="#102A43",
            fg="#BCCCDC",
            font=("Arial", 9)
        ).pack(pady=8)

    def formatear_dinero(self, valor):

        return "$" + f"{valor:,.0f}".replace(",", ".")

    def actualizar_dashboard(self):

        datos = obtener_indicadores()

        if datos is None:

            messagebox.showerror(
                "Error",
                "No se pudieron cargar los indicadores."
            )

            return

        self.tarjetas["clientes"].config(
            text=str(datos["clientes"])
        )

        self.tarjetas["clientes_activos"].config(
            text=str(datos["clientes_activos"])
        )

        self.tarjetas["oportunidades"].config(
            text=str(datos["oportunidades"])
        )

        self.tarjetas["ganadas"].config(
            text=str(datos["ganadas"])
        )

        self.tarjetas["valor_ganado"].config(
            text=self.formatear_dinero(datos["valor_ganado"])
        )

        self.tarjetas["pipeline"].config(
            text=self.formatear_dinero(datos["pipeline"])
        )

        self.dibujar_pipeline()

    def dibujar_pipeline(self):

        self.canvas.delete("all")

        datos = obtener_pipeline_por_estado()

        if not datos:

            self.canvas.create_text(
                300,
                100,
                text="No hay oportunidades registradas.",
                fill="white",
                font=("Arial", 12)
            )

            return

        ancho = max(self.canvas.winfo_width(), 600)

        max_valor = max(
            (float(fila[2]) for fila in datos),
            default=0
        )

        if max_valor == 0:
            max_valor = 1

        colores = {
            "Nueva": "#2874A6",
            "En proceso": "#E6A23C",
            "Ganada": "#16803C",
            "Perdida": "#C0392B"
        }

        inicio_y = 35
        alto_barra = 28
        separacion = 45

        for indice, (estado, cantidad, valor) in enumerate(datos):

            y = inicio_y + indice * separacion

            self.canvas.create_text(
                15,
                y + 12,
                text=estado,
                fill="white",
                anchor="w",
                font=("Arial", 10, "bold")
            )

            x_inicio = 130
            x_final = ancho - 190

            longitud = (
                (float(valor) / max_valor)
                * (x_final - x_inicio)
            )

            self.canvas.create_rectangle(
                x_inicio,
                y,
                x_inicio + longitud,
                y + alto_barra,
                fill=colores.get(estado, "#526D82"),
                outline=""
            )

            texto = (
                f"{cantidad} oportunidades | "
                f"{self.formatear_dinero(valor)}"
            )

            self.canvas.create_text(
                x_final + 10,
                y + 12,
                text=texto,
                fill="white",
                anchor="w",
                font=("Arial", 9)
            )

    def abrir_clientes(self):

        ventana_clientes = tk.Toplevel(self.ventana)

        ClientesApp(ventana_clientes)


def iniciar_dashboard():

    ventana = tk.Tk()

    app = DashboardApp(ventana)

    ventana.mainloop()
