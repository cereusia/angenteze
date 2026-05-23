# Agente Ze Character Assets

## Quem e o Agente Ze

Agente Ze e o personagem 3D do projeto open source da CereusIA. Ele representa um assistente global de macOS, operador de IA e coordenador de agentes, inspirado na Caatinga, no mandacaru/cacto Cereus e na ideia "Da Caatinga para o mundo".

As imagens em `references/` sao a fonte visual principal. Elas definem a silhueta, paleta oficial, logo, vistas tecnicas, icone de menu bar, interacao macOS e variacoes iniciais de especialistas.

## Como o Personagem Deve Ser Modelado

- Comecar por blockout simples em Blender.
- Travar a silhueta chibi antes dos detalhes.
- Manter cabeca grande, corpo compacto e visor frontal brilhante.
- Modelar o capuz/capacete como mandacaru amigavel.
- Usar espinhos arredondados, nunca pontiagudos agressivos.
- Separar olhos, boca, visor e simbolo para controle emissivo.
- Manter roupa de operador de campo, nao militar.

## Estrutura

```text
assets/character/agente-ze/
├── references/
├── blender/
├── textures/
├── rigs/
├── animations/
├── sprites/
├── icons/
├── exports/
├── README.md
└── agente-ze.character.json
```

## Referencias Principais

- `references/agente-ze-visual-board.png`
- `references/agente-ze-turnaround-poses.png`
- `references/agente-ze-open-source-board.png`
- `references/REFERENCE_IMAGES.md`

## Como Exportar do Blender

1. Salvar o arquivo fonte em `blender/`.
2. Validar nomes de meshes e bones com `blender/BLENDER_MODEL_BLUEPRINT.md`.
3. Aplicar transforms.
4. Exportar `.glb` para `exports/`.
5. Exportar renders/sprites para `sprites/` e `icons/` quando necessario.
6. Validar o GLB em um viewer externo.

## Como Integrar ao App

O app deve consumir:

- `agente-ze.character.json` para configuracao.
- GLB/GLTF exportado em `exports/`.
- sprites/icons como fallback.
- contrato em `docs/character/agente-ze-interaction-contract.md`.

O runtime pode ser SceneKit, RealityKit, WebView/Three.js ou outro motor 3D, desde que respeite `CharacterState`, `CharacterEmotion`, `CharacterAnimation`, `CharacterEvent` e `CharacterCommand`.

## Como Adicionar Novas Emocoes

1. Criar estado em `docs/character/agente-ze-emotion-system.md`.
2. Adicionar animacao em `docs/character/agente-ze-animation-map.md`, se necessario.
3. Adicionar entrada em `agente-ze.character.json`.
4. Criar controles/poses no Blender.
5. Validar fallback visual em sprite.

## Como Criar Variacoes para Agentes Especialistas

- Preservar silhueta-base.
- Alterar apenas cor secundaria, acessorio e ferramenta visual.
- Criar manifest JSON proprio.
- Documentar a variacao em `docs/character/agente-ze-specialists.md`.
- Nao adicionar armas, armaduras ou visual agressivo.
