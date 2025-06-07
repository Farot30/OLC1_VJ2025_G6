class Errores:
    def __init__(self, tipo: str, desc: str, linea: int, col: int):
        self.tipoError = tipo
        self.desc = desc
        self.linea = linea
        self.col = col

    def get_desc(self) -> str:
        return self.desc

    def get_tipo_error(self) -> str:
        return self.tipoError

    def get_linea(self) -> int:
        return self.linea

    def get_col(self) -> int:
        return self.col

    def get_errores(self) -> dict:
        return {
            "tipo": self.tipoError,
            "desc": self.desc,
            "linea": self.linea,
            "col": self.col
        }

    def __str__(self) -> str:
        return f"----- Error {self.tipoError}: {self.desc} en la linea {self.linea} y columna {self.col} ----"
