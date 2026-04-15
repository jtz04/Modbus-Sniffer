# Modbus-Sniffer
Script para captura de trafego protocolo Modbus/TCP - (scapy e pymodbus == 3.5.2)

Funcionamento para simulação loopback (local) (atencao na linha 69 do script de captura argumento iface muda conforme Windows ou Linux):

Abrindo 3 terminais e rodando cada script em um terminal seguindo a ordem servidor → captura → gerar_trafego

O Script de captura vai gerar um data frame e importar em formato csv contendo registros dos pacotes capturados.
