from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Date
from database import Base

class Jejum(Base):
    __tablename__ = "jejum"

    id = Column(Integer, primary_key=True, index=True)
    inicio = Column(DateTime, nullable=False)
    fim = Column(DateTime, nullable=True)
    duracao_horas = Column(Float, nullable=True)

class Treino(Base):
    __tablename__ = "treinos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, nullable=True)
    data_agendada = Column(Date, nullable=False)
    concluido = Column(Boolean, default=False)

class Alimentacao(Base):
    __tablename__ = "alimentacao"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, nullable=False)
    refeicao = Column(String, nullable=False)
    notas = Column(String, nullable=True)

# --- NOVA TABELA: UNIVERSIDADE ---
class TarefaUniversidade(Base):
    __tablename__ = "tarefas_universidade"

    id = Column(Integer, primary_key=True, index=True)
    cadeira = Column(String, nullable=False)             # Ex: Automação
    descricao = Column(String, nullable=False)           # Ex: Relatório Lab 1
    data_limite = Column(Date, nullable=False)           # Deadline
    concluido = Column(Boolean, default=False)           # Checkbox