# Agente Ze - Emotion System

## Objetivo

Definir estados emocionais claros para controlar expressao, postura, movimento e feedback do personagem no app macOS.

## Estados

| Estado | Olhos | Boca | Brilho do visor | Postura corporal | Movimento | Som opcional | Quando ativar no app |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `idle` | circulares, ciano suave | linha pequena neutra | baixo/medio | relaxada | respiracao leve | hum baixo | app aberto sem tarefa |
| `listening` | maiores, ciano intenso | pequena curva neutra | pulso medio | inclinado para frente | pulso no visor | bip suave | usuario começou a digitar ou abriu prompt |
| `thinking` | semicerrados, alternando ciano/verde | pontos ou linha curta | pulso lento | mao no queixo/lateral | leve balanco | tick suave | agente esta planejando resposta |
| `speaking` | abertos, estaveis | barras digitais animadas | medio | frontal, confiante | boca sincronizada | blip curto | resposta sendo exibida |
| `executing` | focados, ciano/verde | linha firme | varredura no visor | corpo firme | micro inclinacoes | sequencia leve | ferramenta local em uso |
| `success` | olhos felizes/arcos | sorriso pequeno | verde claro alto | peito aberto | bounce curto | sinal positivo | tarefa concluida |
| `warning` | olhos abertos, contorno amarelo | linha pequena | amarelo medio | postura atenta | inclinacao curta | alerta suave | permissao ou risco exige atencao |
| `error` | olhos reduzidos, vermelho suave | curva baixa pequena | vermelho baixo/medio | ombros baixos | shake curto | tom grave curto | tarefa falhou |
| `confused` | assimetricos | boca inclinada | ciano irregular | cabeca inclinada | tilt lateral | bip interrogativo | input ambiguo ou falta contexto |
| `celebrating` | olhos felizes, verde/ciano | sorriso amplo | verde alto | bracos abertos | salto curto | fanfarra curta | marco importante concluido |
| `sleeping` | fechados | linha pequena | muito baixo | relaxada | respiracao lenta | nenhum ou hum | inatividade longa |
| `updating` | circulares com scan | linha neutra | verde pulsante no peito | mochila destacada | luz em fluxo | tick leve | memoria/config atualizada |
| `connecting` | ciano alternado | linha neutra | pulso ciano | alerta leve | antena/visor pulsando | bip conectado | inicializacao ou conexao backend |
| `offline` | cinza/azul baixo | linha neutra | minimo | ombros baixos | quase parado | nenhum | backend/rede indisponivel |

## Regras

- Estados nao podem mudar a silhueta-base.
- Transicoes devem durar entre 0.12s e 0.45s.
- `warning` e `error` devem ser claros, mas nao assustadores.
- `executing` nunca deve sugerir acao perigosa sem permissao.
- `sleeping` deve acordar com `wake_up` antes de qualquer estado ativo.
- Brilho emissivo deve respeitar modo claro/escuro do app.
