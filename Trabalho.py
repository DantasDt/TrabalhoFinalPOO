from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///futebol.db")

Session = sessionmaker(bind=engine)
session = Session()

TimeCompeticao = Table("TimeCompeticao",
                       Base.metadata,
                       Column("TimeId", Integer, ForeignKey("times.id"), primary_key=True),
                       Column("CompeticaoId", Integer, ForeignKey("competicoes.id"), primary_key=True))

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    AnoFundacao = Column(Integer, nullable=False)

    jogadores = relationship("Jogador", back_populates="time")

    competicoes = relationship("Competicao",
                                secondary=TimeCompeticao,
                                back_populates="times")

class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    posicao = Column(String(50), nullable=False)
    idade = Column(Integer, nullable=False)

    time_id = Column(Integer, ForeignKey("times.id"), nullable=False)

    time = relationship("Time", back_populates="jogadores")

class Competicao(Base):
    __tablename__ = "competicoes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    temporada = Column(Integer, nullable=False)

    times = relationship("Time",
                        secondary=TimeCompeticao,
                        back_populates="competicoes")

Base.metadata.create_all(engine)


if not session.query(Time).first():

    Nasa = Time(nome="Nasa FC", AnoFundacao=2025)
    Vsfd = Time(nome="Vsfd FC", AnoFundacao=2024)
    Fc67 = Time(nome="67 Fc", AnoFundacao=2010)

    jogadores = [
        Jogador(nome="Jeipy", posicao="Goleiro", idade=16, time=Nasa),
        Jogador(nome="Dantas", posicao="Fixo", idade=16, time=Nasa),
        Jogador(nome="Diniz", posicao="Ala", idade=17, time=Nasa),
        Jogador(nome="Luiz", posicao="Ala", idade=17, time=Nasa),
        Jogador(nome="Patapim", posicao="Atacante", idade=16, time=Nasa),

        Jogador(nome="Faluba", posicao="Goleiro", idade=18, time=Vsfd),
        Jogador(nome="Nikao", posicao="Fixo", idade=18, time=Vsfd),
        Jogador(nome="Ivo", posicao="Ala", idade=18, time=Vsfd),
        Jogador(nome="Luiz Fome", posicao="Ala", idade=18, time=Vsfd),
        Jogador(nome="Iam", posicao="Atacante", idade=19, time=Vsfd),

        Jogador(nome="Caio Pinto", posicao="Goleiro", idade=67, time=Fc67),
        Jogador(nome="Alfredo dos Anzois", posicao="Fixo", idade=67, time=Fc67),
        Jogador(nome="Helio de Janeiro", posicao="Ala", idade=67, time=Fc67),
        Jogador(nome="Joao Goulart", posicao="Ala", idade=67, time=Fc67),
        Jogador(nome="Six Sevenaldo", posicao="Atacante", idade=67, time=Fc67)
    ]

    competicao1 = Competicao(nome="Copa Quadra Aberta", temporada=2026)
    competicao2 = Competicao(nome="Interclasse", temporada=2026)
    competicao3 = Competicao(nome="Copa Alterosa", temporada=2027)
    competicao4 = Competicao(nome="Taca das Favelas", temporada=2028)

    Nasa.competicoes.extend([competicao1, competicao2, competicao3, competicao4])

    Vsfd.competicoes.extend([competicao1, competicao2])

    Fc67.competicoes.extend([competicao4, competicao1])

    session.add_all([Nasa, Vsfd, Fc67, competicao1, competicao2, competicao3, competicao4])
    session.add_all(jogadores)

    session.commit()

time = session.query(Time).filter_by(nome="Nasa FC").first()

if time:
    print("Time:", time.nome)

    for jogador in time.jogadores:
        print(jogador.nome, "-", jogador.posicao)

time = session.query(Time).filter_by(nome="Vsfd FC").first()

if time:
    print("Time:", time.nome)

    for jogador in time.jogadores:
        print(jogador.nome, "-", jogador.posicao)

time = session.query(Time).filter_by(nome="67 Fc").first()

if time:
    print("Time:", time.nome)

    for jogador in time.jogadores:
        print(jogador.nome, "-", jogador.posicao)

competicao = session.query(Competicao).filter_by(nome="Copa Quadra Aberta").first()

if competicao:
    print("Competicao:", competicao.nome)

    for time in competicao.times:
        print(time.nome, "-", time.AnoFundacao)


session.close()