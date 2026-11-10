"""Excepciones de negocio del catálogo EcoTech."""


class StockInvalidoError(Exception):
    """Se eleva cuando se intenta asignar un stock negativo o no entero."""

    def __init__(self, valor, mensaje="El stock debe ser un número entero mayor o igual a 0"):
        self.valor = valor
        super().__init__(f"{mensaje} (valor recibido: {valor!r})")
