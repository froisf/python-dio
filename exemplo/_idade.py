from pydantic import BaseModel, Field, ValidationError
class Pessoa(BaseModel):
    nome: str = Field(..., min_length=3, description="Nome da pessoa")
    idade: int = Field(..., ge=0, le=120, description="Idade da pessoa (0-120 anos)")

    @property
    def pode_tirar_habilitacao(self) -> bool:
        """Verifica se a pessoa tem idade suficiente para tirar habilitação."""
        return self.idade >= 18
    
if __name__ == "__main__":
    print("=== TESTE 1: Dados Válidos ===")

    pessoa_valida = Pessoa(nome="João", idade=15)
        
    print(pessoa_valida.model_dump())
    if pessoa_valida.pode_tirar_habilitacao:
        print("João pode tirar habilitação.")
    else:
        print("João NÃO pode tirar habilitação.")
