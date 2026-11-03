"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import csv
import time
import os

from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.List import array_list as al


data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/singapur_bus_routes/'


def new_logic():
    """Inicializa el analizador.

    stops: Lista para guardar las paradas de bus (array_list)
    routes_pq: Cola de prioridad para gestionar las rutas de bus (priority_queue)

    Returns:
        dict: Analizador con las claves 'stops' y 'routes_pq' inicializadas a None.
    """
    analyzer = {
        'stops': None,
        'routes_pq': None
    }
    
    analyzer['stops'] = al.new_list()
    analyzer['routes_pq'] = pq.new_heap()

    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def load_data(analyzer, file):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    file = data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for stop in input_file:
        add_stop(analyzer, stop)
    return analyzer


def add_stop(analyzer, stop):
    """
    Adiciona una parada al analizador.

    Parámetros:
    ------------
    analyzer : dict
        Estructura de datos principal del analizador que contiene, entre otros,
        la lista de paradas ('stops') y la cola de prioridad ('pq').
    stop : dict
        Información completa de una parada de bus, que incluye al menos los campos:
        - ServiceNo: número de la ruta del bus
        - Direction: dirección del recorrido (1 o 2)
        - StopSequence: número de secuencia de la parada en la ruta
        - WD_FirstBus: hora de salida del primer bus en día laboral
        (además de otros datos complementarios)
    """

    # Agregar la parada a la lista general de paradas
    al.add_last(analyzer['stops'], stop)

    # Solo la primera parada de cada ruta-dirección entra a la cola de prioridad
    if int(stop['StopSequence']) == 1:
        elemento = {
            'route_id': stop['ServiceNo'],
            'direction': stop['Direction'],
            'priority': stop['WD_FirstBus']
        }
        # Se convierte a int para comparar horas HHMM sin depender de ceros a la izquierda.
        # Las rutas sin servicio entre semana ('-') quedan al final de la cola
        horasalida = elemento['priority']
        if horasalida.isdigit():
            prioridad = int(horasalida)
        else:
            prioridad = 9999
        # El archivo trae rutas repetidas (ej. 410 dirección 1); cada ruta-dirección entra una sola vez
        if not pq.contains(analyzer['routes_pq'], elemento):
            pq.insert(analyzer['routes_pq'], prioridad, elemento)

    return analyzer


# ___________________________________________________
#  Funciones de consulta
# ___________________________________________________

def stops_size(analyzer):
    """
    Obtener el número de paradas de bus
    """
    return al.size(analyzer['stops'])

def pq_size(analyzer):
    """
    Obtener el número de elementos en la cola de prioridad
    """
    return pq.size(analyzer['routes_pq'])

def pq_first(analyzer):
    """
    Obtener el primer elemento en la cola de prioridad
    """
    return pq.get_first_priority(analyzer['routes_pq'])

def get_next_route(analyzer):
    """
    Atiende la cola de prioridad del analizador.

    Esta función consulta la ruta con mayor prioridad (es decir, la de menor valor 
    de 'WD_FirstBus'), la elimina de la cola de prioridad y retorna la información 
    de dicha ruta.

    Parámetros:
    ------------
    analyzer : dict
        Estructura de datos principal del analizador que contiene, entre otros,
        la cola de prioridad ('pq') con las rutas pendientes de procesar.

    """

    # remove retorna la ruta con mayor prioridad y la retira de la cola
    sigruta = pq.remove(analyzer['routes_pq'])
    return sigruta


