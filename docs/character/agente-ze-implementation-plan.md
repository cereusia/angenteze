# Agente Ze - Implementation Plan

## Fase 1: Character Bible

- Consolidar especificacao visual.
- Selecionar referencias oficiais e internas.
- Definir paleta, materiais e silhueta.
- Validar com Zé, Tarcila, Lina e Eliane.

## Fase 2: Modelagem Base

- Criar blockout simples em Blender.
- Validar proporcao chibi.
- Travar silhueta frontal, lateral e tres-quartos.
- Separar casco, visor, corpo, roupa, botas, luvas e mochila.

## Fase 3: Rig

- Criar rig humanoide simples.
- Adicionar bones do capacete/capuz e mochila.
- Criar controles faciais para olhos, boca e glow.
- Testar poses principais.

## Fase 4: Animacoes

- Implementar loops base.
- Implementar one-shots de feedback.
- Garantir transicoes suaves.
- Exportar clipes nomeados.

## Fase 5: Export GLB

- Exportar GLB com materiais PBR e emissivos.
- Testar escala, orientacao e nomes.
- Validar no Blender e em viewer GLTF.
- Criar versao otimizada para runtime.

## Fase 6: Integracao no App macOS

- Escolher runtime: SceneKit, RealityKit, WebView/Three.js ou sprite fallback.
- Implementar loader do asset.
- Mapear eventos do app para `CharacterCommand`.
- Garantir fallback sem GPU/3D.

## Fase 7: Estados Guiados pelo Agente

- Conectar backend local aos eventos do personagem.
- Mapear prompt, pensamento, ferramenta, sucesso e erro.
- Adicionar memoria atualizada e offline.

## Fase 8: Otimizacao para Performance

- Reduzir contagem de vertices.
- Otimizar texturas.
- Testar FPS em Macs de entrada.
- Criar LOD ou sprite fallback.

## Fase 9: Agentes Especialistas

- Criar variacoes por acessorio e cor secundaria.
- Manter mesma silhueta-base.
- Versionar cada variacao com manifestos proprios.
- Validar consistencia visual do grupo.

## Marco de Aceite Inicial

- Character spec aprovada.
- Blueprint Blender pronto.
- JSON valido.
- Pastas de assets criadas.
- Contrato de integracao definido.
