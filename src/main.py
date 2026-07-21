from machine import Pin, ADC
import time

# -----------------------------
# Configuração dos componentes
# -----------------------------

# Sensor LDR
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)

# Botão de reset
botao = Pin(27, Pin.IN, Pin.PULL_UP)


# -----------------------------
# Variáveis do sistema
# -----------------------------

contador = 0

sensor_bloqueado = False
inicio_bloqueio = 0
micro_parada_alertada = False

estado_botao_anterior = 1


# Limites
LUX_BAIXO = 100
TEMPO_MICRO_PARADA = 5000  # 5 segundos


# -----------------------------
# Funções auxiliares
# -----------------------------

def ler_lux():
    """
    Converte a leitura analógica do LDR
    para uma escala aproximada de lux.
    """
    valor = ldr.read()
    
    # Conversão simples para simulação
    lux = int((valor / 4095) * 1000)
    
    return lux


def reset_turno():
    global contador
    contador = 0
    
    print("Turno resetado com sucesso. Contadores zerados.")


# -----------------------------
# Inicialização
# -----------------------------

print("Contador de Producao Inicializado")


# -----------------------------
# Loop principal
# -----------------------------

while True:

    lux = ler_lux()
    
    print("Lux lido:", lux)

    # -------------------------
    # Detecção de peça
    # -------------------------

    if lux < LUX_BAIXO:

        if not sensor_bloqueado:
            sensor_bloqueado = True
            inicio_bloqueio = time.ticks_ms()

    else:

        # Retorno da luz normaliza
        if sensor_bloqueado:

            contador += 1

            print(f"Peca detectada! Total: {contador}")

            sensor_bloqueado = False
            micro_parada_alertada = False


    # -------------------------
    # Detecção de micro-parada
    # -------------------------

    if sensor_bloqueado:

        tempo = time.ticks_diff(
            time.ticks_ms(),
            inicio_bloqueio
        )

        if tempo >= TEMPO_MICRO_PARADA and not micro_parada_alertada:

            print("Alerta: Micro-parada detectada!")

            micro_parada_alertada = True


    # -------------------------
    # Botão de reset
    # -------------------------

    estado_botao = botao.value()

    # Detecta mudança pressionado -> solto
    if estado_botao_anterior == 0 and estado_botao == 1:

        reset_turno()

    estado_botao_anterior = estado_botao


    time.sleep_ms(50)