import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from itertools import combinations
import math

class System_expert_fuzzy():
    def __init__(self ,nombre_actividad, caracteristicas_psicologicas):
        self.caracteristicas = caracteristicas_psicologicas
        self.actividad = nombre_actividad
        self.antecedentes_difusos = {}
        self.consecuente_difuso = {}
        self.reglas_difusas = []

    def crear_antecedentes_difusos(self):
        # Crear un diccionario para almacenar los antecedentes difusos
        for variable in self.caracteristicas:
            self.antecedentes_difusos[variable] = ctrl.Antecedent(np.arange(1, 6, 1), variable)
        
        # Definir los conjuntos difusos para todas las variables antecedentes
        for variable_difuso in self.antecedentes_difusos:
            self.antecedentes_difusos[variable_difuso]['bajo'] = fuzz.trimf(self.antecedentes_difusos[variable_difuso].universe, [1, 1, 3])
            self.antecedentes_difusos[variable_difuso]['medio'] = fuzz.trimf(self.antecedentes_difusos[variable_difuso].universe, [2, 3, 4])
            self.antecedentes_difusos[variable_difuso]['alta'] = fuzz.trimf(self.antecedentes_difusos[variable_difuso].universe, [3, 5, 5])

    def crear_consecuente_difusos(self):
        # Crear el consecuente difuso para la actividad
        self.consecuente_difuso = ctrl.Consequent(np.arange(1, 4, 1), self.actividad)

        # Definir los conjuntos difusos para el consecuente
        self.consecuente_difuso['bajo'] = fuzz.trimf(self.consecuente_difuso.universe, [1, 1, 2])
        self.consecuente_difuso['alta'] = fuzz.trimf(self.consecuente_difuso.universe, [2, 3, 3])

    #Esta función se encarga de crear y definir reglas difusas para un sistema de control difuso. Las reglas se basan en las características del sistema y en los valores de los #antecedentes difusos y consecuentes difusos
    def crear_reglas_difusas(self):
        #Llamada a Métodos para Crear Antecedentes y Consecuentes Difusos
        self.crear_antecedentes_difusos()
        self.crear_consecuente_difusos()

        # Cálculo de Combinaciones de Características
        conjunto_maximo_caracteristicas_bajas = math.ceil(len(self.caracteristicas) / 2)
        combinaciones_bajas = list(combinations(self.caracteristicas, conjunto_maximo_caracteristicas_bajas))
        #Aquí se determina cuántas características mínimas se deben combinar para formar reglas. Se calcula la mitad del número total de características y se genera una lista de todas las combinaciones posibles de esas características.

        condicion_baja = None

        # Se itera sobre cada combinación de características en la lista combinaciones_bajas. 
        # Cada combinacion es una tupla que contiene un subconjunto de características
        # Ejemplo: Supongamos que combinaciones_bajas tiene las combinaciones [('A', 'B'), ('C', 'D')]. El primer combinacion en el bucle podría ser ('A', 'B').
        for combinacion in combinaciones_bajas:
            # Se establece condicion_actual con el valor de la condición 'bajo' del primer antecedente en la combinación actual.
            # Ejemplo: Si la combinación es ('A', 'B'), entonces condicion_actual se inicializa con el valor de self.antecedentes_difusos['A']['bajo'].
            condicion_actual = self.antecedentes_difusos[combinacion[0]]['bajo']
            for antecedente in combinacion[1:]:
                condicion_actual &= self.antecedentes_difusos[antecedente]['bajo']
            # Para cada antecedente adicional en la combinación, se actualiza condicion_actual combinando la condición 'bajo' del antecedente con condicion_actual usando la operación lógica AND (&)
            # Ejemplo: Si la combinación es ('A', 'B') y condicion_actual inicialmente es self.antecedentes_difusos['A']['bajo'], entonces condicion_actual se combina con self.antecedentes_difusos['B']['bajo'] usando &.
            
            if condicion_baja is None:
                condicion_baja = condicion_actual
            else:
                condicion_baja |= condicion_actual

        #regla1 establece que si la condición compuesta es 'baja', el consecuente debe ser 'bajo'.
        # ejemplo: si exite un conjunto de 5 caracteristicas o mas con nivel bajo la consecuencia sera de recomendacion baja "regla1", en caso contrario la consecuencia sera de recomendacion alta "regla2".
        regla1 = ctrl.Rule(
            condicion_baja,
            self.consecuente_difuso['bajo']
        )
        
        #regla2 establece que si la condición compuesta no es 'baja' (lo que se denota por ~condicion_baja), el consecuente debe ser 'alta'.
        regla2 = ctrl.Rule(
            ~condicion_baja,
            self.consecuente_difuso['alta']
        )
        
        self.reglas_difusas.extend([regla1, regla2])

    def obtener_grado_recomendacion(self, valor_caracteristica):
        self.crear_reglas_difusas()

        # Crear el sistema de control
        system_fuzzy = ctrl.ControlSystem(self.reglas_difusas)
        fuzzy_simulator = ctrl.ControlSystemSimulation(system_fuzzy)

        
        for nombre, valor in valor_caracteristica.items():
            fuzzy_simulator.input[nombre] = valor
        
        # Aquí puedes agregar la lógica para la simulación o evaluación
        fuzzy_simulator.compute()

        resultado = fuzzy_simulator.output[self.actividad]

        return resultado
    
    def imprimir_recomendacion(self, valor_caracteristica):
        grado_recomendacion = self.obtener_grado_recomendacion(valor_caracteristica)

        print(f"Recomendación para la actividad de {self.actividad}: {round(grado_recomendacion,2)}")

        # Interpretar el resultado en términos cualitativos
        if grado_recomendacion <= 1.5:
            print("Recomendación: Baja")
        elif 1.5 < grado_recomendacion <= 2.5:
            print("Recomendación: Media")
        else:
            print("Recomendación: Alta")

antecedentes = [
    "resistencia",
    "velocidad",
    "fuerza",
    "coordinacion_superior",
    "coordinacion_inferior",
    "resiliencia",
    "trabajo_individual"
]

inputs_natacion = {
    "resistencia" : 5,
    "velocidad" : 1,
    "fuerza" : 5,
    "coordinacion_superior" : 1,
    "coordinacion_inferior" : 5,
    "resiliencia" : 1,
    "trabajo_individual" : 5
}

sistema = System_expert_fuzzy('futbol', antecedentes)
sistema.imprimir_recomendacion(inputs_natacion)