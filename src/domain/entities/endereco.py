from dataclasses import dataclass


@dataclass(frozen=True)
class Endereco:
    rua: str
    numero: str

    def __post_init__(self):
        if not self.rua or not self.rua.strip():
            raise ValueError("rua é obrigatória")
        if not self.numero or not self.numero.strip():
            raise ValueError("número é obrigatório")

        object.__setattr__(self, "rua", self.rua.strip())
        object.__setattr__(self, "numero", self.numero.strip())
