from pathlib import Path
import json
from tkinter import Tk, Canvas, Button, PhotoImage, StringVar, ttk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path('../assets')

def obtener_preguntas():
    with open('data/preguntas.json', 'r', encoding='utf-8') as file:
        datos = json.load(file)
    preguntas = datos['preguntas']
    return preguntas

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class CuestionarioApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1009x697")
        self.root.configure(bg="#82C0CC")

        # Preguntas a mostrar en el cuestionario
        self.preguntas = obtener_preguntas()
        self.index_pregunta = 0
        self.index_respuesta = 0

        # Alternativas marcadas por el usuario
        self.diccionario_alternativas = {
            "Desinteresado" : 1,
            "Algo" : 2,
            "Moderado" : 3,
            "Mucho" : 4,
            "Interesado" : 5 
        }

        self.variables_sistema_difuso = [
            'deportes',
            'artes',
            'ciencia',
            'tecnologia',
            'creatividad',
            'social',
            'autoexpresion',
            'competitividad',
            'independencia',
            'coordinacion',
            'creatividad_habilidad',
            'tecnologia_habilidad',
            'resolucion_problemas',
            'expresion_artistica',
            'trabajo_equipo',
            'debates',
            'actividades_grupales',
            'colaboracion',
            'compartir_ideas',
            'competir',
            'aprendizaje',
            'autoexpresion_valor',
            'superar_limites',
            'liberar_energia',
            'desconectar',
            'creatividad_relajacion',
            'deportes_relajacion',
            'mejorar_habilidades',
            'desarrollo_liderazgo',
            'equilibrio_salud',
            'aprender_nueva_habilidad',
            'crecimiento_personal'
        ]
        
        self.respuestas_usuario = []
        self.diccionario_respuestas = {}

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
        self.imagen_deporte        = PhotoImage(file=relative_to_assets("img_deporte.png"))

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
        self.contenedor_imagen = self.canvas.create_image(504.0, 303.0, image=self.imagen_deporte)

        # Texto de instrucciones
        self.texto_instrucciones = self.canvas.create_text(
            100.0, 410.0,
            anchor="nw",
            text="Marca la alternativa según tu grado de interés:",
            fill="#FFFFFF",
            font=('Inter', 16 * -1, 'bold')
        )


        # Alternativas
        #self.alternativa_Desinteresado = self.canvas.create_text(117.0, 468.0, anchor="nw", text="Desinteresado", fill="#FFFFFF", font=('Inter', 16 * -1, 'bold'))
        #self.alternativa_Algo = self.canvas.create_text(326.0, 468.0, anchor="nw", text="Algo",          fill="#FFFFFF", font=('Inter', 16 * -1, 'bold'))
        #self.alternativa_Moderado = self.canvas.create_text(475.0, 468.0, anchor="nw", text="Moderado",      fill="#FFFFFF", font=('Inter', 16 * -1, 'bold'))
        #self.alternativa_Mucho = self.canvas.create_text(672.0, 468.0, anchor="nw", text="Mucho",         fill="#FFFFFF", font=('Inter', 16 * -1, 'bold'))
        #self.alternativ_Interesado = self.canvas.create_text(825.0, 468.0, anchor="nw", text="Interesado",    fill="#FFFFFF", font=('Inter', 16 * -1, 'bold'))

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

    def guardar_alternativa(self):
        #clave_alternativa = self.alternativa_seleccionada.get()
        #if clave_alternativa in self.diccionario_alternativas:
        #    clave_variable_sistema = self.variables_sistema_difuso[self.index_pregunta]
        #    self.respuestas_usuario[clave_variable_sistema] = self.diccionario_alternativas[clave_alternativa]
        
        #if self.respuestas_usuario:
        #    self.respuestas_usuario[self.index_respuesta] = self.diccionario_alternativas[self.alternativa_seleccionada.get()]
        #else:
        #    self.respuestas_usuario.append(self.diccionario_alternativas[self.alternativa_seleccionada.get()])

        #if len(self.respuestas_usuario)-1 > self.index_pregunta:
        if len(self.respuestas_usuario) > self.index_respuesta:
            self.respuestas_usuario[self.index_respuesta] = self.diccionario_alternativas[self.alternativa_seleccionada.get()]
        else:
            self.respuestas_usuario.append(self.diccionario_alternativas[self.alternativa_seleccionada.get()])


    def alternativa_anterior(self):
        #valor_alternativa = self.respuestas_usuario[self.variables_sistema_difuso[self.index_pregunta]]
        #self.alternativa_seleccionada.set(list(self.diccionario_alternativas.keys())[list(self.diccionario_alternativas.values()).index(valor_alternativa)])
        #self.respuestas_usuario[clave_variable_sistema] = self.diccionario_alternativas[clave_alternativa]
        print(list(self.diccionario_alternativas.keys())[list(self.diccionario_alternativas.values()).index(self.respuestas_usuario[self.index_respuesta])])
        self.alternativa_seleccionada.set(list(self.diccionario_alternativas.keys())[list(self.diccionario_alternativas.values()).index(self.respuestas_usuario[self.index_respuesta])])

    def siguiente_pregunta(self):
        """Muestra la siguiente pregunta si existe."""
        if len(self.respuestas_usuario) > self.index_respuesta:
            print(self.index_respuesta)
            self.index_respuesta += 1
            self.alternativa_seleccionada.set(list(self.diccionario_alternativas.keys())[list(self.diccionario_alternativas.values()).index(self.respuestas_usuario[self.index_respuesta])])

        if self.index_pregunta < len(self.preguntas) - 1 and self.alternativa_seleccionada.get():
            self.guardar_alternativa()
            self.index_pregunta += 1
            self.index_respuesta += 1
            self.actualizar_pregunta()
            print(f"Index aumento: {self.index_respuesta}")
            print(self.respuestas_usuario)
            self.alternativa_seleccionada.set(list(self.diccionario_alternativas.keys())[list(self.diccionario_alternativas.values()).index(self.respuestas_usuario[self.index_respuesta-1])])
            print(f"ALTERNATIVA SELECCIONADA: {list(self.diccionario_alternativas.keys())[list(self.diccionario_alternativas.values()).index(self.respuestas_usuario[self.index_respuesta-1])]}")
            #self.btn_siguiente.place(x=615.0, y=595.0, width=156.0, height=38.0)
        print(len(self.respuestas_usuario), self.index_pregunta)

        if self.index_pregunta == len(self.preguntas) - 1:
            self.btn_siguiente.place_forget()
            self.btn_enviar.place(x=420.0, y=595.0, width=156.0, height=38.0)
        
        self.alternativa_seleccionada.set("")
        #print(self.respuestas_usuario)


    def anterior_pregunta(self):
        """Muestra la pregunta anterior si existe."""

        if self.index_pregunta > 0:
            self.index_pregunta -= 1
            self.index_respuesta -= 1
            self.actualizar_pregunta()
            self.alternativa_anterior()
            print(self.index_respuesta)
            self.btn_siguiente.place(x=615.0, y=595.0, width=156.0, height=38.0)
        
        if self.index_pregunta != len(self.preguntas) - 1:
            self.btn_enviar.place_forget()
            #self.self.btn_siguiente.place(x=615.0, y=595.0, width=156.0, height=38.0)


    def ocultar_preguntas(self):
        self.canvas.itemconfig(self.contenedor_marco_contador, state="hidden")
        self.canvas.itemconfig(self.titulo_contador_pregunta, state="hidden")
        self.canvas.itemconfig(self.contador_pregunta, state="hidden")
        self.canvas.itemconfig(self.contador_pregunta_total, state="hidden")
        self.canvas.itemconfig(self.numero_pregunta, state="hidden")
        self.canvas.itemconfig(self.texto_pregunta, state="hidden")
        self.canvas.itemconfig(self.contenedor_imagen, state="hidden")
        self.canvas.itemconfig(self.texto_instrucciones, state="hidden")

        #Alternativas
        self.canvas.itemconfig(self.contenedor_Desinteresado, state="hidden")
        self.canvas.itemconfig(self.contenedor_Algo, state="hidden")
        self.canvas.itemconfig(self.contenedor_Moderado, state="hidden")
        self.canvas.itemconfig(self.contenedor_Mucho, state="hidden")
        self.canvas.itemconfig(self.contenedor_Interesado, state="hidden")
        
        #self.canvas.itemconfig(self.alternativa_Desinteresado, state="hidden")
        #self.canvas.itemconfig(self.alternativa_Algo, state="hidden")
        #self.canvas.itemconfig(self.alternativa_Moderado, state="hidden")
        #self.canvas.itemconfig(self.alternativa_Mucho, state="hidden")
        #self.canvas.itemconfig(self.alternativ_Interesado, state="hidden")
    
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

        #self.canvas.itemconfig(self.alternativa_Desinteresado, state="normal")
        #self.canvas.itemconfig(self.alternativa_Algo, state="normal")
        #self.canvas.itemconfig(self.alternativa_Moderado, state="normal")
        #self.canvas.itemconfig(self.alternativa_Mucho, state="normal")
        #self.canvas.itemconfig(self.alternativ_Interesado, state="normal")

    def enviar_respuestas(self):
        """Envía las respuestas (simulado aquí)."""
        self.ocultar_preguntas()

        self.btn_anterior.place_forget()
        self.btn_enviar.place_forget()
        self.btn_siguiente.place_forget()
        self.btn_reiniciar.place(x=807.0, y=595.0, width=156.0, height=38.0)

        self.respuesta_actividad = self.canvas.create_text(
            505.0, 340.0,
            text="¡Gracias por enviar tus respuestas!",
            fill="#FFFFFF",
            font=("Inter", 24 * -1, 'bold'),
            anchor="center"
        )

        self.guardar_alternativa()
        
        print("Respuestas enviadas")
        print(self.respuestas_usuario)

    
    def reiniciar_cuestionario(self):
        self.mostrar_preguntas()

        self.btn_anterior.place(x=225.0, y=595.0, width=156.0, height=38.0)
        self.btn_siguiente.place(x=615.0, y=595.0, width=156.0, height=38.0)
        self.btn_enviar.place_forget()
        self.btn_reiniciar.place_forget()
        self.canvas.itemconfig(self.respuesta_actividad, state="hidden")
        self.index_pregunta = 0
        self.actualizar_pregunta()
        self.respuestas_usuario.clear()
        print(self.respuestas_usuario)

if __name__ == "__main__":
    window = Tk()
    app = CuestionarioApp(window)
    window.resizable(False, False)
    window.mainloop()
