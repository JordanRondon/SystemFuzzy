import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

##### Definición de las variables difusas para cada pregunta del cuestionario #####
variable_psicologica = [
    # 1. Intereses Personales
    'deportes',                 # 1.1. ¿Te gusta participar en actividades deportivas y físicas?
    'artes',                    # 1.2. ¿Disfrutas de actividades artísticas como la música, la pintura, la danza, la fotografia o otras actividades creativas?
    'ciencia',                  # 1.3. ¿Te apasiona resolver problemas matemáticos o científicos?
    'tecnologia',               # 1.4. ¿Te atraen las actividades relacionadas con la tecnología y la innovación?
    'creatividad',              # 1.5. ¿Te gusta participar en proyectos creativos como la escritura, la fotografía o actuar?
    # 2. Personalidad
    'social',                   # 2.1. ¿Prefieres estar rodeado de personas y participar en actividades?
    #'liderazgo',                # 2.2. ¿Te sientes cómodo liderando grupos o actividades?
    'autoexpresion',            # 2.3. ¿Prefieres actividades en las que puedas expresarte libremente, como el teatro o la música?
    'competitividad',           # 2.4. ¿Te gusta competir y destacarte en lo que haces?
    'independencia',            # 2.5. ¿Prefieres actividades que te permitan reflexionar y trabajar de manera independiente?
    # 3. Habilidades y Capacidades
    'coordinacion',             # 3.1. ¿Consideras que tienes buena coordinación y habilidades físicas para los deportes?
    'creatividad_habilidad',    # 3.2. ¿Disfrutas de actividades que requieren creatividad e imaginación?
    'tecnologia_habilidad',     # 3.3. ¿Te sientes cómodo utilizando herramientas tecnológicas y aprendiendo sobre nuevas tecnologías?
    'resolucion_problemas',     # 3.4. ¿Te gusta resolver acertijos, problemas o realizar actividades que requieren concentración?
    'expresion_artistica',      # 3.5. ¿Disfrutas de actividades que te permiten expresar tus emociones a través del arte o la música?
    # 4. Preferencias de Socialización
    'trabajo_equipo',           # 4.1. ¿Prefieres trabajar en equipo para lograr un objetivo común?
    'debates',                  # 4.2. ¿Te sientes cómodo participando en discusiones o debates en grupo?
    'actividades_grupales',     # 4.3. ¿Te gusta participar en actividades grupales como deportes o teatro?
    'colaboracion',             # 4.4. ¿Prefieres actividades donde puedas colaborar con otros, en lugar de trabajar solo?
    'compartir_ideas',          # 4.5. ¿Te sientes motivado cuando puedes compartir tus ideas y aprender de los demás?
    # 5. Valores y Motivaciones
    'competir',                 # 5.1. ¿Te motiva la idea de competir y ganar en juegos o deportes?
    'aprendizaje',              # 5.2. ¿Te interesa aprender cosas nuevas y explorar diferentes áreas de conocimiento?
    #'ayudar',                   # 5.3. ¿Te gusta ayudar a los demás y participar en proyectos comunitarios?
    'autoexpresion_valor',      # 5.4. ¿Te motiva la autoexpresión y sientes que es importante compartir tus pensamientos y sentimientos?
    'superar_limites',          # 5.5. ¿Prefieres actividades que te desafíen y te permitan superar tus límites?
    # 6. Nivel de Estrés y Manejo de la Ansiedad
    #'relajacion',               # 6.1. ¿Buscas actividades que te ayuden a relajarte y reducir el estrés?
    'liberar_energia',          # 6.2. ¿Te sientes mejor cuando puedes liberar energía a través de actividades físicas intensas?
    'desconectar',              # 6.3. ¿Prefieres actividades que te permitan desconectar y centrarte en el momento presente?
    'creatividad_relajacion',   # 6.4. ¿Te ayudan las actividades creativas como la escritura o el arte o manejar el estrés?
    'deportes_relajacion',      # 6.5. ¿Te sientes más relajado cuando practicas deportes o ejercicios físicos?
    # 7. Objetivos Personales
    'mejorar_habilidades',      # 7.1. ¿Te interesa mejorar tus habilidades físicas o atléticas?
    'desarrollo_liderazgo',     # 7.2. ¿Estás buscando actividades que te ayuden a desarrollar habilidades de liderazgo o trabajo en equipo?
    'equilibrio_salud',         # 7.3. ¿Te importa mantener un equilibrio entre tu salud física y mental a través de actividades?
    'aprender_nueva_habilidad', # 7.4. ¿Tienes el objetivo de aprender una nueva habilidad o mejorar una que ya tienes?
    'crecimiento_personal'      # 7.5. ¿Estás buscando actividades que te ayuden a crecer personalmente y alcanzar tus metas a largo plazo?
]

# Creación de antecedentes para el sistema difuso.
# Un 'Antecedent' representa una variable de entrada en el sistema difuso.
# El rango de valores posibles para cada antecedente es de 0 a 5, con un incremento de 1.
antecedentes = {variable: ctrl.Antecedent(np.arange(0, 5), variable) for variable in variable_psicologica}

# Definición de las variables difusas para cada variable de salida
actividad_extracurricular = [
    'futbol',
    'voley',
    'baloncesto',
    'natacion',
    'artes_marciales',
    'ciclismo',
    'teatro',
    'musica',
    'danza',
    'fotografia',
    'debate',
    'ciencia_tecnologia',
    'ajedrez',
    #'cine_artes_escenicas',
    'cocina_gastronomia',
    'escritura_creativa'
]

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
    ############# FUTBOL ############
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho']),
        consecuencias['futbol']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho'] | antecedentes['deportes']['moderado'] | antecedentes['deportes']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho'] | antecedentes['coordinacion']['moderado'] | antecedentes['coordinacion']['algo']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho'] | antecedentes['trabajo_equipo']['moderado'] | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho'] | antecedentes['actividades_grupales']['moderado'] | antecedentes['actividades_grupales']['algo']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho'] | antecedentes['colaboracion']['moderado'] | antecedentes['colaboracion']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho'] | antecedentes['superar_limites']['moderado'] | antecedentes['superar_limites']['algo']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho'] | antecedentes['mejorar_habilidades']['moderado'] | antecedentes['mejorar_habilidades']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['futbol']['medio']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['algo'] | antecedentes['deportes']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['coordinacion']['algo'] | antecedentes['coordinacion']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo'] | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['actividades_grupales']['algo'] | antecedentes['actividades_grupales']['desinteresado']) &
        (antecedentes['colaboracion']['algo'] | antecedentes['colaboracion']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['superar_limites']['algo'] | antecedentes['superar_limites']['desinteresado']) &
        (antecedentes['mejorar_habilidades']['algo'] | antecedentes['mejorar_habilidades']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['futbol']['bajo']
    ),

    ############# VOLEY ############
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho']),
        consecuencias['voley']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho'] | antecedentes['deportes']['moderado'] | antecedentes['deportes']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho'] | antecedentes['coordinacion']['moderado'] | antecedentes['coordinacion']['algo']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho'] | antecedentes['trabajo_equipo']['moderado'] | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho'] | antecedentes['actividades_grupales']['moderado'] | antecedentes['actividades_grupales']['algo']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho'] | antecedentes['colaboracion']['moderado'] | antecedentes['colaboracion']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho'] | antecedentes['superar_limites']['moderado'] | antecedentes['superar_limites']['algo']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho'] | antecedentes['mejorar_habilidades']['moderado'] | antecedentes['mejorar_habilidades']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['voley']['medio']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['algo'] | antecedentes['deportes']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['coordinacion']['algo'] | antecedentes['coordinacion']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo'] | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['actividades_grupales']['algo'] | antecedentes['actividades_grupales']['desinteresado']) &
        (antecedentes['colaboracion']['algo'] | antecedentes['colaboracion']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['superar_limites']['algo'] | antecedentes['superar_limites']['desinteresado']) &
        (antecedentes['mejorar_habilidades']['algo'] | antecedentes['mejorar_habilidades']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['voley']['bajo']
    ),

    ############# BALONCESTO ############
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho']),
        consecuencias['baloncesto']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho'] | antecedentes['deportes']['moderado'] | antecedentes['deportes']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho'] | antecedentes['coordinacion']['moderado'] | antecedentes['coordinacion']['algo']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho'] | antecedentes['trabajo_equipo']['moderado'] | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho'] | antecedentes['actividades_grupales']['moderado'] | antecedentes['actividades_grupales']['algo']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho'] | antecedentes['colaboracion']['moderado'] | antecedentes['colaboracion']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho'] | antecedentes['superar_limites']['moderado'] | antecedentes['superar_limites']['algo']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho'] | antecedentes['mejorar_habilidades']['moderado'] | antecedentes['mejorar_habilidades']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['baloncesto']['medio']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['algo'] | antecedentes['deportes']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['coordinacion']['algo'] | antecedentes['coordinacion']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo'] | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['actividades_grupales']['algo'] | antecedentes['actividades_grupales']['desinteresado']) &
        (antecedentes['colaboracion']['algo'] | antecedentes['colaboracion']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['superar_limites']['algo'] | antecedentes['superar_limites']['desinteresado']) &
        (antecedentes['mejorar_habilidades']['algo'] | antecedentes['mejorar_habilidades']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['baloncesto']['bajo']
    ),

    ############# NATACIÓN ############
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho']),
        consecuencias['natacion']['alto']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho'] | antecedentes['deportes']['moderado'] | antecedentes['deportes']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho'] | antecedentes['coordinacion']['moderado'] | antecedentes['coordinacion']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho'] | antecedentes['superar_limites']['moderado'] | antecedentes['superar_limites']['algo']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho'] | antecedentes['mejorar_habilidades']['moderado'] | antecedentes['mejorar_habilidades']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['natacion']['medio']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['algo'] | antecedentes['deportes']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['coordinacion']['algo'] | antecedentes['coordinacion']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['superar_limites']['algo'] | antecedentes['superar_limites']['desinteresado']) &
        (antecedentes['mejorar_habilidades']['algo'] | antecedentes['mejorar_habilidades']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['natacion']['bajo']
    ),
    
    ############# ARTES_MARCIALES ############
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho']) &
        (antecedentes['liberar_energia']['interesado'] | antecedentes['liberar_energia']['mucho']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho']),
        consecuencias['artes_marciales']['alto']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho'] | antecedentes['deportes']['moderado'] | antecedentes['deportes']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho'] | antecedentes['independencia']['moderado'] | antecedentes['independencia']['algo']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho'] | antecedentes['coordinacion']['moderado'] | antecedentes['coordinacion']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho'] | antecedentes['superar_limites']['moderado'] | antecedentes['superar_limites']['algo']) &
        (antecedentes['liberar_energia']['interesado'] | antecedentes['liberar_energia']['mucho'] | antecedentes['liberar_energia']['moderado'] | antecedentes['liberar_energia']['algo']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho'] | antecedentes['mejorar_habilidades']['moderado'] | antecedentes['mejorar_habilidades']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['artes_marciales']['medio']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['algo'] | antecedentes['deportes']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['independencia']['algo'] | antecedentes['independencia']['desinteresado']) &
        (antecedentes['coordinacion']['algo'] | antecedentes['coordinacion']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['superar_limites']['algo'] | antecedentes['superar_limites']['desinteresado']) &
        (antecedentes['liberar_energia']['algo'] | antecedentes['liberar_energia']['desinteresado']) &
        (antecedentes['mejorar_habilidades']['algo'] | antecedentes['mejorar_habilidades']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['artes_marciales']['bajo']
    ),
    
    ############# CICLISMO ############
    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho']) &
        (antecedentes['liberar_energia']['interesado'] | antecedentes['liberar_energia']['mucho']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho']),
        consecuencias['ciclismo']['alto']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['interesado'] | antecedentes['deportes']['mucho'] | antecedentes['deportes']['moderado'] | antecedentes['deportes']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho'] | antecedentes['independencia']['moderado'] | antecedentes['independencia']['algo']) &
        (antecedentes['coordinacion']['interesado'] | antecedentes['coordinacion']['mucho'] | antecedentes['coordinacion']['moderado'] | antecedentes['coordinacion']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho'] | antecedentes['superar_limites']['moderado'] | antecedentes['superar_limites']['algo']) &
        (antecedentes['liberar_energia']['interesado'] | antecedentes['liberar_energia']['mucho'] | antecedentes['liberar_energia']['moderado'] | antecedentes['liberar_energia']['algo']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho'] | antecedentes['desconectar']['moderado'] | antecedentes['desconectar']['algo']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho'] | antecedentes['mejorar_habilidades']['moderado'] | antecedentes['mejorar_habilidades']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['ciclismo']['medio']
    ),

    ctrl.Rule(
        (antecedentes['deportes']['algo'] | antecedentes['deportes']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['independencia']['algo'] | antecedentes['independencia']['desinteresado']) &
        (antecedentes['coordinacion']['algo'] | antecedentes['coordinacion']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['superar_limites']['algo'] | antecedentes['superar_limites']['desinteresado']) &
        (antecedentes['liberar_energia']['algo'] | antecedentes['liberar_energia']['desinteresado']) &
        (antecedentes['desconectar']['algo'] | antecedentes['desconectar']['desinteresado']) &
        (antecedentes['mejorar_habilidades']['algo'] | antecedentes['mejorar_habilidades']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['ciclismo']['bajo']
    ),
    ############# TEATRO ############
    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho']) &
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['autoexpresion']['interesado'] | antecedentes['autoexpresion']['mucho']) &
        (antecedentes['creatividad_habilidad']['interesado'] | antecedentes['creatividad_habilidad']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho']) &
        (antecedentes['compartir_ideas']['interesado'] | antecedentes['compartir_ideas']['mucho']),
        consecuencias['teatro']['alto']
    ),

    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho'] | antecedentes['artes']['moderado'] | antecedentes['artes']['algo']) &
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho'] | antecedentes['creatividad']['moderado'] | antecedentes['creatividad']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['autoexpresion']['interesado'] | antecedentes['autoexpresion']['mucho'] | antecedentes['autoexpresion']['moderado'] | antecedentes['autoexpresion']['algo']) &
        (antecedentes['creatividad_habilidad']['interesado'] | antecedentes['creatividad_habilidad']['mucho'] | antecedentes['creatividad_habilidad']['moderado'] | antecedentes['creatividad_habilidad']['algo']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho'] | antecedentes['trabajo_equipo']['moderado'] | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho'] | antecedentes['actividades_grupales']['moderado'] | antecedentes['actividades_grupales']['algo']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho'] | antecedentes['colaboracion']['moderado'] | antecedentes['colaboracion']['algo']) &
        (antecedentes['compartir_ideas']['interesado'] | antecedentes['compartir_ideas']['mucho'] | antecedentes['compartir_ideas']['moderado'] | antecedentes['compartir_ideas']['algo']),
        consecuencias['teatro']['medio']
    ),

    ctrl.Rule(
        (antecedentes['artes']['algo'] | antecedentes['artes']['desinteresado']) &
        (antecedentes['creatividad']['algo'] | antecedentes['creatividad']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['autoexpresion']['algo'] | antecedentes['autoexpresion']['desinteresado']) &
        (antecedentes['creatividad_habilidad']['algo'] | antecedentes['creatividad_habilidad']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo'] | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['actividades_grupales']['algo'] | antecedentes['actividades_grupales']['desinteresado']) &
        (antecedentes['colaboracion']['algo'] | antecedentes['colaboracion']['desinteresado']) &
        (antecedentes['compartir_ideas']['algo'] | antecedentes['compartir_ideas']['desinteresado']),
        consecuencias['teatro']['bajo']
    ),

    ############# MUSICA ############
    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho']) &
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['autoexpresion']['interesado'] | antecedentes['autoexpresion']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['expresion_artistica']['interesado'] | antecedentes['expresion_artistica']['mucho']),
        consecuencias['musica']['alto']
    ),

    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho'] | antecedentes['artes']['moderado'] | antecedentes['artes']['algo']) &
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho'] | antecedentes['creatividad']['moderado'] | antecedentes['creatividad']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['autoexpresion']['interesado'] | antecedentes['autoexpresion']['mucho'] | antecedentes['autoexpresion']['moderado'] | antecedentes['autoexpresion']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['expresion_artistica']['interesado'] | antecedentes['expresion_artistica']['mucho'] | antecedentes['expresion_artistica']['moderado'] | antecedentes['expresion_artistica']['algo']),
        consecuencias['musica']['medio']
    ),

    ctrl.Rule(
        (antecedentes['artes']['algo'] | antecedentes['artes']['desinteresado']) &
        (antecedentes['creatividad']['algo'] | antecedentes['creatividad']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['autoexpresion']['algo'] | antecedentes['autoexpresion']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['expresion_artistica']['algo'] | antecedentes['expresion_artistica']['desinteresado']),
        consecuencias['musica']['bajo']
    ),

    ############# DANZA ############
    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['expresion_artistica']['interesado'] | antecedentes['expresion_artistica']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho']) &
        (antecedentes['deportes_relajacion']['interesado'] | antecedentes['deportes_relajacion']['mucho']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho']) &
        (antecedentes['desarrollo_liderazgo']['interesado'] | antecedentes['desarrollo_liderazgo']['mucho']) &
        (antecedentes['equilibrio_salud']['interesado'] | antecedentes['equilibrio_salud']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['equilibrio_salud']['mucho']) &        
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho']),
        consecuencias['danza']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho'] | antecedentes['artes']['moderado'] | antecedentes['artes']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['expresion_artistica']['interesado'] | antecedentes['expresion_artistica']['mucho'] | antecedentes['expresion_artistica']['moderado'] | antecedentes['expresion_artistica']['algo']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho'] | antecedentes['trabajo_equipo']['moderado'] | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho'] | antecedentes['actividades_grupales']['moderado'] | antecedentes['actividades_grupales']['algo']) &
        (antecedentes['deportes_relajacion']['interesado'] | antecedentes['deportes_relajacion']['mucho'] | antecedentes['deportes_relajacion']['moderado'] | antecedentes['deportes_relajacion']['algo']) &
        (antecedentes['mejorar_habilidades']['interesado'] | antecedentes['mejorar_habilidades']['mucho'] | antecedentes['mejorar_habilidades']['moderado'] | antecedentes['mejorar_habilidades']['algo']) &
        (antecedentes['desarrollo_liderazgo']['interesado'] | antecedentes['desarrollo_liderazgo']['mucho'] | antecedentes['desarrollo_liderazgo']['moderado'] | antecedentes['desarrollo_liderazgo']['algo']) &
        (antecedentes['equilibrio_salud']['interesado'] | antecedentes['equilibrio_salud']['mucho'] | antecedentes['equilibrio_salud']['moderado'] | antecedentes['equilibrio_salud']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['danza']['medio']
    ),
        
    ctrl.Rule(
        (antecedentes['artes']['algo'] | antecedentes['artes']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['expresion_artistica']['algo'] | antecedentes['expresion_artistica']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo'] | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['actividades_grupales']['algo'] | antecedentes['actividades_grupales']['desinteresado']) &
        (antecedentes['deportes_relajacion']['algo'] | antecedentes['deportes_relajacion']['desinteresado']) &
        (antecedentes['mejorar_habilidades']['algo'] | antecedentes['mejorar_habilidades']['desinteresado']) &
        (antecedentes['desarrollo_liderazgo']['algo'] | antecedentes['desarrollo_liderazgo']['desinteresado']) &
        (antecedentes['equilibrio_salud']['algo'] | antecedentes['equilibrio_salud']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['danza']['bajo']
    ),

    ############# FOTOGRAFIA ############
    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho']) &
        (antecedentes['tecnologia']['interesado'] | antecedentes['tecnologia']['mucho']) &
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho']) &
        (antecedentes['creatividad_habilidad']['interesado'] | antecedentes['creatividad_habilidad']['mucho']) &
        (antecedentes['tecnologia_habilidad']['interesado'] | antecedentes['tecnologia_habilidad']['mucho']) &
        (antecedentes['expresion_artistica']['interesado'] | antecedentes['expresion_artistica']['mucho']) &
        (antecedentes['aprendizaje']['interesado'] | antecedentes['aprendizaje']['mucho']) &        
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']),
        consecuencias['fotografia']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['artes']['interesado'] | antecedentes['artes']['mucho'] | antecedentes['artes']['moderado'] | antecedentes['artes']['algo']) &
        (antecedentes['tecnologia']['interesado'] | antecedentes['tecnologia']['mucho'] | antecedentes['tecnologia']['moderado'] | antecedentes['tecnologia']['algo']) &
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho'] | antecedentes['creatividad']['moderado'] | antecedentes['creatividad']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho'] | antecedentes['independencia']['moderado'] | antecedentes['independencia']['algo']) &
        (antecedentes['creatividad_habilidad']['interesado'] | antecedentes['creatividad_habilidad']['mucho'] | antecedentes['creatividad_habilidad']['moderado'] | antecedentes['creatividad_habilidad']['algo']) &
        (antecedentes['tecnologia_habilidad']['interesado'] | antecedentes['tecnologia_habilidad']['mucho'] | antecedentes['tecnologia_habilidad']['moderado'] | antecedentes['tecnologia_habilidad']['algo']) &
        (antecedentes['expresion_artistica']['interesado'] | antecedentes['expresion_artistica']['mucho'] | antecedentes['expresion_artistica']['moderado'] | antecedentes['expresion_artistica']['algo']) &
        (antecedentes['aprendizaje']['interesado'] | antecedentes['aprendizaje']['mucho'] | antecedentes['aprendizaje']['moderado'] | antecedentes['aprendizaje']['algo']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho'] | antecedentes['desconectar']['moderado'] | antecedentes['desconectar']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']),
        consecuencias['fotografia']['medio']
    ),
        
    ctrl.Rule(
        (antecedentes['artes']['algo'] | antecedentes['artes']['desinteresado']) &
        (antecedentes['tecnologia']['algo'] | antecedentes['tecnologia']['desinteresado']) &
        (antecedentes['creatividad']['algo'] | antecedentes['creatividad']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['independencia']['algo'] | antecedentes['independencia']['desinteresado']) &
        (antecedentes['creatividad_habilidad']['algo'] | antecedentes['creatividad_habilidad']['desinteresado']) &
        (antecedentes['tecnologia_habilidad']['algo'] | antecedentes['tecnologia_habilidad']['desinteresado']) &
        (antecedentes['expresion_artistica']['algo'] | antecedentes['expresion_artistica']['desinteresado']) &
        (antecedentes['aprendizaje']['algo'] | antecedentes['aprendizaje']['desinteresado']) &
        (antecedentes['desconectar']['algo'] | antecedentes['desconectar']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']),
        consecuencias['fotografia']['bajo']
    ),
    
    ############# DEBATE ############
    ctrl.Rule(
        (antecedentes['autoexpresion']['interesado'] | antecedentes['autoexpresion']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['debates']['interesado'] | antecedentes['debates']['mucho']) &
        (antecedentes['compartir_ideas']['interesado'] | antecedentes['compartir_ideas']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['aprendizaje']['interesado'] | antecedentes['aprendizaje']['mucho']) &
        (antecedentes['autoexpresion_valor']['interesado'] | antecedentes['autoexpresion_valor']['mucho']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['debate']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['autoexpresion']['interesado'] | antecedentes['autoexpresion']['mucho'] | antecedentes['autoexpresion']['moderado'] | antecedentes['autoexpresion']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['debates']['interesado'] | antecedentes['debates']['mucho'] | antecedentes['debates']['moderado'] | antecedentes['debates']['algo']) &
        (antecedentes['compartir_ideas']['interesado'] | antecedentes['compartir_ideas']['mucho'] | antecedentes['compartir_ideas']['moderado'] | antecedentes['compartir_ideas']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['aprendizaje']['interesado'] | antecedentes['aprendizaje']['mucho'] | antecedentes['aprendizaje']['moderado'] | antecedentes['aprendizaje']['algo']) &
        (antecedentes['autoexpresion_valor']['interesado'] | antecedentes['autoexpresion_valor']['mucho'] | antecedentes['autoexpresion_valor']['moderado'] | antecedentes['autoexpresion_valor']['algo']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho'] | antecedentes['desconectar']['moderado'] | antecedentes['desconectar']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['debate']['medio']
    ),
        
    ctrl.Rule(
        (antecedentes['autoexpresion']['algo'] | antecedentes['autoexpresion']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['debates']['algo'] | antecedentes['debates']['desinteresado']) &
        (antecedentes['compartir_ideas']['algo'] | antecedentes['compartir_ideas']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['aprendizaje']['algo'] | antecedentes['aprendizaje']['desinteresado']) &
        (antecedentes['autoexpresion_valor']['algo'] | antecedentes['autoexpresion_valor']['desinteresado']) &
        (antecedentes['desconectar']['algo'] | antecedentes['desconectar']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['debate']['bajo']
    ),
    
    ############# CIENCIA_TECNOLOGIA ############
    ctrl.Rule(
        (antecedentes['ciencia']['interesado'] | antecedentes['ciencia']['mucho']) &
        (antecedentes['tecnologia']['interesado'] | antecedentes['tecnologia']['mucho']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho']) &
        (antecedentes['tecnologia_habilidad']['interesado'] | antecedentes['tecnologia_habilidad']['mucho']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho']) &
        (antecedentes['compartir_ideas']['interesado'] | antecedentes['compartir_ideas']['mucho']) &
        (antecedentes['aprendizaje']['algo'] | antecedentes['aprendizaje']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['ciencia_tecnologia']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['ciencia']['interesado'] | antecedentes['ciencia']['mucho'] | antecedentes['ciencia']['moderado'] | antecedentes['ciencia']['algo']) &
        (antecedentes['tecnologia']['interesado'] | antecedentes['tecnologia']['mucho'] | antecedentes['tecnologia']['moderado'] | antecedentes['tecnologia']['algo']) &
        (antecedentes['social']['interesado'] | antecedentes['social']['mucho'] | antecedentes['social']['moderado'] | antecedentes['social']['algo']) &
        (antecedentes['tecnologia_habilidad']['interesado'] | antecedentes['tecnologia_habilidad']['mucho'] | antecedentes['tecnologia_habilidad']['moderado'] | antecedentes['tecnologia_habilidad']['algo']) &
        (antecedentes['trabajo_equipo']['interesado'] | antecedentes['trabajo_equipo']['mucho'] | antecedentes['trabajo_equipo']['moderado'] | antecedentes['trabajo_equipo']['algo']) &
        (antecedentes['actividades_grupales']['interesado'] | antecedentes['actividades_grupales']['mucho'] | antecedentes['actividades_grupales']['moderado'] | antecedentes['actividades_grupales']['algo']) &
        (antecedentes['colaboracion']['interesado'] | antecedentes['colaboracion']['mucho'] | antecedentes['colaboracion']['moderado'] | antecedentes['colaboracion']['algo']) &
        (antecedentes['compartir_ideas']['interesado'] | antecedentes['compartir_ideas']['mucho'] | antecedentes['compartir_ideas']['moderado'] | antecedentes['compartir_ideas']['algo']) &
        (antecedentes['aprendizaje']['interesado'] | antecedentes['aprendizaje']['mucho'] | antecedentes['aprendizaje']['moderado'] | antecedentes['aprendizaje']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']) &
        (antecedentes['crecimiento_personal']['interesado'] | antecedentes['crecimiento_personal']['mucho'] | antecedentes['crecimiento_personal']['moderado'] | antecedentes['crecimiento_personal']['algo']),
        consecuencias['ciencia_tecnologia']['medio']
    ),
        
    ctrl.Rule(
        (antecedentes['ciencia']['algo'] | antecedentes['ciencia']['desinteresado']) &
        (antecedentes['tecnologia']['algo'] | antecedentes['tecnologia']['desinteresado']) &
        (antecedentes['social']['algo'] | antecedentes['social']['desinteresado']) &
        (antecedentes['tecnologia_habilidad']['algo'] | antecedentes['tecnologia_habilidad']['desinteresado']) &
        (antecedentes['trabajo_equipo']['algo'] | antecedentes['trabajo_equipo']['desinteresado']) &
        (antecedentes['actividades_grupales']['algo'] | antecedentes['actividades_grupales']['desinteresado']) &
        (antecedentes['colaboracion']['algo'] | antecedentes['colaboracion']['desinteresado']) &
        (antecedentes['compartir_ideas']['algo'] | antecedentes['compartir_ideas']['desinteresado']) &
        (antecedentes['aprendizaje']['algo'] | antecedentes['aprendizaje']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']) &
        (antecedentes['crecimiento_personal']['algo'] | antecedentes['crecimiento_personal']['desinteresado']),
        consecuencias['ciencia_tecnologia']['bajo']
    ),
    ############# AJEDREZ ############
    ctrl.Rule(
        (antecedentes['ciencia']['interesado'] | antecedentes['ciencia']['mucho']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho']) &
        (antecedentes['resolucion_problemas']['interesado'] | antecedentes['resolucion_problemas']['mucho']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho']),
        consecuencias['ajedrez']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['ciencia']['interesado'] | antecedentes['ciencia']['mucho'] | antecedentes['ciencia']['moderado'] | antecedentes['ciencia']['algo']) &
        (antecedentes['competitividad']['interesado'] | antecedentes['competitividad']['mucho'] | antecedentes['competitividad']['moderado'] | antecedentes['competitividad']['algo']) &
        (antecedentes['resolucion_problemas']['interesado'] | antecedentes['resolucion_problemas']['mucho'] | antecedentes['resolucion_problemas']['moderado'] | antecedentes['resolucion_problemas']['algo']) &
        (antecedentes['competir']['interesado'] | antecedentes['competir']['mucho'] | antecedentes['competir']['moderado'] | antecedentes['competir']['algo']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho'] | antecedentes['desconectar']['moderado'] | antecedentes['desconectar']['algo']) &
        (antecedentes['aprender_nueva_habilidad']['interesado'] | antecedentes['aprender_nueva_habilidad']['mucho'] | antecedentes['aprender_nueva_habilidad']['moderado'] | antecedentes['aprender_nueva_habilidad']['algo']),
        consecuencias['ajedrez']['medio']
    ),
        
    ctrl.Rule(
        (antecedentes['ciencia']['algo'] | antecedentes['ciencia']['desinteresado']) &
        (antecedentes['competitividad']['algo'] | antecedentes['competitividad']['desinteresado']) &
        (antecedentes['resolucion_problemas']['algo'] | antecedentes['resolucion_problemas']['desinteresado']) &
        (antecedentes['competir']['algo'] | antecedentes['competir']['desinteresado']) &
        (antecedentes['desconectar']['algo'] | antecedentes['desconectar']['desinteresado']) &
        (antecedentes['aprender_nueva_habilidad']['algo'] | antecedentes['aprender_nueva_habilidad']['desinteresado']),
        consecuencias['ajedrez']['bajo']
    ),
    ############# COCINA_GASTRONOMIA ############
    ctrl.Rule(
        (antecedentes['resolucion_problemas']['interesado'] | antecedentes['resolucion_problemas']['mucho']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho']),
        consecuencias['cocina_gastronomia']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['resolucion_problemas']['interesado'] | antecedentes['resolucion_problemas']['mucho'] | antecedentes['resolucion_problemas']['moderado'] | antecedentes['resolucion_problemas']['algo']) &
        (antecedentes['superar_limites']['interesado'] | antecedentes['superar_limites']['mucho'] | antecedentes['superar_limites']['moderado'] | antecedentes['superar_limites']['algo']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho'] | antecedentes['desconectar']['moderado'] | antecedentes['desconectar']['algo']),
        consecuencias['cocina_gastronomia']['medio']
    ),
        
    ctrl.Rule(
        (antecedentes['resolucion_problemas']['algo'] | antecedentes['resolucion_problemas']['desinteresado']) &
        (antecedentes['superar_limites']['algo'] | antecedentes['superar_limites']['desinteresado']) &
        (antecedentes['desconectar']['algo'] | antecedentes['desconectar']['desinteresado']),
        consecuencias['cocina_gastronomia']['bajo']
    ),
    ############# ESCRITURA_CREATIVA ############
    ctrl.Rule(
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho']) &
        (antecedentes['creatividad_habilidad']['interesado'] | antecedentes['creatividad_habilidad']['mucho']) &
        (antecedentes['autoexpresion_valor']['interesado'] | antecedentes['autoexpresion_valor']['mucho']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho']) &
        (antecedentes['creatividad_relajacion']['interesado'] | antecedentes['creatividad_relajacion']['mucho']),
        consecuencias['escritura_creativa']['alto']
    ),
    
    ctrl.Rule(
        (antecedentes['creatividad']['interesado'] | antecedentes['creatividad']['mucho'] | antecedentes['creatividad']['moderado'] | antecedentes['creatividad']['algo']) &
        (antecedentes['independencia']['interesado'] | antecedentes['independencia']['mucho'] | antecedentes['independencia']['moderado'] | antecedentes['independencia']['algo']) &
        (antecedentes['creatividad_habilidad']['interesado'] | antecedentes['creatividad_habilidad']['mucho'] | antecedentes['creatividad_habilidad']['moderado'] | antecedentes['creatividad_habilidad']['algo']) &
        (antecedentes['autoexpresion_valor']['interesado'] | antecedentes['autoexpresion_valor']['mucho'] | antecedentes['autoexpresion_valor']['moderado'] | antecedentes['autoexpresion_valor']['algo']) &
        (antecedentes['desconectar']['interesado'] | antecedentes['desconectar']['mucho'] | antecedentes['desconectar']['moderado'] | antecedentes['desconectar']['algo']) &
        (antecedentes['creatividad_relajacion']['interesado'] | antecedentes['creatividad_relajacion']['mucho'] | antecedentes['creatividad_relajacion']['moderado'] | antecedentes['creatividad_relajacion']['algo']),
        consecuencias['escritura_creativa']['medio']
    ),
        
    ctrl.Rule(
        (antecedentes['creatividad']['algo'] | antecedentes['creatividad']['desinteresado']) &
        (antecedentes['independencia']['algo'] | antecedentes['independencia']['desinteresado']) &
        (antecedentes['creatividad_habilidad']['algo'] | antecedentes['creatividad_habilidad']['desinteresado']) &
        (antecedentes['autoexpresion_valor']['algo'] | antecedentes['autoexpresion_valor']['desinteresado']) &
        (antecedentes['desconectar']['algo'] | antecedentes['desconectar']['desinteresado']) &
        (antecedentes['creatividad_relajacion']['algo'] | antecedentes['creatividad_relajacion']['desinteresado']),
        consecuencias['escritura_creativa']['bajo']
    )
]

# Crear el sistema de control difuso y su simulador
# 1. Crear un sistema de control basado en las reglas definidas.
sistema_control = ctrl.ControlSystem(reglas)
# 2. Crear un simulador del sistema de control para procesar las entradas y generar las salidas.
sistema_simulador  = ctrl.ControlSystemSimulation(sistema_control)

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
    for Actividad, nivel_recomendacion in recomedaciones.items():
        print(f"{Actividad}: {nivel_recomendacion}")


respuestas_usuario = {
    'deportes' : 4,
    'artes' : 4,
    'ciencia' : 4,
    'tecnologia' : 5,
    'creatividad' : 5,
    'social' : 5,
    #'liderazgo' : 0,
    'autoexpresion' : 5,
    'competitividad' : 5,
    'independencia' : 5,
    'coordinacion' : 4,
    'creatividad_habilidad' : 4,
    'tecnologia_habilidad' : 5,
    'resolucion_problemas' : 4,
    'expresion_artistica' : 5,
    'trabajo_equipo' : 4,
    'debates' : 4,
    'actividades_grupales' : 4,
    'colaboracion' : 5,
    'compartir_ideas' : 5,
    'competir' : 5,
    'aprendizaje' : 5,
    #'ayudar' : 0,
    'autoexpresion_valor' : 4,
    'superar_limites' : 4,
    #'relajacion' : 0,
    'liberar_energia' : 4,
    'desconectar' : 4,
    'creatividad_relajacion' : 5,
    'deportes_relajacion' : 5,
    'mejorar_habilidades' : 4,
    'desarrollo_liderazgo' : 5,
    'equilibrio_salud' : 4,
    'aprender_nueva_habilidad' : 4,
    'crecimiento_personal' : 5
}

actividad_recomendada = recomendar_actividad(respuestas_usuario)
mostrar_respuesta(actividad_recomendada)