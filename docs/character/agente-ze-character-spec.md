# Agente Ze - Character Spec

## 1. Descricao Geral

Agente Ze e o mascote 3D oficial do projeto open source da CereusIA. Ele representa um operador de IA pequeno, resiliente e prestativo, com linguagem visual inspirada na Caatinga, no mandacaru/cacto Cereus e no sertao brasileiro.

O personagem deve parecer premium, moderno e amigavel. A leitura principal deve ser: um pequeno agente tecnico de campo, com visor digital expressivo, corpo compacto, equipamento utilitario e capuz/capacete botanico inspirado no mandacaru.

Ele nao deve parecer militar, agressivo, infantil demais, robotico demais ou caricatural sem acabamento.

Referencias visuais oficiais:

- `assets/character/agente-ze/references/agente-ze-visual-board.png`
- `assets/character/agente-ze/references/agente-ze-turnaround-poses.png`
- `assets/character/agente-ze/references/agente-ze-open-source-board.png`

Essas imagens fixam logo, paleta, silhueta, vistas tecnicas, icone de menu bar, interacao macOS, evolucao e variacoes iniciais.

## 2. Proporcoes

- Estilo: mascote 3D chibi premium.
- Altura total: 3.0 unidades Blender.
- Cabeca/capacete: 45% a 50% da altura total.
- Corpo: 35% a 40% da altura total.
- Pernas/botas: 15% a 20% da altura total.
- Silhueta: compacta, arredondada e facilmente reconhecivel em tamanho pequeno.
- Face/visor: ocupa 65% a 75% da frente da cabeca.
- Olhos: grandes, circulares, com brilho emissivo.
- Maos e pes: pequenos, arredondados, sem agressividade.
- Mochila: visivel em perfil e tres-quartos, mas sem competir com a silhueta principal.

## 3. Paleta de Cores

| Uso | HEX | Observacao |
| --- | --- | --- |
| Verde CereusIA oficial | `#22C55E` | logo, simbolo, brilho principal |
| Verde mandacaru principal | `#2F7D46` | capacete/capuz |
| Verde profundo | `#174A2A` | sombras do casco e detalhes |
| Verde claro emissivo | `#65F2A3` | simbolo, highlights, feedback positivo |
| Ciano digital | `#47D7FF` | olhos e estados ativos |
| Azul tecnico oficial | `#2563EB` | detalhes digitais e especialistas |
| Preto oficial | `#0B0F14` | fundo, visor e UI escura |
| Preto visor | `#090D10` | face frontal brilhante |
| Grafite visor | `#1A2228` | reflexos e bordas |
| Areia oficial | `#F2E8CF` | tipografia clara e tecido claro |
| Areia roupa | `#C8A66A` | jaqueta e tecido principal |
| Bege claro | `#E6D0A2` | areas elevadas da roupa |
| Marrom oficial | `#8B5E34` | couro, mochila, botas |
| Terra marrom | `#7A4E2D` | cinto, botas, luvas |
| Lenço terroso escuro | `#5A2E24` | pescoco |
| Metal escuro | `#3A3F42` | fivelas e componentes tecnicos |
| Alerta amarelo | `#FFD166` | warning |
| Erro vermelho suave | `#FF5A5F` | error, sem agressividade |
| Offline azul cinza | `#7B8A90` | estados desconectados |

## 4. Materiais Sugeridos para Blender

- `MAT_AZE_CactusShell`: verde mandacaru, roughness medio, subsurface muito leve.
- `MAT_AZE_CactusGrooves`: verde profundo em sulcos verticais.
- `MAT_AZE_SoftSpines`: espinhos arredondados, verde claro fosco.
- `MAT_AZE_FaceGlass`: preto brilhante, roughness baixo, clearcoat alto.
- `MAT_AZE_EyeGlow`: emissivo ciano/verde, intensidade animavel.
- `MAT_AZE_MouthGlow`: emissivo suave, intensidade menor que os olhos.
- `MAT_AZE_FieldCloth`: tecido areia/bege, roughness alto.
- `MAT_AZE_Scarf`: tecido terroso escuro, leve ondulacao normal map.
- `MAT_AZE_LeatherUtility`: marrom, roughness medio, bordas suaves.
- `MAT_AZE_TechMetal`: metal escuro nao polido.
- `MAT_AZE_ChestSymbolGlow`: emissivo verde, pulsacao leve.

## 5. Pecas do Modelo

- Corpo compacto.
- Cabeca/casco externo.
- Visor frontal preto.
- Olho esquerdo.
- Olho direito.
- Boca digital.
- Capacete/capuz de mandacaru.
- Gomos verticais do cacto.
- Espinhos arredondados.
- Roupa de operador de campo.
- Lenco no pescoco.
- Mochila tecnica.
- Cinto utilitario.
- Bolsos pequenos.
- Luvas.
- Botas.
- Simbolo CereusIA/Ze no peito.

## 6. Acessorios

- Mochila tecnica: representa memoria, ferramentas, contexto e conhecimento.
- Cinto utilitario: pequenos modulos nao agressivos.
- Bolsos laterais: leitura de operador de campo.
- Lenco terroso: ponte visual com o sertao.
- Simbolo no peito: pequeno, emissivo, legivel em close.
- Porta-ferramenta visual: sem armas, sem itens militares.
- Aba/chapeu de explorador integrada ao capacete, conforme turnaround.
- Rolos laterais/mochila compacta visiveis em perfil e costas.

## 7. Expressoes Faciais

As expressoes devem ser feitas principalmente por olhos, boca digital e brilho do visor.

- Neutro: olhos circulares abertos, boca pequena horizontal.
- Ouvindo: olhos maiores, brilho ciano pulsante.
- Pensando: olhos levemente semicerrados, boca pontilhada ou pequena curva.
- Falando: boca com barras digitais animadas.
- Executando: olhos focados, visor com varredura sutil.
- Sucesso: olhos felizes em arco/circulo, boca sorriso pequeno.
- Alerta: olhos abertos, amarelo suave no contorno.
- Erro: olhos menores, brilho vermelho suave, sem agressividade.
- Confuso: olhos assimetricos, boca pequena inclinada.
- Dormindo: olhos fechados, visor baixo.

## 8. Estados Emocionais

Estados base:

- `idle`
- `listening`
- `thinking`
- `speaking`
- `executing`
- `success`
- `warning`
- `error`
- `confused`
- `celebrating`
- `sleeping`
- `updating`
- `connecting`
- `offline`

Cada estado deve mapear olhos, boca, brilho, postura e animacao conforme `docs/character/agente-ze-emotion-system.md`.

## 9. Poses

- Pose neutra: pe levemente aberto, maos relaxadas.
- Pose de escuta: corpo inclinado 3 a 5 graus para frente.
- Pose de pensamento: uma mao no queixo ou lateral do visor.
- Pose de execucao: corpo firme, visor ativo, mochila levemente destacada.
- Pose de sucesso: pequeno salto ou bracos abertos.
- Pose de alerta: corpo rigido, olhos focados.
- Pose offline: ombros baixos, visor com brilho reduzido.

## 10. Animacoes

Animacoes obrigatorias:

- `idle_breathing`
- `blink`
- `look_at_cursor`
- `listen_pulse`
- `thinking_loop`
- `typing_response`
- `tool_execution`
- `success_bounce`
- `error_shake`
- `warning_attention`
- `sleep_mode`
- `wake_up`
- `open_panel`
- `close_panel`
- `double_click_react`
- `drag_follow`
- `notification_ping`

Detalhes em `docs/character/agente-ze-animation-map.md`.

## 11. Regras de Fidelidade Visual

- Manter silhueta pequena, arredondada e chibi.
- Preservar a leitura do capuz/capacete de mandacaru.
- O visor frontal deve ser preto, brilhante e integrado a cabeca.
- Os olhos devem ser grandes, luminosos e amigaveis.
- A roupa deve parecer de campo/operacao, nao militar.
- Nao usar armas, armaduras pesadas, caveiras, agressividade ou estetica de combate.
- O simbolo do peito deve ser pequeno, emissivo e legivel.
- A mochila deve sugerir conhecimento e ferramentas, nao combate.
- O personagem deve continuar reconhecivel em icone pequeno.
- Variacoes futuras devem preservar a silhueta-base.

## 12. Usos no App macOS

- Menu bar: icone/sprite reduzido ou cabeca simplificada.
- Floating panel: personagem em 3D ou sprite renderizado em estado `idle`.
- Prompt global: muda para `listening`, `thinking`, `speaking` e `executing`.
- Permissoes: estado `warning` com postura atenciosa.
- Falhas: estado `error` sem dramatizacao.
- Tarefa concluida: `success` ou `celebrating`.
- Offline: visor reduzido e movimento minimo.
- Atualizacao de memoria: `updating` com brilho no simbolo/ mochila.
- Futuro runtime 3D: SceneKit, RealityKit, WebView com Three.js ou outro motor 3D.

## 13. Identidade Grafica Associada

- Logo: simbolo hexagonal verde com `Z` central e brotos superiores.
- Tagline primaria: "DA CAATINGA PARA O MUNDO."
- Frase secundaria: "FEITO NO CARIRI. PARA O MUNDO."
- Tipografia de referencia: Inter.
- Menu bar: versao de cabeca em fundo escuro arredondado, mantendo olhos e capuz.
