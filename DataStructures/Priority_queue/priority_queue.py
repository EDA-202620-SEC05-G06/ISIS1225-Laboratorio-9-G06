
from DataStructures.List import array_list as al
from DataStructures.Priority_queue import pq_entry as pqe


def new_heap(esminpq=True):
    """
    Crea una cola de prioridad vacía orientada a menor o a mayor
    dependiendo del valor de esminpq.
    """
    heap = {
        "elements": al.new_list(),
        "size": 0,
        "cmp_function": None,
    }
    al.add_last(heap["elements"], None)
    if esminpq:
        heap["cmp_function"] = default_compare_lower_value
    else:
        heap["cmp_function"] = default_compare_higher_value
    return heap


def default_compare_higher_value(nodopadre, nodohijo):
    """
    Retorna True si el padre tiene mayor o igual prioridad que el hijo
    (cola orientada a mayor).
    """
    if pqe.get_priority(nodopadre) >= pqe.get_priority(nodohijo):
        return True
    return False


def default_compare_lower_value(nodopadre, nodohijo):
    """
    Retorna True si el padre tiene menor o igual prioridad que el hijo
    (cola orientada a menor).
    """
    if pqe.get_priority(nodopadre) <= pqe.get_priority(nodohijo):
        return True
    return False


def priority(heap, padre, hijo):
    """
    Indica si el padre tiene más prioridad que el hijo según la
    función de comparación del heap.
    """
    return heap["cmp_function"](padre, hijo)


def exchange(heap, pos1, pos2):
    """
    Intercambia los elementos en las posiciones pos1 y pos2 del heap.
    """
    al.exchange(heap["elements"], pos1, pos2)


def size(heap):
    """
    Retorna el número de elementos en el heap.
    """
    return heap["size"]


def is_empty(heap):
    """
    Indica si el heap está vacío.
    """
    return size(heap) == 0


def insert(heap, prioridad, valor):
    """
    Agrega un nuevo elemento al final del heap y lo sube hasta su
    posición correcta con swim.
    """
    entrada = pqe.new_pq_entry(prioridad, valor)
    al.add_last(heap["elements"], entrada)
    heap["size"] += 1
    swim(heap, heap["size"])
    return heap


def swim(heap, pos):
    """
    Sube el elemento en la posición pos mientras tenga más prioridad
    que su padre.
    """
    while pos > 1:
        pospadre = pos // 2
        padre = al.get_element(heap["elements"], pospadre)
        actual = al.get_element(heap["elements"], pos)
        if priority(heap, padre, actual):
            break
        exchange(heap, pos, pospadre)
        pos = pospadre
