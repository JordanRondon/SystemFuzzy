import json
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def obtener_datos_json(nombre: str):
    with open('data/preguntas.json', 'r', encoding='utf-8') as file:
        contenido_json = json.load(file)
    datos_extraidos = contenido_json[nombre]
    return datos_extraidos

##### Definición de las variables difusas para cada pregunta del cuestionario #####
variable_psicologica = obtener_datos_json("caracteristica_psicologica")

# Creación de antecedentes para el sistema difuso.
# Un 'Antecedent' representa una variable de entrada en el sistema difuso.
# El rango de valores posibles para cada antecedente es de 0 a 5, con un incremento de 1.
antecedentes = {variable: ctrl.Antecedent(np.arange(0, 5), variable) for variable in variable_psicologica}


# Definición de las variables difusas para cada variable de salida
actividad_extracurricular = obtener_datos_json("actividades")

# Creación de consecuencias para el sistema difuso.
# Un 'Consequent' representa una variable de salida en el sistema difuso.
# El rango de valores posibles para cada antecedente es de 0 a 10, con un incremento de 1.
consecuencias = {actividad: ctrl.Consequent(np.arange(0, 10), actividad) for actividad in actividad_extracurricular}

##### Definición de variables de pertinencia para cada antecedente y consecuencia #####

# Para cada antecedente en el sistema difuso, se definen las funciones de pertenencia.
# Los antecedentes son las variables de entrada del sistema, representando aspectos psicológicos del estudiante.
# Se asignan cinco funciones de pertenencia difusa ('totalmente_desinteresado', 'algo', 'moderado', 'mucho', 'totalmente_interesado') a cada antecedente.
# Estas funciones de pertenencia son de tipo triangular (trimf) y definen la relación entre los valores posibles
# de la variable antecedente y su grado de pertenencia a las categorías mencionadas.
# - 'totalmente_desinteresado': máximo entre [0, 0, 2], representando poco o ningún interés.
# - 'algo': máximo entre [1, 2, 3], representando un interés bajo.
# - 'moderado': máximo entre [2, 3, 4], representando un interés moderado.
# - 'mucho': máximo entre [3, 4, 5], representando un interés alto.
# - 'totalmente_interesado': máximo entre [4, 5, 5], representando el máximo interés.

for antecedente in antecedentes.values():
    antecedente['desinteresado'] = fuzz.trimf(antecedente.universe, [0, 0, 2])
    antecedente['algo'] = fuzz.trimf(antecedente.universe, [1, 2, 3])
    antecedente['moderado'] = fuzz.trimf(antecedente.universe, [2, 3, 4])
    antecedente['mucho'] = fuzz.trimf(antecedente.universe, [3, 4, 5])
    antecedente['interesado'] = fuzz.trimf(antecedente.universe, [4, 5, 5])


# Para cada consecuencia en el sistema difuso, se definen las funciones de pertenencia.
# Las consecuencias son las variables de salida del sistema, representando actividades extracurriculares.
# Se asignan tres funciones de pertenencia difusa ('bajo', 'medio', 'alto') a cada consecuencia.
# Estas funciones de pertenencia son de tipo triangular (trimf) y definen la relación entre los valores posibles
# de la consecuencia y su grado de pertenencia a las categorías 'bajo', 'medio' y 'alto'.
# - 'bajo' tiene un valor máximo entre [0, 0, 5], donde la pertenencia es máxima en 0.
# - 'medio' se extiende entre [0, 5, 10], con el valor máximo en 5.
# - 'alto' tiene un valor máximo entre [5, 10, 10], donde la pertenencia es máxima en 10.
for consecuencia in consecuencias.values():
    consecuencia['bajo'] = fuzz.trimf(consecuencia.universe, [0, 0, 5])
    consecuencia['medio'] = fuzz.trimf(consecuencia.universe, [0, 5, 10])
    consecuencia['alto'] = fuzz.trimf(consecuencia.universe, [5, 10, 10])


# Definimos las reglas difusas
reglas = [
    ############# Futbol ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['velocidad']['interesado']                | antecedentes['velocidad']['mucho']) &
        (antecedentes['fuerza']['interesado']                   | antecedentes['fuerza']['mucho']) &
        (antecedentes['agilidad']['interesado']                 | antecedentes['agilidad']['mucho']) &
        (antecedentes['coordinacion_inferior']['interesado']    | antecedentes['coordinacion_inferior']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['liderazgo']['interesado']                | antecedentes['liderazgo']['mucho']) &
        (antecedentes['responsabilidad']['interesado']          | antecedentes['responsabilidad']['mucho']) &
        (antecedentes['solucion_problemas']['interesado']       | antecedentes['solucion_problemas']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado']           | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['comunicacion']['interesado']             | antecedentes['comunicacion']['mucho']) &
        (antecedentes['cooperacion']['interesado']              | antecedentes['cooperacion']['mucho']) &
        (antecedentes['deporte_contacto']['interesado']         | antecedentes['deporte_contacto']['mucho']),
        consecuencias['futbol']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['velocidad']['moderado']                | antecedentes['velocidad']['algo']) &
        (antecedentes['fuerza']['moderado']                   | antecedentes['fuerza']['algo']) &
        (antecedentes['agilidad']['moderado']                 | antecedentes['agilidad']['algo']) &
        (antecedentes['coordinacion_inferior']['moderado']    | antecedentes['coordinacion_inferior']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['liderazgo']['moderado']                | antecedentes['liderazgo']['algo']) &
        (antecedentes['responsabilidad']['moderado']          | antecedentes['responsabilidad']['algo']) &
        (antecedentes['solucion_problemas']['moderado']       | antecedentes['solucion_problemas']['algo']) &
        (antecedentes['trabajo_equipo']['moderado']           | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['comunicacion']['moderado']             | antecedentes['comunicacion']['algo']) &
        (antecedentes['cooperacion']['moderado']              | antecedentes['cooperacion']['algo']) &
        (antecedentes['deporte_contacto']['moderado']         | antecedentes['deporte_contacto']['algo']),
        consecuencias['futbol']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['velocidad']['algo']                | antecedentes['velocidad']['desinteresado']) &
        (antecedentes['fuerza']['algo']                   | antecedentes['fuerza']['desinteresado']) &
        (antecedentes['agilidad']['algo']                 | antecedentes['agilidad']['desinteresado']) &
        (antecedentes['coordinacion_inferior']['algo']    | antecedentes['coordinacion_inferior']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['liderazgo']['algo']                | antecedentes['liderazgo']['desinteresado']) &
        (antecedentes['responsabilidad']['algo']          | antecedentes['responsabilidad']['desinteresado']) &
        (antecedentes['solucion_problemas']['algo']       | antecedentes['solucion_problemas']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo']           | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['comunicacion']['algo']             | antecedentes['comunicacion']['desinteresado']) &
        (antecedentes['cooperacion']['algo']              | antecedentes['cooperacion']['desinteresado']) &
        (antecedentes['deporte_contacto']['algo']         | antecedentes['deporte_contacto']['desinteresado']),
        consecuencias['futbol']['bajo']
    ),
    ############# Voley ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['velocidad']['interesado']                | antecedentes['velocidad']['mucho']) &
        (antecedentes['fuerza']['interesado']                   | antecedentes['fuerza']['mucho']) &
        (antecedentes['agilidad']['interesado']                 | antecedentes['agilidad']['mucho']) &
        (antecedentes['coordinacion_superior']['interesado']    | antecedentes['coordinacion_superior']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['liderazgo']['interesado']                | antecedentes['liderazgo']['mucho']) &
        (antecedentes['responsabilidad']['interesado']          | antecedentes['responsabilidad']['mucho']) &
        (antecedentes['solucion_problemas']['interesado']       | antecedentes['solucion_problemas']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado']           | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['comunicacion']['interesado']             | antecedentes['comunicacion']['mucho']) &
        (antecedentes['cooperacion']['interesado']              | antecedentes['cooperacion']['mucho']),
        consecuencias['voley']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['velocidad']['moderado']                | antecedentes['velocidad']['algo']) &
        (antecedentes['fuerza']['moderado']                   | antecedentes['fuerza']['algo']) &
        (antecedentes['agilidad']['moderado']                 | antecedentes['agilidad']['algo']) &
        (antecedentes['coordinacion_superior']['moderado']    | antecedentes['coordinacion_superior']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['liderazgo']['moderado']                | antecedentes['liderazgo']['algo']) &
        (antecedentes['responsabilidad']['moderado']          | antecedentes['responsabilidad']['algo']) &
        (antecedentes['solucion_problemas']['moderado']       | antecedentes['solucion_problemas']['algo']) &
        (antecedentes['trabajo_equipo']['moderado']           | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['comunicacion']['moderado']             | antecedentes['comunicacion']['algo']) &
        (antecedentes['cooperacion']['moderado']              | antecedentes['cooperacion']['algo']),
        consecuencias['voley']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['velocidad']['algo']                | antecedentes['velocidad']['desinteresado']) &
        (antecedentes['fuerza']['algo']                   | antecedentes['fuerza']['desinteresado']) &
        (antecedentes['agilidad']['algo']                 | antecedentes['agilidad']['desinteresado']) &
        (antecedentes['coordinacion_superior']['algo']    | antecedentes['coordinacion_superior']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['liderazgo']['algo']                | antecedentes['liderazgo']['desinteresado']) &
        (antecedentes['responsabilidad']['algo']          | antecedentes['responsabilidad']['desinteresado']) &
        (antecedentes['solucion_problemas']['algo']       | antecedentes['solucion_problemas']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo']           | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['comunicacion']['algo']             | antecedentes['comunicacion']['desinteresado']) &
        (antecedentes['cooperacion']['algo']              | antecedentes['cooperacion']['desinteresado']),
        consecuencias['voley']['bajo']
    ),
    ############# Baloncesto ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['velocidad']['interesado']                | antecedentes['velocidad']['mucho']) &
        (antecedentes['fuerza']['interesado']                   | antecedentes['fuerza']['mucho']) &
        (antecedentes['agilidad']['interesado']                 | antecedentes['agilidad']['mucho']) &
        (antecedentes['coordinacion_superior']['interesado']    | antecedentes['coordinacion_superior']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['liderazgo']['interesado']                | antecedentes['liderazgo']['mucho']) &
        (antecedentes['responsabilidad']['interesado']          | antecedentes['responsabilidad']['mucho']) &
        (antecedentes['solucion_problemas']['interesado']       | antecedentes['solucion_problemas']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado']           | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['comunicacion']['interesado']             | antecedentes['comunicacion']['mucho']) &
        (antecedentes['cooperacion']['interesado']              | antecedentes['cooperacion']['mucho']) &
        (antecedentes['deporte_contacto']['interesado']         | antecedentes['deporte_contacto']['mucho']),
        consecuencias['baloncesto']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['velocidad']['moderado']                | antecedentes['velocidad']['algo']) &
        (antecedentes['fuerza']['moderado']                   | antecedentes['fuerza']['algo']) &
        (antecedentes['agilidad']['moderado']                 | antecedentes['agilidad']['algo']) &
        (antecedentes['coordinacion_superior']['moderado']    | antecedentes['coordinacion_superior']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['liderazgo']['moderado']                | antecedentes['liderazgo']['algo']) &
        (antecedentes['responsabilidad']['moderado']          | antecedentes['responsabilidad']['algo']) &
        (antecedentes['solucion_problemas']['moderado']       | antecedentes['solucion_problemas']['algo']) &
        (antecedentes['trabajo_equipo']['moderado']           | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['comunicacion']['moderado']             | antecedentes['comunicacion']['algo']) &
        (antecedentes['cooperacion']['moderado']              | antecedentes['cooperacion']['algo']) &
        (antecedentes['deporte_contacto']['moderado']         | antecedentes['deporte_contacto']['algo']),
        consecuencias['baloncesto']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['velocidad']['algo']                | antecedentes['velocidad']['desinteresado']) &
        (antecedentes['fuerza']['algo']                   | antecedentes['fuerza']['desinteresado']) &
        (antecedentes['agilidad']['algo']                 | antecedentes['agilidad']['desinteresado']) &
        (antecedentes['coordinacion_superior']['algo']    | antecedentes['coordinacion_superior']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['liderazgo']['algo']                | antecedentes['liderazgo']['desinteresado']) &
        (antecedentes['responsabilidad']['algo']          | antecedentes['responsabilidad']['desinteresado']) &
        (antecedentes['solucion_problemas']['algo']       | antecedentes['solucion_problemas']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo']           | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['comunicacion']['algo']             | antecedentes['comunicacion']['desinteresado']) &
        (antecedentes['cooperacion']['algo']              | antecedentes['cooperacion']['desinteresado']) &
        (antecedentes['deporte_contacto']['algo']         | antecedentes['deporte_contacto']['desinteresado']),
        consecuencias['baloncesto']['bajo']
    ),
    ############# Natacion ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['velocidad']['interesado']                | antecedentes['velocidad']['mucho']) &
        (antecedentes['fuerza']['interesado']                   | antecedentes['fuerza']['mucho']) &
        (antecedentes['coordinacion_superior']['interesado']    | antecedentes['coordinacion_superior']['mucho']) &
        (antecedentes['coordinacion_inferior']['interesado']    | antecedentes['coordinacion_inferior']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['trabajo_individual']['interesado']       | antecedentes['trabajo_individual']['mucho']),
        consecuencias['natacion']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['velocidad']['moderado']                | antecedentes['velocidad']['algo']) &
        (antecedentes['fuerza']['moderado']                   | antecedentes['fuerza']['algo']) &
        (antecedentes['coordinacion_superior']['moderado']    | antecedentes['coordinacion_superior']['algo']) &
        (antecedentes['coordinacion_inferior']['moderado']    | antecedentes['coordinacion_inferior']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['trabajo_individual']['moderado']       | antecedentes['trabajo_individual']['algo']),
        consecuencias['natacion']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['velocidad']['algo']                | antecedentes['velocidad']['desinteresado']) &
        (antecedentes['fuerza']['algo']                   | antecedentes['fuerza']['desinteresado']) &
        (antecedentes['coordinacion_superior']['algo']    | antecedentes['coordinacion_superior']['desinteresado']) &
        (antecedentes['coordinacion_inferior']['algo']    | antecedentes['coordinacion_inferior']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['trabajo_individual']['algo']       | antecedentes['trabajo_individual']['desinteresado']),
        consecuencias['natacion']['bajo']
    ),
    ############# Artes Marciales ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['velocidad']['interesado']                | antecedentes['velocidad']['mucho']) &
        (antecedentes['fuerza']['interesado']                   | antecedentes['fuerza']['mucho']) &
        (antecedentes['agilidad']['interesado']                 | antecedentes['agilidad']['mucho']) &
        (antecedentes['coordinacion_superior']['interesado']    | antecedentes['coordinacion_superior']['mucho']) &
        (antecedentes['coordinacion_inferior']['interesado']    | antecedentes['coordinacion_inferior']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['responsabilidad']['interesado']          | antecedentes['responsabilidad']['mucho']) &
        (antecedentes['autocontrol']['interesado']              | antecedentes['autocontrol']['mucho']) &
        (antecedentes['equilibrio_fisica_mental']['interesado'] | antecedentes['equilibrio_fisica_mental']['mucho']) &
        (antecedentes['trabajo_individual']['interesado']       | antecedentes['trabajo_individual']['mucho']) &
        (antecedentes['deporte_contacto']['interesado']         | antecedentes['deporte_contacto']['mucho']),
        consecuencias['artes_marciales']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['velocidad']['moderado']                | antecedentes['velocidad']['algo']) &
        (antecedentes['fuerza']['moderado']                   | antecedentes['fuerza']['algo']) &
        (antecedentes['agilidad']['moderado']                 | antecedentes['agilidad']['algo']) &
        (antecedentes['coordinacion_superior']['moderado']    | antecedentes['coordinacion_superior']['algo']) &
        (antecedentes['coordinacion_inferior']['moderado']    | antecedentes['coordinacion_inferior']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['responsabilidad']['moderado']          | antecedentes['responsabilidad']['algo']) &
        (antecedentes['autocontrol']['moderado']              | antecedentes['autocontrol']['algo']) &
        (antecedentes['equilibrio_fisica_mental']['moderado'] | antecedentes['equilibrio_fisica_mental']['algo']) &
        (antecedentes['trabajo_individual']['moderado']       | antecedentes['trabajo_individual']['algo']) &
        (antecedentes['deporte_contacto']['moderado']         | antecedentes['deporte_contacto']['algo']),
        consecuencias['artes_marciales']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['velocidad']['algo']                | antecedentes['velocidad']['desinteresado']) &
        (antecedentes['fuerza']['algo']                   | antecedentes['fuerza']['desinteresado']) &
        (antecedentes['agilidad']['algo']                 | antecedentes['agilidad']['desinteresado']) &
        (antecedentes['coordinacion_superior']['algo']    | antecedentes['coordinacion_superior']['desinteresado']) &
        (antecedentes['coordinacion_inferior']['algo']    | antecedentes['coordinacion_inferior']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['responsabilidad']['algo']          | antecedentes['responsabilidad']['desinteresado']) &
        (antecedentes['autocontrol']['algo']              | antecedentes['autocontrol']['desinteresado']) &
        (antecedentes['equilibrio_fisica_mental']['algo'] | antecedentes['equilibrio_fisica_mental']['desinteresado']) &
        (antecedentes['trabajo_individual']['algo']       | antecedentes['trabajo_individual']['desinteresado']) &
        (antecedentes['deporte_contacto']['algo']         | antecedentes['deporte_contacto']['desinteresado']),
        consecuencias['artes_marciales']['bajo']
    ),
    ############# Ciclismo ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['velocidad']['interesado']                | antecedentes['velocidad']['mucho']) &
        (antecedentes['fuerza']['interesado']                   | antecedentes['fuerza']['mucho']) &
        (antecedentes['agilidad']['interesado']                 | antecedentes['agilidad']['mucho']) &
        (antecedentes['coordinacion_superior']['interesado']    | antecedentes['coordinacion_superior']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['trabajo_individual']['interesado']       | antecedentes['trabajo_individual']['mucho']),
        consecuencias['ciclismo']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['velocidad']['moderado']                | antecedentes['velocidad']['algo']) &
        (antecedentes['fuerza']['moderado']                   | antecedentes['fuerza']['algo']) &
        (antecedentes['agilidad']['moderado']                 | antecedentes['agilidad']['algo']) &
        (antecedentes['coordinacion_superior']['moderado']    | antecedentes['coordinacion_superior']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['trabajo_individual']['moderado']       | antecedentes['trabajo_individual']['algo']),
        consecuencias['ciclismo']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['velocidad']['algo']                | antecedentes['velocidad']['desinteresado']) &
        (antecedentes['fuerza']['algo']                   | antecedentes['fuerza']['desinteresado']) &
        (antecedentes['agilidad']['algo']                 | antecedentes['agilidad']['desinteresado']) &
        (antecedentes['coordinacion_superior']['algo']    | antecedentes['coordinacion_superior']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['trabajo_individual']['algo']       | antecedentes['trabajo_individual']['desinteresado']),
        consecuencias['ciclismo']['bajo']
    ),
    ############# Ajedrez ############
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['solucion_problemas']['interesado']       | antecedentes['solucion_problemas']['mucho']) &
        (antecedentes['paciencia']['interesado']                | antecedentes['paciencia']['mucho']) &
        (antecedentes['trabajo_individual']['interesado']       | antecedentes['trabajo_individual']['mucho']) &
        (antecedentes['deporte_estrategia']['interesado']       | antecedentes['deporte_estrategia']['mucho']),
        consecuencias['ajedrez']['alto']
    ),
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['solucion_problemas']['moderado']       | antecedentes['solucion_problemas']['algo']) &
        (antecedentes['paciencia']['moderado']                | antecedentes['paciencia']['algo']) &
        (antecedentes['trabajo_individual']['moderado']       | antecedentes['trabajo_individual']['algo']) &
        (antecedentes['deporte_estrategia']['moderado']       | antecedentes['deporte_estrategia']['algo']),
        consecuencias['ajedrez']['medio']
    ),
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['solucion_problemas']['algo']       | antecedentes['solucion_problemas']['desinteresado']) &
        (antecedentes['paciencia']['algo']                | antecedentes['paciencia']['desinteresado']) &
        (antecedentes['trabajo_individual']['algo']       | antecedentes['trabajo_individual']['desinteresado']) &
        (antecedentes['deporte_estrategia']['algo']       | antecedentes['deporte_estrategia']['desinteresado']),
        consecuencias['ajedrez']['bajo']
    ),
    ############# Musica ############
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['memorizacion']['interesado']             | antecedentes['memorizacion']['mucho']) &
        (antecedentes['perfeccionismo']['interesado']           | antecedentes['perfeccionismo']['mucho']) &
        (antecedentes['autoexpresion']['interesado']            | antecedentes['autoexpresion']['mucho']) &
        (antecedentes['comunicacion']['interesado']             | antecedentes['comunicacion']['mucho']) &
        (antecedentes['cooperacion']['interesado']              | antecedentes['cooperacion']['mucho']),
        consecuencias['musica']['alto']
    ),
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['memorizacion']['moderado']             | antecedentes['memorizacion']['algo']) &
        (antecedentes['perfeccionismo']['moderado']           | antecedentes['perfeccionismo']['algo']) &
        (antecedentes['autoexpresion']['moderado']            | antecedentes['autoexpresion']['algo']) &
        (antecedentes['comunicacion']['moderado']             | antecedentes['comunicacion']['algo']) &
        (antecedentes['cooperacion']['moderado']              | antecedentes['cooperacion']['algo']),
        consecuencias['musica']['medio']
    ),
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['memorizacion']['algo']             | antecedentes['memorizacion']['desinteresado']) &
        (antecedentes['perfeccionismo']['algo']           | antecedentes['perfeccionismo']['desinteresado']) &
        (antecedentes['autoexpresion']['algo']            | antecedentes['autoexpresion']['desinteresado']) &
        (antecedentes['comunicacion']['algo']             | antecedentes['comunicacion']['desinteresado']) &
        (antecedentes['cooperacion']['algo']              | antecedentes['cooperacion']['desinteresado']),
        consecuencias['musica']['bajo']
    ),
    ############# Danza ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['fuerza']['interesado']                   | antecedentes['fuerza']['mucho']) &
        (antecedentes['agilidad']['interesado']                 | antecedentes['agilidad']['mucho']) &
        (antecedentes['coordinacion_superior']['interesado']    | antecedentes['coordinacion_superior']['mucho']) &
        (antecedentes['coordinacion_inferior']['interesado']    | antecedentes['coordinacion_inferior']['mucho']) &
        (antecedentes['flexibilidad']['interesado']             | antecedentes['flexibilidad']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['memorizacion']['interesado']             | antecedentes['memorizacion']['mucho']) &
        (antecedentes['perfeccionismo']['interesado']           | antecedentes['perfeccionismo']['mucho']) &
        (antecedentes['autoexpresion']['interesado']            | antecedentes['autoexpresion']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado']           | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['comunicacion']['interesado']             | antecedentes['comunicacion']['mucho']) &
        (antecedentes['cooperacion']['interesado']              | antecedentes['cooperacion']['mucho']),
        consecuencias['danza']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['fuerza']['moderado']                   | antecedentes['fuerza']['algo']) &
        (antecedentes['agilidad']['moderado']                 | antecedentes['agilidad']['algo']) &
        (antecedentes['coordinacion_superior']['moderado']    | antecedentes['coordinacion_superior']['algo']) &
        (antecedentes['coordinacion_inferior']['moderado']    | antecedentes['coordinacion_inferior']['algo']) &
        (antecedentes['flexibilidad']['moderado']             | antecedentes['flexibilidad']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['memorizacion']['moderado']             | antecedentes['memorizacion']['algo']) &
        (antecedentes['perfeccionismo']['moderado']           | antecedentes['perfeccionismo']['algo']) &
        (antecedentes['autoexpresion']['moderado']            | antecedentes['autoexpresion']['algo']) &
        (antecedentes['trabajo_equipo']['moderado']           | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['comunicacion']['moderado']             | antecedentes['comunicacion']['algo']) &
        (antecedentes['cooperacion']['moderado']              | antecedentes['cooperacion']['algo']),
        consecuencias['danza']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['fuerza']['algo']                   | antecedentes['fuerza']['desinteresado']) &
        (antecedentes['agilidad']['algo']                 | antecedentes['agilidad']['desinteresado']) &
        (antecedentes['coordinacion_superior']['algo']    | antecedentes['coordinacion_superior']['desinteresado']) &
        (antecedentes['coordinacion_inferior']['algo']    | antecedentes['coordinacion_inferior']['desinteresado']) &
        (antecedentes['flexibilidad']['algo']             | antecedentes['flexibilidad']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['memorizacion']['algo']             | antecedentes['memorizacion']['desinteresado']) &
        (antecedentes['perfeccionismo']['algo']           | antecedentes['perfeccionismo']['desinteresado']) &
        (antecedentes['autoexpresion']['algo']            | antecedentes['autoexpresion']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo']           | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['comunicacion']['algo']             | antecedentes['comunicacion']['desinteresado']) &
        (antecedentes['cooperacion']['algo']              | antecedentes['cooperacion']['desinteresado']),
        consecuencias['danza']['bajo']
    ),
    ############# Teatro ############
    ctrl.Rule(
        (antecedentes['resistencia']['interesado']              | antecedentes['resistencia']['mucho']) &
        (antecedentes['agilidad']['interesado']                 | antecedentes['agilidad']['mucho']) &
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['resiliencia']['interesado']              | antecedentes['resiliencia']['mucho']) &
        (antecedentes['disciplina']['interesado']               | antecedentes['disciplina']['mucho']) &
        (antecedentes['memorizacion']['interesado']             | antecedentes['memorizacion']['mucho']) &
        (antecedentes['perfeccionismo']['interesado']           | antecedentes['perfeccionismo']['mucho']) &
        (antecedentes['autoexpresion']['interesado']            | antecedentes['autoexpresion']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado']           | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['comunicacion']['interesado']             | antecedentes['comunicacion']['mucho']) &
        (antecedentes['cooperacion']['interesado']              | antecedentes['cooperacion']['mucho']),
        consecuencias['teatro']['alto']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['moderado']              | antecedentes['resistencia']['algo']) &
        (antecedentes['agilidad']['moderado']                 | antecedentes['agilidad']['algo']) &
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['resiliencia']['moderado']              | antecedentes['resiliencia']['algo']) &
        (antecedentes['disciplina']['moderado']               | antecedentes['disciplina']['algo']) &
        (antecedentes['memorizacion']['moderado']             | antecedentes['memorizacion']['algo']) &
        (antecedentes['perfeccionismo']['moderado']           | antecedentes['perfeccionismo']['algo']) &
        (antecedentes['autoexpresion']['moderado']            | antecedentes['autoexpresion']['algo']) &
        (antecedentes['trabajo_equipo']['moderado']           | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['comunicacion']['moderado']             | antecedentes['comunicacion']['algo']) &
        (antecedentes['cooperacion']['moderado']              | antecedentes['cooperacion']['algo']),
        consecuencias['teatro']['medio']
    ),
    ctrl.Rule(
        (antecedentes['resistencia']['algo']              | antecedentes['resistencia']['desinteresado']) &
        (antecedentes['agilidad']['algo']                 | antecedentes['agilidad']['desinteresado']) &
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['resiliencia']['algo']              | antecedentes['resiliencia']['desinteresado']) &
        (antecedentes['disciplina']['algo']               | antecedentes['disciplina']['desinteresado']) &
        (antecedentes['memorizacion']['algo']             | antecedentes['memorizacion']['desinteresado']) &
        (antecedentes['perfeccionismo']['algo']           | antecedentes['perfeccionismo']['desinteresado']) &
        (antecedentes['autoexpresion']['algo']            | antecedentes['autoexpresion']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo']           | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['comunicacion']['algo']             | antecedentes['comunicacion']['desinteresado']) &
        (antecedentes['cooperacion']['algo']              | antecedentes['cooperacion']['desinteresado']),
        consecuencias['teatro']['bajo']
    ),
    ############# Escritura Creativa ############
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['interesado'] | antecedentes['determinacion_motivacion']['mucho']) &
        (antecedentes['perseverancia']['interesado']            | antecedentes['perseverancia']['mucho']) &
        (antecedentes['concentracion']['interesado']            | antecedentes['concentracion']['mucho']) &
        (antecedentes['autoexpresion']['interesado']            | antecedentes['autoexpresion']['mucho']) &
        (antecedentes['trabajo_individual']['interesado']       | antecedentes['trabajo_individual']['mucho']),
        consecuencias['escritura_creativa']['alto']
    ),
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['moderado'] | antecedentes['determinacion_motivacion']['algo']) &
        (antecedentes['perseverancia']['moderado']            | antecedentes['perseverancia']['algo']) &
        (antecedentes['concentracion']['moderado']            | antecedentes['concentracion']['algo']) &
        (antecedentes['autoexpresion']['moderado']            | antecedentes['autoexpresion']['algo']) &
        (antecedentes['trabajo_individual']['moderado']       | antecedentes['trabajo_individual']['algo']),
        consecuencias['escritura_creativa']['medio']
    ),
    ctrl.Rule(
        (antecedentes['determinacion_motivacion']['algo'] | antecedentes['determinacion_motivacion']['desinteresado']) &
        (antecedentes['perseverancia']['algo']            | antecedentes['perseverancia']['desinteresado']) &
        (antecedentes['concentracion']['algo']            | antecedentes['concentracion']['desinteresado']) &
        (antecedentes['autoexpresion']['algo']            | antecedentes['autoexpresion']['desinteresado']) &
        (antecedentes['trabajo_individual']['algo']       | antecedentes['trabajo_individual']['desinteresado']),
        consecuencias['escritura_creativa']['bajo']
    )
]

def recomendar_actividad(respuestas):
    """
    Recomienda actividades extracurriculares basadas en un sistema difuso.

    Parámetros:
    respuestas (dict): Diccionario con las respuestas del estudiante. Las claves son las variables de entrada y los 
                       valores son los niveles de interés (0 a 5).

    Retorna:
    dict: Diccionario con las actividades recomendadas y su nivel de adecuación. Si no se puede calcular, 
          el valor será 'No se pudo calcular'.

    Descripción:
    1. Asigna las respuestas al simulador del sistema difuso.
    2. Ejecuta la simulación para calcular las recomendaciones.
    3. Devuelve un diccionario con las recomendaciones para cada actividad.
    """

    # Crear el sistema de control difuso y su simulador
    # 1. Crear un sistema de control basado en las reglas definidas.
    sistema_control = ctrl.ControlSystem(reglas)
    # 2. Crear un simulador del sistema de control para procesar las entradas y generar las salidas.
    sistema_simulador  = ctrl.ControlSystemSimulation(sistema_control)

    for key, valor in respuestas.items():
        sistema_simulador.input[key] = valor
    sistema_simulador.compute()
    recomendaciones = {}
    for actividad in consecuencias:
        try:
            recomendaciones[actividad] = sistema_simulador.output[actividad]
        except KeyError:
            recomendaciones[actividad] = 'No se pudo calcular'
        
    return recomendaciones

def mostrar_respuesta(recomedaciones):
    """
    Imprime cada actividad recomendada y su nivel de recomendación.

    Parámetros:
    recomendaciones (dict): Diccionario con actividades como claves y niveles de recomendación como valores.
    """
    respuesta = ""

    for Actividad, nivel_recomendacion in recomedaciones.items():
        respuesta += f"{Actividad}: {nivel_recomendacion}\n"

    return respuesta