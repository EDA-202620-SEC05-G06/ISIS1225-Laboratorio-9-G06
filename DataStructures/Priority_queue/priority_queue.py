
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


def sink(heap, pos):
    """
    Baja el elemento en la posición pos mientras alguno de sus hijos
    tenga más prioridad que él.
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
    Retira la entrada con mayor prioridad (la raíz) y retorna su valor.
    El último elemento pasa a la raíz y se baja con sink.
    Retorna None si el heap está vacío.
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
    Retorna el valor de la entrada con mayor prioridad sin retirarla.
    Retorna None si el heap está vacío.
    """
    if is_empty(heap):
        return None
    return pqe.get_value(al.get_element(heap["elements"], 1))


def is_present_value(heap, valor):
    """
    Retorna la posición de la entrada cuyo valor es valor,
    o -1 si no está en el heap.
    """
    for pos in range(1, size(heap) + 1):
        entrada = al.get_element(heap["elements"], pos)
        if pqe.get_value(entrada) == valor:
            return pos
    return -1


def contains(heap, valor):
    """
    Indica si existe una entrada con el valor dado en el heap.
    """
    return is_present_value(heap, valor) != -1


def improve_priority(heap, prioridad, valor):
    """
    Cambia la prioridad de la entrada con el valor dado por una mejor
    y la sube hasta su posición correcta con swim.
    """
    pos = is_present_value(heap, valor)
    if pos != -1:
        entrada = al.get_element(heap["elements"], pos)
        pqe.set_priority(entrada, prioridad)
        swim(heap, pos)
    return heap
