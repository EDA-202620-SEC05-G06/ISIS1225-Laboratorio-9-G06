
from DataStructures.List import array_list as al
from DataStructures.Priority_queue import pq_entry as pqe


def new_heap(esminpq=True):
    """
    Crea una cola de prioridad vacía (a menor por defecto).
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
    True si el padre tiene mayor o igual prioridad que el hijo.
    """
    if pqe.get_priority(nodopadre) >= pqe.get_priority(nodohijo):
        return True
    return False


def default_compare_lower_value(nodopadre, nodohijo):
    """
    True si el padre tiene menor o igual prioridad que el hijo.
    """
    if pqe.get_priority(nodopadre) <= pqe.get_priority(nodohijo):
        return True
    return False


def priority(heap, padre, hijo):
    """
    True si el padre tiene más prioridad que el hijo.
    """
    return heap["cmp_function"](padre, hijo)


def exchange(heap, pos1, pos2):
    """
    Intercambia dos elementos del heap.
    """
    al.exchange(heap["elements"], pos1, pos2)


def size(heap):
    """
    Retorna el número de elementos.
    """
    return heap["size"]


def is_empty(heap):
    """
    Indica si el heap está vacío.
    """
    return size(heap) == 0


def insert(heap, prioridad, valor):
    """
    Agrega un elemento y lo sube con swim.
    """
    entrada = pqe.new_pq_entry(prioridad, valor)
    al.add_last(heap["elements"], entrada)
    heap["size"] += 1
    swim(heap, heap["size"])
    return heap


def swim(heap, pos):
    """
    Sube el elemento hasta su posición correcta.
    """
    while pos > 1:
        pospadre = pos // 2
        padre = al.get_element(heap["elements"], pospadre)
        actual = al.get_element(heap["elements"], pos)
        if priority(heap, padre, actual):
            break
        exchange(heap, pos, pospadre)
        pos = pospadre


def sink(heap, pos):
    """
    Baja el elemento hasta su posición correcta.
    """
    tamano = size(heap)
    while 2 * pos <= tamano:
        poshijo = 2 * pos
        if poshijo < tamano:
            hijoizq = al.get_element(heap["elements"], poshijo)
            hijoder = al.get_element(heap["elements"], poshijo + 1)
            if not priority(heap, hijoizq, hijoder):
                poshijo += 1
        actual = al.get_element(heap["elements"], pos)
        hijo = al.get_element(heap["elements"], poshijo)
        if priority(heap, actual, hijo):
            break
        exchange(heap, pos, poshijo)
        pos = poshijo


def remove(heap):
    """
    Retira la raíz y retorna su valor (None si está vacío).
    """
    if is_empty(heap):
        return None
    raiz = al.get_element(heap["elements"], 1)
    exchange(heap, 1, size(heap))
    al.remove_last(heap["elements"])
    heap["size"] -= 1
    sink(heap, 1)
    return pqe.get_value(raiz)


def get_first_priority(heap):
    """
    Retorna el valor de la raíz sin retirarla (None si está vacío).
    """
    if is_empty(heap):
        return None
    return pqe.get_value(al.get_element(heap["elements"], 1))


def is_present_value(heap, valor):
    """
    Retorna la posición del valor o -1 si no está.
    """
    for pos in range(1, size(heap) + 1):
        entrada = al.get_element(heap["elements"], pos)
        if pqe.get_value(entrada) == valor:
            return pos
    return -1


def contains(heap, valor):
    """
    Indica si el valor está en el heap.
    """
    return is_present_value(heap, valor) != -1


def improve_priority(heap, prioridad, valor):
    """
    Mejora la prioridad de un valor y lo sube con swim.
    """
    pos = is_present_value(heap, valor)
    if pos != -1:
        entrada = al.get_element(heap["elements"], pos)
        pqe.set_priority(entrada, prioridad)
        swim(heap, pos)
    return heap
