# Agente Ze - Animation Map

## Objetivo

Mapear animacoes reutilizaveis do personagem para estados e eventos do app.

| Animacao | Duracao sugerida | Tipo | Intensidade | Propriedades animadas | Prioridade | Gatilho no aplicativo |
| --- | --- | --- | --- | --- | --- | --- |
| `idle_breathing` | 2.8s | loop | baixa | escala torso, ombros, brilho leve | baixa | app aberto sem atividade |
| `blink` | 0.12s | one-shot/aleatorio | baixa | escala Y dos olhos, emissivo | baixa | a cada 3 a 6s em estados ativos |
| `look_at_cursor` | continuo | loop procedural | baixa/media | rotacao olhos, leve giro cabeca | media | cursor proximo ao personagem |
| `listen_pulse` | 1.2s | loop | media | emissivo olhos/visor, leve inclinacao | media | usuario digitando |
| `thinking_loop` | 1.8s | loop | media | olhos, cabeca, mao, simbolo peito | media | agente pensando |
| `typing_response` | 0.8s | loop | media | boca digital, olhos, glow | media | streaming/exibicao de resposta |
| `tool_execution` | 1.4s | loop | media/alta | visor scan, mochila, simbolo, postura | alta | ferramenta MCP/local em uso |
| `success_bounce` | 0.7s | one-shot | media | root, bracos, olhos, glow verde | alta | tarefa concluida |
| `error_shake` | 0.45s | one-shot | media | root X, olhos, visor vermelho suave | alta | erro de tarefa |
| `warning_attention` | 0.65s | one-shot | media | cabeca, olhos, glow amarelo | alta | permissao/riscos |
| `sleep_mode` | 1.2s | one-shot + loop final | baixa | olhos fecham, emissivo reduz | media | inatividade longa |
| `wake_up` | 0.9s | one-shot | media | olhos abrem, postura sobe, glow volta | alta | usuario interage depois de inatividade |
| `open_panel` | 0.35s | one-shot | media | escala root, opacidade, postura | alta | painel flutuante abre |
| `close_panel` | 0.28s | one-shot | baixa/media | escala root, opacidade, olhos | alta | painel flutuante fecha |
| `double_click_react` | 0.55s | one-shot | media | cabeca, olhos, bounce pequeno | media | duplo clique no personagem |
| `drag_follow` | continuo | procedural | baixa/media | root, olhos, inercia corpo | media | usuario arrasta personagem |
| `notification_ping` | 0.8s | one-shot | media | simbolo peito, olhos, bounce leve | alta | notificacao do agente |

## Prioridades

1. `error_shake`, `warning_attention`, `tool_execution`.
2. `success_bounce`, `notification_ping`, `wake_up`.
3. `thinking_loop`, `typing_response`, `listen_pulse`.
4. `look_at_cursor`, `idle_breathing`, `blink`.

Animacoes de prioridade alta podem interromper loops de baixa prioridade. Ao terminar, devem retornar ao estado emocional atual.
