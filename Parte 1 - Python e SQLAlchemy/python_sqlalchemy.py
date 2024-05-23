from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    conta = relationship("Conta", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, name={self.name}, cpf={self.cpf}, endereço={self.endereco})"
    

class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(30), nullable=False)
    agencia = Column(Integer, nullable=False)
    num = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(Float, nullable=False)

    cliente = relationship("Cliente", back_populates="conta")


    def __repr__(self):
        return f"Conta(id={self.id}, saldo={self.saldo})"
    
# print(Cliente.__tablename__)
# print(Conta.__tablename__)

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)
# print(inspetor_engine.has_table("cliente"))
# print(inspetor_engine.get_table_names())
# print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    Marcos = Cliente(
        name="marcos",
        cpf="111.111.111-11",
        endereco="Jardim Europa, 344",
        conta=[
            Conta(
                tipo="corrente",
                agencia=1,
                num=11111,
                saldo=2500.
                )
            ]
    )

    Ian = Cliente(
        name="ian",
        cpf="222.222.222-22",
        endereco="Itu, 144",
        conta=[
            Conta(
                tipo="corrente",
                agencia=2,
                num=22222,
                saldo=3500.
                )
            ]
    )

    session.add_all([Marcos, Ian])

    session.commit()

print("Recuperando usuários a partir de condição de filtragem")

stmt = select(Cliente).where(Cliente.name.in_(["marcos", "ian"]))

for user in session.scalars(stmt):
    print(user)


print("\nRecuperando usuários a partir do id")

id = 2

stmt_saldo = select(Conta).where(Conta.user_id.in_([id]))

for saldos in session.scalars(stmt_saldo):
    print(saldos)

connection = engine.connect()


print("\nRecuperando dados após a união de três dados de diferentes classes")

stmt_join = select(
    Cliente.name, 
    Cliente.endereco, 
    Conta.saldo
    ).join_from(Conta, Cliente)

results = connection.execute(stmt_join).fetchall()

for result in results:
    print(result)


print("\nTotal de instâncias em Cliente")

stmt_count = select(func.count("*")).select_from(Cliente)

for result in session.scalars(stmt_count):
    print(result)

session.close()
