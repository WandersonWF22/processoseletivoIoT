from machine import Pin, ADC
import time


# Sensor LDR no GPIO 34
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)


# Botão no GPIO 27
botao = Pin(27, Pin.IN, Pin.PULL_UP)


contador = 0

# Guarda se o sensor está bloqueado
sensor_bloqueado = False

# Controle da micro-parada
inicio_bloqueio = None
micro_parada_alertada = False

# Controle do botão
estado_botao_anterior = 1


# Ajustado para os valores reais do Wokwi
LIMITE_LUZ_BAIXA = 1000

TEMPO_MICRO_PARADA = 5


print("Contador de Producao Inicializado")


while True:

    valor_luz = ldr.read()

    print("Lux lido:", valor_luz)


    # Detecta objeto bloqueando o LDR
    bloqueado = valor_luz < LIMITE_LUZ_BAIXA


    # Entrada da peça
    if bloqueado and not sensor_bloqueado:

        sensor_bloqueado = True
        inicio_bloqueio = time.time()
        micro_parada_alertada = False


    # Saída da peça
    elif not bloqueado and sensor_bloqueado:

        contador += 1

        print("Peca detectada! Total:", contador)

        sensor_bloqueado = False
        inicio_bloqueio = None
        micro_parada_alertada = False



    # Detecção de micro-parada
    if sensor_bloqueado and inicio_bloqueio:

        tempo = time.time() - inicio_bloqueio

        if tempo >= TEMPO_MICRO_PARADA and not micro_parada_alertada:

            print("Alerta: Micro-parada detectada!")

            micro_parada_alertada = True



    # Reset manual
    estado_botao = botao.value()

    # Detecta pressionamento
    if estado_botao_anterior == 1 and estado_botao == 0:

        contador = 0

        print("Turno resetado com sucesso. Contadores zerados.")

        time.sleep(0.5)


    estado_botao_anterior = estado_botao


    time.sleep(0.1)