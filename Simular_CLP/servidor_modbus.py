# Funcionando como servidor (CLP Virtual)

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Cria um "banco de dados" vazio para o CLP simulado
# Isso simula os registradores físicos de um hardware real
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100), # Entradas Digitais
    co=ModbusSequentialDataBlock(0, [0]*100), # Bobinas (Saídas Digitais)
    hr=ModbusSequentialDataBlock(0, [0]*100), # Holding Registers (Onde gravamos números)
    ir=ModbusSequentialDataBlock(0, [0]*100)  # Input Registers
)
# Cria o contexto do servidor, associando o "banco de dados" ao servidor Modbus
context = ModbusServerContext(slaves=store, single=True)

print("Iniciando CLP Virtual na porta 502...")
# Inicia o servidor no endereço local. 
StartTcpServer(context=context, address=("127.0.0.1", 502))