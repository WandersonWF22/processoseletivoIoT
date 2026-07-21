# Contador de Produção Não-Intrusivo

## Identificação do Candidato

**Nome completo:** Wanderson Wilkerson Felix da Silva

**GitHub:** https://github.com/WandersonWF22/processoseletivoIoT

## Visão Geral da Solução

O projeto desenvolvido consiste em um sistema embarcado para monitoramento de produção utilizando um microcontrolador ESP32, um sensor LDR e um botão de reset. O objetivo da solução é realizar a contagem automática de peças em uma esteira transportadora de forma não intrusiva, eliminando a necessidade de registros manuais e permitindo o acompanhamento da produção em tempo real.

O funcionamento do sistema baseia-se na leitura contínua da luminosidade pelo sensor LDR. Quando uma peça interrompe o feixe de luz, o firmware identifica o bloqueio e inicia o monitoramento do evento. A contagem é incrementada apenas quando a luminosidade retorna ao estado normal, garantindo que a peça tenha passado completamente pelo sensor e evitando contagens duplicadas. Além disso, caso o bloqueio permaneça por um período superior ao tempo configurado, o sistema interpreta a situação como uma micro-parada na linha de produção e informa o evento através da porta serial. O usuário também pode reiniciar o contador utilizando um botão físico dedicado ao reset do turno.

## Arquitetura do Sistema Embarcado

O firmware foi desenvolvido em MicroPython utilizando uma estrutura baseada em um único laço principal de execução (loop infinito), responsável por monitorar continuamente o estado do sensor LDR e do botão de reset.

A lógica do programa foi organizada por estados simples. Inicialmente o sistema permanece aguardando alterações na leitura do sensor. Quando ocorre uma mudança de luminosidade indicando a passagem de uma peça, o firmware registra o início do bloqueio. Após a liberação do feixe luminoso, o contador é incrementado e a quantidade total de peças produzidas é enviada para o monitor serial.

Paralelamente à rotina de contagem, o programa monitora o tempo em que o sensor permanece bloqueado utilizando funções de temporização baseadas em milissegundos. Caso esse intervalo ultrapasse o limite estabelecido de 5 segundos, uma mensagem de alerta de micro-parada é emitida.

A leitura do botão de reset também ocorre continuamente dentro do mesmo laço principal. Para evitar leituras incorretas causadas pelo efeito de bouncing mecânico, foi implementado um tratamento de debounce antes da confirmação do acionamento, garantindo maior confiabilidade durante a operação.

Toda a comunicação do sistema ocorre por meio da interface serial, utilizada tanto para informar a inicialização do firmware quanto para registrar eventos de produção, micro-paradas e reset dos contadores.

## Componentes Utilizados na Simulação

O projeto foi desenvolvido utilizando uma placa ESP32 DevKit C v4 como unidade de processamento principal. A detecção das peças foi realizada por meio de um sensor fotoresistor (LDR), configurado no ambiente Wokwi com o identificador `ldr1` e conectado à entrada analógica GPIO 34. O reset manual do turno foi implementado utilizando um botão de pressão (`btn1`), conectado ao GPIO 27 e configurado com resistor Pull-Up interno. Para acompanhamento do funcionamento do sistema foi utilizada a interface de comunicação serial UART integrada ao ESP32, responsável pela transmissão das mensagens de inicialização, contagem de peças, detecção de micro-paradas e reset dos contadores através do monitor serial.

## Decisões Técnicas Relevantes

Durante o desenvolvimento foi priorizada uma implementação simples, organizada e compatível com a validação automatizada do Wokwi CI. As leituras do sensor e do botão foram concentradas no laço principal do programa, evitando o uso de estruturas complexas desnecessárias.

A detecção de micro-paradas foi implementada utilizando as funções `time.ticks_ms()` e `time.ticks_diff()`, permitindo uma medição precisa do tempo sem bloquear a execução do firmware. Essa abordagem garante que o sistema continue respondendo aos demais eventos enquanto monitora o tempo de bloqueio do sensor.

Também foi implementado um mecanismo de debounce para o botão de reset, reduzindo falsos acionamentos provocados pelas oscilações mecânicas naturais durante o pressionamento e liberação do botão. Durante os testes automatizados observou-se que a confirmação do reset após a liberação do botão apresentou maior compatibilidade com o comportamento esperado pelo ambiente de validação.

As mensagens enviadas pela interface serial seguiram os padrões definidos no desafio e foram validadas conforme os cenários automatizados do Wokwi CI. Durante a implementação da rotina de reset manual, foi realizado um ajuste na mensagem de retorno para adequar a resposta do firmware ao comportamento esperado pelo teste automatizado, mantendo a funcionalidade de limpeza dos contadores.

## Resultados Obtidos

O sistema desenvolvido atendeu aos requisitos propostos para o desafio, realizando corretamente a detecção da passagem de peças, a contagem automática da produção, a identificação de micro-paradas e o reset manual do turno.

A solução foi validada utilizando os testes automatizados disponibilizados pelo Wokwi CI, contemplando os três cenários exigidos: contagem normal de peças, detecção de micro-parada e reset manual. Todos os cenários foram executados com sucesso, confirmando o funcionamento correto do firmware desenvolvido.

## Comentários Adicionais

Durante o desenvolvimento, a principal dificuldade encontrada esteve relacionada à compatibilidade entre a lógica do firmware e o comportamento esperado pelos testes automatizados do Wokwi CI. Pequenas diferenças na forma de detectar o acionamento do botão, especialmente entre o momento do pressionamento e da liberação, influenciavam diretamente o resultado dos testes.

A experiência proporcionou uma compreensão mais aprofundada sobre sistemas embarcados, temporização não bloqueante, tratamento de debounce e integração contínua utilizando GitHub Actions. Também evidenciou a importância da padronização das mensagens enviadas pela interface serial e da sincronização correta entre o firmware e os cenários automatizados de validação.
