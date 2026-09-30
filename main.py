from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date
from pydantic import BaseModel

import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestor Diário API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TreinoCriar(BaseModel):
    titulo: str
    descricao: str | None = None
    data_agendada: date

class AlimentacaoCriar(BaseModel):
    refeicao: str
    notas: str | None = None
    data_hora: datetime | None = None

class TarefaCriar(BaseModel):
    cadeira: str
    descricao: str
    data_limite: date

# --- JEJUM ---
@app.post("/api/fitness/jejum/iniciar")
def iniciar_jejum(db: Session = Depends(get_db)):
    agora = datetime.now()
    jejum_ativo = db.query(models.Jejum).filter(models.Jejum.fim == None).first()
    if jejum_ativo:
        raise HTTPException(status_code=400, detail="Jejum a decorrer.")
    
    novo_jejum = models.Jejum(inicio=agora)
    db.add(novo_jejum)
    db.commit()            
    db.refresh(novo_jejum) 
    return {"mensagem": "Iniciado!", "hora_inicio": novo_jejum.inicio}

@app.post("/api/fitness/jejum/terminar")
def terminar_jejum(db: Session = Depends(get_db)):
    agora = datetime.now()
    jejum_ativo = db.query(models.Jejum).filter(models.Jejum.fim == None).order_by(models.Jejum.inicio.desc()).first()
    if not jejum_ativo:
        raise HTTPException(status_code=400, detail="Nenhum jejum ativo.")
    
    jejum_ativo.fim = agora
    horas = (jejum_ativo.fim - jejum_ativo.inicio).total_seconds() / 3600
    jejum_ativo.duracao_horas = round(horas, 2)
    db.commit()
    return {"mensagem": "Terminado!"}

@app.get("/api/fitness/jejum/historico")
def historico_jejuns(db: Session = Depends(get_db)):
    return db.query(models.Jejum).order_by(models.Jejum.inicio.desc()).all()

# --- TREINOS ---
@app.post("/api/fitness/treinos")
def criar_treino(treino: TreinoCriar, db: Session = Depends(get_db)):
    novo = models.Treino(titulo=treino.titulo, descricao=treino.descricao, data_agendada=treino.data_agendada)
    db.add(novo)
    db.commit()
    return {"mensagem": "Sucesso!"}

@app.get("/api/fitness/treinos")
def listar_treinos(db: Session = Depends(get_db)):
    return db.query(models.Treino).order_by(models.Treino.data_agendada).all()

@app.put("/api/fitness/treinos/{treino_id}/concluir")
def concluir_treino(treino_id: int, db: Session = Depends(get_db)):
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    treino.concluido = not treino.concluido
    db.commit()
    return {"mensagem": "Atualizado!"}

@app.delete("/api/fitness/treinos/{treino_id}")
def apagar_treino(treino_id: int, db: Session = Depends(get_db)):
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    db.delete(treino)
    db.commit()
    return {"mensagem": "Treino apagado!"}

# --- ALIMENTAÇÃO ---
@app.post("/api/fitness/alimentacao")
def registar_refeicao(dados: AlimentacaoCriar, db: Session = Depends(get_db)):
    hora = dados.data_hora if dados.data_hora else datetime.now()
    nova = models.Alimentacao(data_hora=hora, refeicao=dados.refeicao, notas=dados.notas)
    db.add(nova)
    db.commit()
    return {"mensagem": "Registado!"}

@app.get("/api/fitness/alimentacao")
def listar_refeicoes(db: Session = Depends(get_db)):
    return db.query(models.Alimentacao).order_by(models.Alimentacao.data_hora.desc()).all()

# --- UNIVERSIDADE ---
@app.post("/api/universidade/tarefas")
def criar_tarefa(tarefa: TarefaCriar, db: Session = Depends(get_db)):
    nova_tarefa = models.TarefaUniversidade(
        cadeira=tarefa.cadeira,
        descricao=tarefa.descricao,
        data_limite=tarefa.data_limite,
        concluido=False
    )
    db.add(nova_tarefa)
    db.commit()
    return {"mensagem": "Tarefa adicionada!"}

@app.get("/api/universidade/tarefas")
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.TarefaUniversidade).order_by(models.TarefaUniversidade.data_limite).all()

@app.put("/api/universidade/tarefas/{tarefa_id}/concluir")
def concluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaUniversidade).filter(models.TarefaUniversidade.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.concluido = not tarefa.concluido
    db.commit()
    return {"mensagem": "Estado atualizado!"}

@app.delete("/api/universidade/tarefas/{tarefa_id}")
def apagar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaUniversidade).filter(models.TarefaUniversidade.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa apagada!"}