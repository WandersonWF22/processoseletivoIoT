from machine import Pin, ADC
import time


# =============================
# Configuração dos componentes
# =============================

# Sensor LDR no GPIO 34
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)


# Botão no GPIO 27
botao = Pin(27, Pin.IN, Pin.PULL_UP)


# =============================
# Variáveis do sistema
# =============================

contador = 0

# Estado do sensor
sensor_bloqueado = False

# Controle da micro-parada
inicio_bloqueio = None
micro_parada_alertada = False

# Controle do botão
estado_botao_anterior = 1


# =============================
# Parâmetros
# =============================

LIMITE_LUZ_BAIXA = 1500

TEMPO_MICRO_PARADA = 5000  # milissegundos


# =============================
# Inicialização
# =============================

print("Contador de Producao Inicializado")


# =============================
# Loop principal
# =============================

while True:

    valor_luz = ldr.read()

    bloqueado = valor_luz > LIMITE_LUZ_BAIXA


    # -------------------------
    # Entrada da peça
    # -------------------------

    if bloqueado and not sensor_bloqueado:

        sensor_bloqueado = True

        inicio_bloqueio = time.ticks_ms()

        micro_parada_alertada = False



    # -------------------------
    # Saída da peça
    # -------------------------

    elif not bloqueado and sensor_bloqueado:

        contador += 1

        print("Peca detectada! Total:", contador)


        sensor_bloqueado = False

        inicio_bloqueio = None

        micro_parada_alertada = False



    # -------------------------
    # Micro-parada
    # -------------------------

    if sensor_bloqueado and inicio_bloqueio is not None:

        tempo = time.ticks_diff(
            time.ticks_ms(),
            inicio_bloqueio
        )


        if tempo >= TEMPO_MICRO_PARADA and not micro_parada_alertada:

            print("Alerta: Micro-parada detectada!")

            micro_parada_alertada = True




    # -------------------------
    # Reset manual
    # -------------------------

    estado_botao = botao.value()


    # Detecta apenas o momento em que o botão é pressionado
    if estado_botao_anterior == 1 and estado_botao == 0:

        time.sleep_ms(20)  # debounce

        if botao.value() == 0:
            contador = 0
            print("Contadores resetados com sucesso.")


    estado_botao_anterior = estado_botao


    time.sleep_ms(10)