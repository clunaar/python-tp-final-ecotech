"""Dominio del catálogo: jerarquía de productos ecológicos (Punto A)."""

from excepciones import StockInvalidoError


class DispositivoEcológico:
    """Clase base de todo producto del catálogo.

    El stock está encapsulado: se guarda en un atributo privado y solo se
    modifica a través de la propiedad `stock`, que valida la regla de negocio.
    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.__stock = 0
        self.stock = stock  # pasa por el setter y se valida

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
            raise StockInvalidoError(valor)
        self.__stock = valor

    def ficha_tecnica(self) -> str:
        return (
            f"[{self.codigo}] {self.nombre}\n"
            f"  Precio: ${self.precio:,.2f}\n"
            f"  Stock disponible: {self.stock} u."
        )

    def to_dict(self) -> dict:
        """Representación serializable para la persistencia en JSON."""
        return {
            "tipo": type(self).__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return f"{self.nombre} ({self.codigo})"


class PanelSolar(DispositivoEcológico):
    """Producto especializado: hereda de DispositivoEcológico y agrega
    potencia y eficiencia. Sobrescribe la ficha técnica (polimorfismo)."""

    def __init__(self, codigo, nombre, precio, stock, potencia_w: int, eficiencia: float):
        super().__init__(codigo, nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia

    def ficha_tecnica(self) -> str:
        return (
            super().ficha_tecnica()
            + f"\n  Potencia: {self.potencia_w} W"
            + f"\n  Eficiencia: {self.eficiencia:.1%}"
        )

    def to_dict(self) -> dict:
        datos = super().to_dict()
        datos.update({"potencia_w": self.potencia_w, "eficiencia": self.eficiencia})
        return datos
