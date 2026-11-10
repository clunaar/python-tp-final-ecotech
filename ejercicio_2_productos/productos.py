# Ejercicio 2 - Punto A: Dominio del catálogo y reglas de inventario


# Excepción personalizada
class StockInvalidoError(Exception):
    def __init__(self, mensaje="El stock no puede ser negativo"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


# Clase base
class DispositivoEcológico:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.__stock = 0  # atributo privado (encapsulamiento)
        self.set_stock(stock)

    def get_stock(self):
        return self.__stock

    def set_stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise StockInvalidoError(f"Stock inválido para {self.nombre}: {nuevo_stock}")
        self.__stock = nuevo_stock

    def ficha_tecnica(self):
        return f"{self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.__stock}"

    def a_diccionario(self):
        return {
            "tipo": "DispositivoEcologico",
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.__stock,
        }


# Clase hija: hereda de DispositivoEcológico
class PanelSolar(DispositivoEcológico):
    def __init__(self, nombre, precio, stock, potencia_watts, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_watts = potencia_watts
        self.eficiencia = eficiencia

    # Polimorfismo: personalizamos la ficha técnica
    def ficha_tecnica(self):
        ficha = super().ficha_tecnica()
        return f"{ficha} | Potencia: {self.potencia_watts} W | Eficiencia: {self.eficiencia}%"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["tipo"] = "PanelSolar"
        datos["potencia_watts"] = self.potencia_watts
        datos["eficiencia"] = self.eficiencia
        return datos
