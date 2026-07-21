from machine import Pin, ADC
import time


# Sensor LDR no GPIO 34
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)


# Botão no GPIO 27
botao = Pin(27, Pin.IN, Pin.PULL_UP)


contador = 0

# Guarda se uma peça já foi detectada
objeto_detectado = False

# Controle da parada
inicio_parada = None


print("Contador de Producao Inicializado")


while True:

    # Leitura do sensor
    valor_luz = ldr.read()

    print("Lux lido:", valor_luz)


    # Quando a luz cai, consideramos que uma peça bloqueou o sensor
    # O valor pode variar no Wokwi, por isso usamos 400 como referência
    bloqueado = valor_luz < 400


    # Detecta uma nova peça
    if bloqueado and not objeto_detectado:

        contador += 1

        print("Peca detectada! Total:", contador)

        objeto_detectado = True


    # Quando a peça sai
    if not bloqueado:

        objeto_detectado = False

        inicio_parada = None


    # Detecta micro-parada
    if bloqueado:

        if inicio_parada is None:
            inicio_parada = time.time()


        elif time.time() - inicio_parada >= 5:

            print("Alerta: Micro-parada detectada!")

            # evita imprimir infinitamente
            inicio_parada = time.time()



    # Reset manual
    if botao.value() == 0:

        contador = 0

        print("Turno resetado com sucesso. Contadores zerados.")

        time.sleep(1)


    time.sleep(0.1)