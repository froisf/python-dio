"""
context_engine.py

Manipulador e Validador de Contexto para Engenharia de IA.
Combina `pathlib.Path` para varredura determinística do sistema de arquivos 
e `Pydantic v2` para tipagem, validação e controle do orçamento de tokens (Dynamic Context Windows).

Projeto: python-dio
"""

from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, field_validator


class CodeFile(BaseModel):
    """Modelo Pydantic que valida e tipa um arquivo do projeto."""
    file_path: str = Field(..., description="Caminho relativo do arquivo no repositório")
    content: str = Field(..., description="Conteúdo em texto do arquivo")
    language: str = Field(default="python", description="Linguagem para formatação Markdown")
    tokens: int = Field(default=0, description="Estimativa aproximada de tokens")

    @field_validator("content")
    @classmethod
    def validar_conteudo_nao_vazio(cls, v: str) -> str:
        """Garante que arquivos em branco ou contendo apenas espaços sejam barrados."""
        if not v.strip():
            raise ValueError("O conteúdo do arquivo não pode estar vazio.")
        return v

    def estimar_tokens(self) -> int:
        """Calcula a estimativa aproximada de tokens (~4 caracteres por token)."""
        self.tokens = len(self.content) // 4
        return self.tokens


class ContextEngine(BaseModel):
    """
    Engine de Engenharia de Contexto.
    Varre o disco de forma determinística via pathlib e aplica orçamento máximo de tokens.
    """
    max_token_budget: int = Field(default=2000, description="Teto máximo de tokens permitido")
    
    # Diretorios e extensoes ignorados por padrao
    ignored_dirs: List[str] = Field(
        default_factory=lambda: [".git", ".venv", "venv", "__pycache__", ".pytest_cache", "build", "dist", "target"]
    )
    ignored_exts: List[str] = Field(
        default_factory=lambda: [".pyc", ".png", ".jpg", ".zip", ".xml", ".json", ".lock", ".exe", ".dll"]
    )
    
    files: List[CodeFile] = Field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        """Retorna o total acumulado de tokens dos arquivos selecionados."""
        return sum(f.tokens for f in self.files)

    def processar_arquivo(self, rel_path: Path, full_path: Path) -> bool:
        """Filtra, valida e adiciona um arquivo caso respeite o orçamento de tokens."""
        # 1. Ignora pastas reservadas
        if any(part in self.ignored_dirs for part in rel_path.parts):
            return False

        # 2. Ignora extensoes binarias ou nao relevantes
        if rel_path.suffix.lower() in self.ignored_exts:
            return False

        # 3. Leitura segura via pathlib
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return False

        if not content.strip():
            return False

        # 4. Instancia e valida o contrato via Pydantic
        try:
            code_file = CodeFile(
                file_path=str(rel_path).replace("\\", "/"),
                content=content,
                language=rel_path.suffix.lstrip(".") or "text"
            )
        except Exception as err:
            print(f"⚠️ [Validação Falhou] '{rel_path}': {err}")
            return False

        tokens = code_file.estimar_tokens()

        # 5. Dynamic Context Window: Bloqueia se estourar o limite de tokens
        if self.total_tokens + tokens > self.max_token_budget:
            print(f"⚠️ [Orçamento Excedido] '{rel_path}' ({tokens} tokens) excede o limite restante.")
            return False

        self.files.append(code_file)
        return True

    def varrer_projeto(self, pasta_raiz: str = ".") -> int:
        """Usa pathlib.Path para varrer recursivamente a pasta do projeto."""
        root = Path(pasta_raiz)
        arquivos_adicionados = 0

        for path in sorted(root.rglob("*")):
            if path.is_file() and path.name != Path(__file__).name:
                rel_path = path.relative_to(root)
                if self.processar_arquivo(rel_path, path):
                    arquivos_adicionados += 1

        return arquivos_adicionados

    def gerar_prompt(self, tarefa_usuario: str) -> str:
        """Monta o prompt final em Markdown estruturado para a LLM."""
        blocos = []
        for f in self.files:
            blocos.append(
                f"### Arquivo: `{f.file_path}` ({f.tokens} tokens)\n"
                f"```{f.language}\n{f.content.strip()}\n```"
            )

        contexto_formatado = "\n\n".join(blocos)

        return (
            f"## CONTEXTO DO PROJETO (Tokens: {self.total_tokens}/{self.max_token_budget})\n\n"
            f"{contexto_formatado}\n\n"
            f"## TAREFA PARA A IA\n"
            f"{tarefa_usuario}"
        )


if __name__ == "__main__":
    print("🚀 Running ContextEngine...\n")

    engine = ContextEngine(max_token_budget=1500)
    total_lidos = engine.varrer_projeto(pasta_raiz=".")

    print(f"\n✅ Concluído: {total_lidos} arquivo(s) lido(s) e validado(s) via Pydantic.")
    print(f"📊 Total de tokens consumidos: {engine.total_tokens} / {engine.max_token_budget}\n")

    prompt = engine.gerar_prompt(
        tarefa_usuario="Refatore o código para garantir tratamento explícito de exceções e princípios de Clean Code."
    )

    print("=== PROMPT ESTRUTURADO GERADO ===")
    print(prompt[:600] + "\n... [conteúdo truncado para exibição] ...")
