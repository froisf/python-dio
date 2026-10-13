from pydantic import BaseModel, Field, ValidationError

# 1. Definindo o contrato de dados (Schema) para o Agente de IA
class ConfigAgenteIA(BaseModel):
    nome_agente: str = Field(..., min_length=3, description="Nome do agente")
    temperatura: float = Field(default=0.7, ge=0.0, le=1.0) # Deve estar entre 0.0 e 1.0
    max_tokens: int = Field(default=1000, gt=0) # Deve ser maior que 0

print("=== TESTE 1: Dados Válidos ===")
try:
    agente_valido = ConfigAgenteIA(
        nome_agente="AgenteRevisor",
        temperatura=0.2,
        max_tokens=500
    )
    print("✅ Sucesso:", agente_valido.model_dump())
except ValidationError as e:
    print("❌ Erro inesperado:", e)

print("\n=== TESTE 2: Dados Inválidos (Temperatura > 1.0) ===")
try:
    # Tentando passar temperatura 2.5 (inválida)
    agente_invalido = ConfigAgenteIA(
        nome_agente="AgenteErro",
        temperatura=2.5
    )
except ValidationError as e:
    print("🚨 Pydantic barrou o erro automaticamente:")
    print(e)