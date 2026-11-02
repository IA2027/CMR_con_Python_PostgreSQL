
import tkinter as tk
from tkinter import ttk, messagebox

from modules.clientes_db import (
    listar_clientes,
    obtener_empresas,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente
)


class ClientesApp:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title("ZEROCOOL CRM - Gestión de clientes")
        self.ventana.geometry("1250x720")
        self.ventana.minsize(1050, 650)
        self.ventana.configure(bg="#102A43")

        self.cliente_seleccionado = None
        self.empresas = {}

        self.crear_estilos()
        self.crear_interfaz()
        self.cargar_empresas()
        self.cargar_clientes()

    def crear_estilos(self):

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#172B4D",
            rowheight=30,
            fieldbackground="#FFFFFF",
            font=("Arial", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            background="#243B53",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold")
        )

        estilo.map(
            "Treeview",
            background=[("selected", "#2874A6")],
            foreground=[("selected", "#FFFFFF")]
        )

        estilo.configure(
            "TCombobox",
            padding=6
        )

    def crear_interfaz(self):

        # TÍTULO PRINCIPAL

        titulo = tk.Label(
            self.ventana,
            text="ZEROCOOL CRM",
            bg="#102A43",
            fg="#FF3333",
            font=("Arial", 25, "bold")
        )

        titulo.pack(pady=(15, 5))

        subtitulo = tk.Label(
            self.ventana,
            text="GESTIÓN DE CLIENTES",
            bg="#102A43",
            fg="white",
            font=("Arial", 12, "bold")
        )

        subtitulo.pack(pady=(0, 15))

        # CONTENEDOR PRINCIPAL

        contenedor = tk.Frame(
            self.ventana,
            bg="#102A43"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # FORMULARIO

        formulario = tk.LabelFrame(
            contenedor,
            text=" DATOS DEL CLIENTE ",
            bg="#243B53",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        formulario.pack(fill="x", pady=10)

        self.campos = {}

        campos = [
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Email", "email"),
            ("Teléfono", "telefono"),
            ("Dirección", "direccion")
        ]

        for indice, (etiqueta, clave) in enumerate(campos):

            fila = indice // 3
            columna = (indice % 3) * 2

            tk.Label(
                formulario,
                text=etiqueta,
                bg="#243B53",
                fg="white",
                font=("Arial", 10)
            ).grid(
                row=fila * 2,
                column=columna,
                sticky="w",
                padx=8,
                pady=5
            )

            entrada = tk.Entry(
                formulario,
                font=("Arial", 11),
                width=25
            )

            entrada.grid(
                row=fila * 2 + 1,
                column=columna,
                padx=8,
                pady=5,
                sticky="ew"
            )

            self.campos[clave] = entrada

        # ESTADO

        tk.Label(
            formulario,
            text="Estado",
            bg="#243B53",
            fg="white"
        ).grid(row=4, column=0, sticky="w", padx=8, pady=5)

        self.estado = ttk.Combobox(
            formulario,
            values=["Activo", "Inactivo", "Potencial"],
            state="readonly",
            width=22
        )

        self.estado.grid(
            row=5,
            column=0,
            padx=8,
            pady=5,
            sticky="w"
        )

        self.estado.set("Activo")

        # EMPRESA

        tk.Label(
            formulario,
            text="Empresa",
            bg="#243B53",
            fg="white"
        ).grid(row=4, column=2, sticky="w", padx=8, pady=5)

        self.empresa = ttk.Combobox(
            formulario,
            state="readonly",
            width=25
        )

        self.empresa.grid(
            row=5,
            column=2,
            padx=8,
            pady=5,
            sticky="w"
        )

        # BOTONES

        botones = tk.Frame(
            contenedor,
            bg="#102A43"
        )

        botones.pack(fill="x", pady=10)

        self.crear_boton(
            botones,
            "GUARDAR CLIENTE",
            "#16803C",
            self.guardar_cliente
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones,
            "MODIFICAR",
            "#2874A6",
            self.modificar_cliente
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones,
            "ELIMINAR",
            "#C0392B",
            self.borrar_cliente
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones,
            "LIMPIAR",
            "#526D82",
            self.limpiar_formulario
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones,
            "ACTUALIZAR TABLA",
            "#526D82",
            self.cargar_clientes
        ).pack(side="right", padx=5)

        # BUSCADOR

        buscador = tk.Frame(
            contenedor,
            bg="#102A43"
        )

        buscador.pack(fill="x", pady=10)

        tk.Label(
            buscador,
            text="BUSCAR CLIENTE:",
            bg="#102A43",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)

        self.buscar = tk.Entry(
            buscador,
            font=("Arial", 11),
            width=35
        )

        self.buscar.pack(side="left", padx=5)

        self.crear_boton(
            buscador,
            "BUSCAR",
            "#2874A6",
            self.buscar_cliente
        ).pack(side="left", padx=5)

        self.crear_boton(
            buscador,
            "MOSTRAR TODOS",
            "#526D82",
            self.cargar_clientes
        ).pack(side="left", padx=5)

        # TABLA DE CLIENTES

        tabla_frame = tk.Frame(
            contenedor,
            bg="#102A43"
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columnas = (
            "ID",
            "Nombre",
            "Apellido",
            "Email",
            "Telefono",
            "Estado",
            "Empresa"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        anchos = {
            "ID": 55,
            "Nombre": 120,
            "Apellido": 120,
            "Email": 200,
            "Telefono": 120,
            "Estado": 100,
            "Empresa": 150
        }

        for columna in columnas:

            self.tabla.heading(
                columna,
                text=columna
            )

            self.tabla.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scroll.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_cliente
        )

        self.total_label = tk.Label(
            contenedor,
            text="Total de clientes: 0",
            bg="#102A43",
            fg="white",
            font=("Arial", 11, "bold")
        )

        self.total_label.pack(
            anchor="w",
            pady=5
        )

    def crear_boton(self, padre, texto, color, comando):

        return tk.Button(
            padre,
            text=texto,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=12,
            pady=9,
            cursor="hand2",
            command=comando
        )

    def cargar_empresas(self):

        datos = obtener_empresas()

        self.empresas = {}

        nombres = ["Sin empresa"]

        for id_empresa, nombre in datos:

            self.empresas[nombre] = id_empresa
            nombres.append(nombre)

        self.empresa["values"] = nombres
        self.empresa.set("Sin empresa")

    def cargar_clientes(self):

        self.mostrar_resultados("")

    def buscar_cliente(self):

        filtro = self.buscar.get().strip()

        self.mostrar_resultados(filtro)

    def mostrar_resultados(self, filtro):

        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        clientes = listar_clientes(filtro)

        for cliente in clientes:

            self.tabla.insert(
                "",
                "end",
                values=tuple(
                    valor if valor is not None else ""
                    for valor in cliente
                )
            )

        self.total_label.config(
            text=f"Total de clientes: {len(clientes)}"
        )

    def seleccionar_cliente(self, evento):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        datos = self.tabla.item(seleccion[0], "values")

        self.cliente_seleccionado = datos[0]

        valores = {
            "nombre": datos[1],
            "apellido": datos[2],
            "email": datos[3],
            "telefono": datos[4]
        }

        for clave, valor in valores.items():

            self.campos[clave].delete(0, tk.END)
            self.campos[clave].insert(0, valor)

        self.estado.set(datos[5] or "Activo")

        nombre_empresa = datos[6] or "Sin empresa"

        self.empresa.set(nombre_empresa)

        # La dirección no está incluida en la tabla de consulta.
        # Se mantiene vacía hasta que se agregue una consulta detallada.

    def obtener_datos_formulario(self):

        nombre = self.campos["nombre"].get().strip()
        apellido = self.campos["apellido"].get().strip()
        email = self.campos["email"].get().strip()
        telefono = self.campos["telefono"].get().strip()
        direccion = self.campos["direccion"].get().strip()
        estado = self.estado.get()

        nombre_empresa = self.empresa.get()

        id_empresa = self.empresas.get(nombre_empresa)

        if not nombre or not apellido:

            messagebox.showwarning(
                "Datos incompletos",
                "El nombre y el apellido son obligatorios."
            )

            return None

        return (
            nombre,
            apellido,
            email or None,
            telefono or None,
            direccion or None,
            estado,
            id_empresa
        )

    def guardar_cliente(self):

        datos = self.obtener_datos_formulario()

        if datos is None:
            return

        resultado = crear_cliente(*datos)

        if resultado:

            messagebox.showinfo(
                "ZEROCOOL CRM",
                "Cliente registrado correctamente."
            )

            self.limpiar_formulario()
            self.cargar_clientes()

        else:

            messagebox.showerror(
                "Error",
                "No se pudo registrar el cliente. "
                "Revisá la terminal para ver el detalle."
            )

    def modificar_cliente(self):

        if self.cliente_seleccionado is None:

            messagebox.showwarning(
                "Seleccionar cliente",
                "Primero seleccioná un cliente de la tabla."
            )

            return

        datos = self.obtener_datos_formulario()

        if datos is None:
            return

        resultado = actualizar_cliente(
            self.cliente_seleccionado,
            *datos
        )

        if resultado:

            messagebox.showinfo(
                "ZEROCOOL CRM",
                "Cliente actualizado correctamente."
            )

            self.limpiar_formulario()
            self.cargar_clientes()

        else:

            messagebox.showerror(
                "Error",
                "No se pudo actualizar el cliente. "
                "Revisá la terminal."
            )

    def borrar_cliente(self):

        if self.cliente_seleccionado is None:

            messagebox.showwarning(
                "Seleccionar cliente",
                "Primero seleccioná un cliente."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de eliminar este cliente?\n\n"
            "La operación puede estar bloqueada si tiene "
            "interacciones u oportunidades relacionadas."
        )

        if not confirmar:
            return

        resultado = eliminar_cliente(
            self.cliente_seleccionado
        )

        if resultado:

            messagebox.showinfo(
                "ZEROCOOL CRM",
                "Cliente eliminado correctamente."
            )

            self.limpiar_formulario()
            self.cargar_clientes()

        else:

            messagebox.showerror(
                "Error",
                "No se pudo eliminar el cliente. "
                "Puede tener registros relacionados. "
                "Revisá la terminal."
            )

    def limpiar_formulario(self):

        for entrada in self.campos.values():

            entrada.delete(0, tk.END)

        self.estado.set("Activo")
        self.empresa.set("Sin empresa")

        self.cliente_seleccionado = None

        for seleccion in self.tabla.selection():
            self.tabla.selection_remove(seleccion)


def iniciar_app():

    ventana = tk.Tk()

    app = ClientesApp(ventana)

    ventana.mainloop()
