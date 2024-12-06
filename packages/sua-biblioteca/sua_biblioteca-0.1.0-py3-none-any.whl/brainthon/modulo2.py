# modulo2.py
# Este módulo contém funções básicas de multiplicação e divisão.

def multiplicar(a, b):
    """Multiplica dois números."""
    return a * b

def dividir(a, b):
    """Divide o primeiro número pelo segundo.
    Retorna None se a divisão por zero for tentada."""
    if b == 0:
        return None
    return a / b
