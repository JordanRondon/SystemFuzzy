from pathlib import Path
import json
from tkinter import Tk, Canvas, Button, PhotoImage, StringVar, ttk
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path('../assets')

ASSETS_PATH_IMAGEN = OUTPUT_PATH / Path('../assets/imagenes')

def obtener_preguntas():
    with open('data/preguntas.json', 'r', encoding='utf-8') as file:
        datos = json.load(file)
    preguntas = datos['preguntas']
    return preguntas

def obtener_imagenes():
    with open('data/preguntas.json', 'r', encoding='utf-8') as file:
        datos = json.load(file)
    imagenes = datos['imagenes']
    return imagenes

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def relative_to_assets_imagen(path: str) -> Path:
    return ASSETS_PATH_IMAGEN / Path(path)

class CuestionarioApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1009x697")
        self.root.configure(bg="#82C0CC")

        # Preguntas a mostrar en el cuestionario
        self.preguntas = obtener_preguntas()
        self.index_pregunta = 0

        self.imagenes = obtener_imagenes()
        self.index_imagenes = 0

        self.respuesta_usuario = []
        self.index_respuesta = 0

        self.alternativas = [
            "Desinteresado",
            "Algo",
            "Moderado",
            "Mucho",
            "Interesado"
        ]

        # Alternativas marcadas por el usuario
        self.respuestas_usuario = []

        # Canvas principal
        self.canvas = Canvas(
            root,
            bg="#82C0CC",
            height=697,
            width=1009,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Cargar imágenes
        self.imagen_marco_pregunta = PhotoImage(file=relative_to_assets("marco_pregunta.png"))
        self.imagen_marco_contador = PhotoImage(file=relative_to_assets("marco_contador.png"))
        self.imagen_imagen        = PhotoImage(file=relative_to_assets_imagen(self.imagenes[self.index_imagenes]))

        # Configuración inicial del marco de la pregunta y contador
        self.contenedor_marco_pregunta = self.canvas.create_image(505.0, 340.0, image=self.imagen_marco_pregunta)
        self.contenedor_marco_contador = self.canvas.create_image(881.0, 109.0, image=self.imagen_marco_contador)

        # Título
        self.canvas.create_text(
            174.0, 36.0,
            anchor="nw",
            text="TEST PARA ACTIVIDADES EXTRACURRICULARES",
            fill="#16697A",
            font=('Inter', 28 * -1, 'bold')
        )

        # Linea Titulo
        self.linea_titulo = self.canvas.create_line(
            175.0, 70.0, 854, 70, fill = "#16697A", width = 3
        )

        # Titulo Contador de pregunta
        self.titulo_contador_pregunta = self.canvas.create_text(
            813.0,
            100.0,
            anchor="nw",
            text="Pregunta:",
            fill="#FFFFFF",
            font=('Inter', 16 * -1, 'bold')
        )

        # Contador de pregunta
        self.contador_pregunta = self.canvas.create_text(
            894.0, 100.0,
            anchor="nw",
            text=f"{self.index_pregunta + 1:02}",
            fill="#FFFFFF",
            font=('Inter', 16 * -1, 'bold')
        )
        self.contador_pregunta_total = self.canvas.create_text(
            920.0, 100.0,
            anchor="nw",
            text=f"/ {len(self.preguntas)}",
            fill="#FFFFFF",
            font=('Inter', 16 * -1, 'bold')
        )

        # Label de la pregunta
        self.numero_pregunta = self.canvas.create_text(
            65.0, 152.0,
            anchor="nw",
            text=f"{self.index_pregunta + 1:02}.",
            fill="#FFFFFF",
            font=("Inter", 20 * -1)
        )
        self.texto_pregunta = self.canvas.create_text(
            100.0, 152.0,
            anchor="nw",
            text=self.preguntas[self.index_pregunta],
            fill="#FFFFFF",
            font=("Inter", 20 * -1),
            width=870
        )

        # Imagen de ejemplo
        self.contenedor_imagen = self.canvas.create_image(504.0, 303.0, image=self.imagen_imagen)

        # Texto de instrucciones
        self.texto_instrucciones = self.canvas.create_text(
            100.0, 410.0,
            anchor="nw",
            text="Marca la alternativa según tu grado de interés:",
            fill="#FFFFFF",
            font=('Inter', 16 * -1, 'bold')
        )

        # Variable para guardar la alternativa seleccionada por el usuario
        self.alternativa_seleccionada = StringVar()

        # Estilo personalizado para Radiobuttons
        self.style = ttk.Style()
        self.style.configure("TRadiobutton",
                             background="#489FB5",
                             foreground="#FFFFFF",
                             font=('Inter', 14, 'bold'),
                             padding=5)

        # Alternativas
        self.contenedor_Desinteresado = self.create_radiobutton("Desinteresado", 100.0)
        self.contenedor_Algo = self.create_radiobutton("Algo", 310.0)
        self.contenedor_Moderado = self.create_radiobutton("Moderado", 455.0)
        self.contenedor_Mucho = self.create_radiobutton("Mucho", 653.0)
        self.contenedor_Interesado = self.create_radiobutton("Interesado", 805.0)


        # Botones de control
        self.btn_imagen_siguiente = PhotoImage(file=relative_to_assets("btn_siguiente.png"))
        self.btn_siguiente = Button(
            image=self.btn_imagen_siguiente,
            borderwidth=0,
            highlightthickness=0,
            command=self.siguiente_pregunta,
            relief="flat"
        )
        self.btn_siguiente.place(x=615.0, y=595.0, width=156.0, height=38.0)

        self.btn_imagen_reiniciar = PhotoImage(file=relative_to_assets("btn_reiniciar.png"))
        self.btn_reiniciar = Button(
            image=self.btn_imagen_reiniciar,
            borderwidth=0,
            highlightthickness=0,
            command=self.reiniciar_cuestionario,
            relief="flat"
        )
        self.btn_reiniciar.place(x=807.0, y=595.0, width=156.0, height=38.0)
        self.btn_reiniciar.place_forget()

        self.btn_imagen_anterior = PhotoImage(file=relative_to_assets("btn_anterior.png"))
        self.btn_anterior = Button(
            image=self.btn_imagen_anterior,
            borderwidth=0,
            highlightthickness=0,
            command=self.anterior_pregunta,
            relief="flat"
        )
        self.btn_anterior.place(x=225.0, y=595.0, width=156.0, height=38.0)

        self.btn_imagen_enviar = PhotoImage(file=relative_to_assets("btn_enviar.png"))
        self.btn_enviar = Button(
            image=self.btn_imagen_enviar,
            borderwidth=0,
            highlightthickness=0,
            command=self.enviar_respuestas,
            relief="flat"
        )
        self.btn_enviar.place(x=420.0, y=595.0, width=156.0, height=38.0)
        self.btn_enviar.place_forget()

        print(len(self.respuesta_usuario), self.index_respuesta)

    def create_radiobutton(self, text, x_position):
        rb = ttk.Radiobutton(
            self.canvas,
            text=text,
            variable=self.alternativa_seleccionada,
            value=text,
            style="TRadiobutton"
        )

        return self.canvas.create_window(x_position, 468, window=rb, anchor="nw")

    def actualizar_pregunta(self):
        """Actualiza el texto de la pregunta, numero de pregunta y el contador."""
        self.canvas.itemconfig(self.texto_pregunta, text=self.preguntas[self.index_pregunta])
        self.canvas.itemconfig(self.contador_pregunta, text=f"{self.index_pregunta + 1:02}")
        self.canvas.itemconfig(self.numero_pregunta, text=f"{self.index_pregunta + 1:02}.")

        # Actualizar imagen
        # ruta_imagen = relative_to_assets_imagen(self.imagenes[self.index_imagenes])
        # imagen_pillow = Image.open(ruta_imagen)
        # nueva_imagen = ImageTk.PhotoImage(imagen_pillow)
        # # Actualizar la imagen en el Canvas
        # self.canvas.itemconfig(self.contenedor_imagen, image=nueva_imagen)
        # # Mantener una referencia a la nueva imagen para evitar que se recoja como basura
        # self.imagen_imagen = nueva_imagen

        # si existe una respuesta seleccionada se vuleve a pintar 
        if len(self.respuesta_usuario) > self.index_respuesta:
            valor_alternativa_siguiente = self.respuesta_usuario[self.index_respuesta]
            self.alternativa_seleccionada.set(valor_alternativa_siguiente)

    def siguiente_pregunta(self):
        """Muestra la siguiente pregunta si existe."""
        if self.index_pregunta < len(self.preguntas) - 1 and self.alternativa_seleccionada.get() != '':
            self.index_pregunta += 1
            self.index_respuesta += 1

            # si el indice supera la cantidad de elementos del arreglo respuesta_usuario se agrega un elemento mas
            if len(self.respuesta_usuario) < self.index_respuesta or len(self.respuesta_usuario) == 0:
                self.respuesta_usuario.append(self.alternativa_seleccionada.get())

            # si el total del arreglo de respuesta_usuario es mayor al indice actual del respuesta se sobre escribe la seleccion de la alternativa
            if len(self.respuesta_usuario) >= self.index_respuesta:
                self.respuesta_usuario[self.index_respuesta-1] = self.alternativa_seleccionada.get()

            self.alternativa_seleccionada.set("")

            print(len(self.respuesta_usuario), self.index_respuesta)
            print(self.respuesta_usuario)
            print(self.alternativa_seleccionada.get())
            
            self.actualizar_pregunta()

        # validacion para habilitar el boton enviar en la ultima pregunta
        if self.index_pregunta == len(self.preguntas) - 1:
            self.btn_enviar.place(x=420.0, y=595.0, width=156.0, height=38.0)


    def anterior_pregunta(self):
        """Muestra la pregunta anterior si existe."""
        if self.index_pregunta > 0:
            self.index_pregunta -= 1
            self.index_respuesta -= 1
            self.actualizar_pregunta()

            print(len(self.respuesta_usuario), self.index_respuesta)
            print(self.respuesta_usuario)
            print(self.respuesta_usuario[self.index_respuesta])

        # validacion para deshabilitar el boton enviar antes de la ultima pregunta
        if self.index_pregunta != len(self.preguntas) - 1:
            self.btn_enviar.place_forget()


    def ocultar_preguntas(self):
        self.canvas.itemconfig(self.contenedor_marco_contador, state="hidden")
        self.canvas.itemconfig(self.titulo_contador_pregunta, state="hidden")
        self.canvas.itemconfig(self.contador_pregunta, state="hidden")
        self.canvas.itemconfig(self.contador_pregunta_total, state="hidden")
        self.canvas.itemconfig(self.numero_pregunta, state="hidden")
        self.canvas.itemconfig(self.texto_pregunta, state="hidden")
        self.canvas.itemconfig(self.contenedor_imagen, state="hidden")
        self.canvas.itemconfig(self.texto_instrucciones, state="hidden")

        self.canvas.itemconfig(self.contenedor_Desinteresado, state="hidden")
        self.canvas.itemconfig(self.contenedor_Algo, state="hidden")
        self.canvas.itemconfig(self.contenedor_Moderado, state="hidden")
        self.canvas.itemconfig(self.contenedor_Mucho, state="hidden")
        self.canvas.itemconfig(self.contenedor_Interesado, state="hidden")

    def mostrar_preguntas(self):
        self.canvas.itemconfig(self.contenedor_marco_contador, state="normal")
        self.canvas.itemconfig(self.titulo_contador_pregunta, state="normal")
        self.canvas.itemconfig(self.contador_pregunta, state="normal")
        self.canvas.itemconfig(self.contador_pregunta_total, state="normal")
        self.canvas.itemconfig(self.numero_pregunta, state="normal")
        self.canvas.itemconfig(self.texto_pregunta, state="normal")
        self.canvas.itemconfig(self.contenedor_imagen, state="normal")
        self.canvas.itemconfig(self.texto_instrucciones, state="normal")

        self.canvas.itemconfig(self.contenedor_Desinteresado, state="normal")
        self.canvas.itemconfig(self.contenedor_Algo, state="normal")
        self.canvas.itemconfig(self.contenedor_Moderado, state="normal")
        self.canvas.itemconfig(self.contenedor_Mucho, state="normal")
        self.canvas.itemconfig(self.contenedor_Interesado, state="normal")

    def enviar_respuestas(self):
        """Envía las respuestas (simulado aquí)."""
        self.ocultar_preguntas()

        self.btn_anterior.place_forget()
        self.btn_enviar.place_forget()
        self.btn_siguiente.place_forget()
        self.btn_reiniciar.place(x=807.0, y=595.0, width=156.0, height=38.0)

        self.respuesta_usuario.append(self.alternativa_seleccionada.get())

        self.respuesta_actividad = self.canvas.create_text(
            505.0, 340.0,
            text="¡Gracias por enviar tus respuestas!",
            fill="#FFFFFF",
            font=("Inter", 24 * -1, 'bold'),
            anchor="center"
        )

        print(len(self.respuesta_usuario), self.index_respuesta)
        print(self.respuesta_usuario)
        print(self.alternativa_seleccionada.get())

        print("Respuestas enviadas")


    def reiniciar_cuestionario(self):
        self.mostrar_preguntas()

        self.btn_anterior.place(x=225.0, y=595.0, width=156.0, height=38.0)
        self.btn_siguiente.place(x=615.0, y=595.0, width=156.0, height=38.0)
        self.btn_enviar.place_forget()
        self.btn_reiniciar.place_forget()
        self.canvas.itemconfig(self.respuesta_actividad, state="hidden")
        self.index_pregunta = 0
        self.respuesta_usuario.clear()
        self.index_respuesta = 0
        self.actualizar_pregunta()

if __name__ == "__main__":
    window = Tk()
    app = CuestionarioApp(window)
    window.resizable(False, False)
    window.mainloop()