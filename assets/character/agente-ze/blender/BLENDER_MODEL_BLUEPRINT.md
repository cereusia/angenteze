# Agente Ze - Blender Model Blueprint

## Objetivo

Orientar a modelagem, rig, materiais e exportacao do personagem 3D Agente Ze.

Referencias obrigatorias:

- `../references/agente-ze-visual-board.png`
- `../references/agente-ze-turnaround-poses.png`
- `../references/agente-ze-open-source-board.png`

## Lista de Objetos do Modelo

- `AZE_Body`
- `AZE_HeadShell`
- `AZE_FaceScreen`
- `AZE_Eye_L`
- `AZE_Eye_R`
- `AZE_Mouth`
- `AZE_CactusHelmet`
- `AZE_FieldHatBrim`
- `AZE_CactusGrooves`
- `AZE_CactusSpines`
- `AZE_Scarf`
- `AZE_Backpack`
- `AZE_Boot_L`
- `AZE_Boot_R`
- `AZE_Glove_L`
- `AZE_Glove_R`
- `AZE_ChestSymbol`
- `AZE_UtilityBelt`
- `AZE_Pocket_L`
- `AZE_Pocket_R`

## Nomes Padronizados dos Meshes

| Mesh | Funcao |
| --- | --- |
| `AZE_Body_GEO` | corpo compacto |
| `AZE_HeadShell_GEO` | casco/cabeca principal |
| `AZE_FaceScreen_GEO` | visor frontal |
| `AZE_Eye_L_GEO` | olho esquerdo emissivo |
| `AZE_Eye_R_GEO` | olho direito emissivo |
| `AZE_Mouth_GEO` | boca digital |
| `AZE_CactusHelmet_GEO` | capuz/capacete mandacaru |
| `AZE_FieldHatBrim_GEO` | aba integrada de explorador |
| `AZE_CactusGrooves_GEO` | gomos verticais |
| `AZE_CactusSpines_GEO` | espinhos arredondados |
| `AZE_Scarf_GEO` | lenco |
| `AZE_Backpack_GEO` | mochila |
| `AZE_Boot_L_GEO` | bota esquerda |
| `AZE_Boot_R_GEO` | bota direita |
| `AZE_Glove_L_GEO` | luva esquerda |
| `AZE_Glove_R_GEO` | luva direita |
| `AZE_ChestSymbol_GEO` | simbolo emissivo |
| `AZE_UtilityBelt_GEO` | cinto utilitario |

## Hierarquia do Rig

```text
AZE_Rig
├── AZE_ROOT
│   ├── AZE_Hips
│   │   ├── AZE_Spine
│   │   │   ├── AZE_Chest
│   │   │   │   ├── AZE_Neck
│   │   │   │   │   └── AZE_Head
│   │   │   │   │       ├── AZE_EyeTarget_L
│   │   │   │   │       ├── AZE_EyeTarget_R
│   │   │   │   │       ├── AZE_Mouth_CTRL
│   │   │   │   │       └── AZE_CactusHelmet_CTRL
│   │   │   │   ├── AZE_Shoulder_L
│   │   │   │   │   └── AZE_Arm_L -> AZE_Forearm_L -> AZE_Hand_L
│   │   │   │   └── AZE_Shoulder_R
│   │   │   │       └── AZE_Arm_R -> AZE_Forearm_R -> AZE_Hand_R
│   │   │   └── AZE_Backpack_CTRL
│   │   ├── AZE_Leg_L -> AZE_Shin_L -> AZE_Foot_L
│   │   └── AZE_Leg_R -> AZE_Shin_R -> AZE_Foot_R
```

## Materiais

- `MAT_AZE_CactusShell`
- `MAT_AZE_CactusGrooves`
- `MAT_AZE_SoftSpines`
- `MAT_AZE_FaceGlass`
- `MAT_AZE_EyeGlow`
- `MAT_AZE_MouthGlow`
- `MAT_AZE_FieldCloth`
- `MAT_AZE_FieldHat`
- `MAT_AZE_Scarf`
- `MAT_AZE_LeatherUtility`
- `MAT_AZE_TechMetal`
- `MAT_AZE_ChestSymbolGlow`

## Bones Necessarios

- Root: `AZE_ROOT`
- Corpo: `AZE_Hips`, `AZE_Spine`, `AZE_Chest`, `AZE_Neck`, `AZE_Head`
- Bracos: `AZE_Shoulder_L/R`, `AZE_Arm_L/R`, `AZE_Forearm_L/R`, `AZE_Hand_L/R`
- Pernas: `AZE_Leg_L/R`, `AZE_Shin_L/R`, `AZE_Foot_L/R`
- Acessorios: `AZE_Backpack_CTRL`, `AZE_Scarf_CTRL`, `AZE_CactusHelmet_CTRL`
- Aba/chapeu: `AZE_FieldHatBrim_CTRL`
- Face: `AZE_EyeTarget_L/R`, `AZE_EyeScale_L/R`, `AZE_Mouth_CTRL`, `AZE_VisorGlow_CTRL`

## Controles Faciais

- `AZE_EyeShape_CTRL`: circulo, arco feliz, semicerrado, fechado, assimetrico.
- `AZE_EyeGlow_CTRL`: intensidade emissiva 0.0 a 1.0.
- `AZE_MouthShape_CTRL`: neutro, sorriso, fala, erro, confuso.
- `AZE_VisorGlow_CTRL`: intensidade e cor do visor.
- `AZE_ChestSymbolGlow_CTRL`: pulso do simbolo.

## Controle de Olhos

- Olhos devem ser meshes ou curvas emissivas separadas.
- Suportar escala X/Y para piscar e expressar.
- Suportar target de olhar para cursor.
- Manter brilho legivel em tamanho pequeno.

## Controle de Boca

- Boca digital deve ser simples e emissiva.
- Para fala, usar barras verticais ou waveform curta.
- Nao usar dentes ou expressao agressiva.
- Boca deve ficar dentro do visor.

## Estados Emissivos

| Estado | Olhos | Visor | Simbolo |
| --- | --- | --- | --- |
| `idle` | ciano 0.45 | preto brilho baixo | verde 0.25 |
| `listening` | ciano 0.75 | pulso ciano | verde 0.35 |
| `thinking` | ciano/verde 0.60 | pulso lento | verde 0.45 |
| `executing` | verde/ciano 0.80 | scan | verde 0.70 |
| `success` | verde 0.90 | verde suave | verde 1.00 |
| `warning` | amarelo 0.75 | amarelo baixo | amarelo 0.60 |
| `error` | vermelho 0.55 | vermelho baixo | vermelho 0.35 |
| `offline` | azul cinza 0.20 | quase apagado | 0.10 |

## Requisitos para Exportacao GLB/GLTF

- Formato primario: `.glb`.
- Formato editavel: `.blend`.
- Escala: 1 unidade Blender = 1 metro conceitual.
- Altura final: cerca de 3.0 unidades.
- Origem do modelo: centro no chao entre os pes.
- Eixo frontal: `-Y` ou convencao documentada no export.
- Aplicar transforms antes do export.
- Nomear clipes de animacao conforme `docs/character/agente-ze-animation-map.md`.
- Incluir materiais PBR e emissivos.
- Texturas maximas iniciais: 1024px para runtime, 2048px para source.
- Evitar dependencias externas nao versionadas.
- Criar LOD ou sprite fallback em fase posterior.

## Requisitos para Uso em App macOS

- Asset deve carregar em SceneKit, RealityKit ou WebView/Three.js.
- Export deve preservar nomes de meshes, bones e animacoes.
- Estados devem ser controlaveis por JSON/contrato abstrato.
- Deve existir fallback 2D em `sprites/` ou `icons/`.
- O personagem deve funcionar em tamanho pequeno de menu bar e painel flutuante.
- Materiais emissivos devem ter intensidades moderadas para modo claro/escuro.

## Checklist de Fidelidade contra Referencias

- Frente, tres-quartos, lateral direita, traseira, topo e base devem bater com o board tecnico.
- Versao frontal deve preservar olhos circulares, visor preto e sorriso pequeno.
- Vista traseira deve mostrar mochila tecnica, rolos laterais e volume do capacete.
- Poses deitado/descanso do turnaround devem ser possiveis pelo rig.
- Icone de menu bar deve funcionar com apenas cabeca, visor e capuz.
- Estados Normal, Ativo, Falando e Pensando devem ter leitura clara em tamanho pequeno.
