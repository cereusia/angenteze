# Agente Ze - Interaction Contract

## Objetivo

Definir uma interface abstrata para integrar o personagem a SwiftUI, SceneKit, RealityKit, WebView/Three.js ou outro runtime 3D.

Este contrato e conceitual e deve orientar implementacoes futuras sem prender o app a uma engine especifica.

## Tipos

```text
CharacterState
  id: String
  emotion: CharacterEmotion
  activeAnimation: CharacterAnimation?
  glowIntensity: Float
  statusText: String?
  isAttachedToMenuBar: Bool
  isFloatingPanelOpen: Bool

CharacterEmotion
  id: idle | listening | thinking | speaking | executing | success | warning | error | confused | celebrating | sleeping | updating | connecting | offline
  eyeExpression: String
  mouthExpression: String
  visorGlow: Float
  bodyPosture: String

CharacterAnimation
  id: String
  loop: Bool
  priority: Int
  durationMs: Int

CharacterEvent
  id: String
  payload: Object?
  timestamp: ISO-8601

CharacterCommand
  name: String
  args: Object
```

## Eventos

- `USER_OPENED_APP`
- `USER_CLICKED_MENU_BAR`
- `USER_DOUBLE_CLICKED_PET`
- `USER_STARTED_TYPING`
- `USER_SENT_PROMPT`
- `AGENT_STARTED_THINKING`
- `AGENT_STARTED_TOOL_USE`
- `AGENT_NEEDS_PERMISSION`
- `AGENT_COMPLETED_TASK`
- `AGENT_FAILED_TASK`
- `NETWORK_OFFLINE`
- `MEMORY_UPDATED`

## Comandos

```text
setEmotion(emotion: CharacterEmotion)
playAnimation(animation: CharacterAnimation)
setEyeExpression(expression: String)
setMouthExpression(expression: String)
setGlowIntensity(value: Float)
setStatusText(text: String?)
attachToMenuBar(enabled: Bool)
openFloatingPanel()
closeFloatingPanel()
followCursor(enabled: Bool)
reactToNotification(kind: String)
```

## Mapeamento Evento -> Comando

| Evento | Comandos sugeridos |
| --- | --- |
| `USER_OPENED_APP` | `setEmotion(connecting)`, `playAnimation(wake_up)` |
| `USER_CLICKED_MENU_BAR` | `openFloatingPanel()`, `setEmotion(idle)` |
| `USER_DOUBLE_CLICKED_PET` | `playAnimation(double_click_react)`, `setEmotion(listening)` |
| `USER_STARTED_TYPING` | `setEmotion(listening)`, `playAnimation(listen_pulse)` |
| `USER_SENT_PROMPT` | `setEmotion(thinking)`, `playAnimation(thinking_loop)` |
| `AGENT_STARTED_THINKING` | `setEmotion(thinking)` |
| `AGENT_STARTED_TOOL_USE` | `setEmotion(executing)`, `playAnimation(tool_execution)` |
| `AGENT_NEEDS_PERMISSION` | `setEmotion(warning)`, `playAnimation(warning_attention)` |
| `AGENT_COMPLETED_TASK` | `setEmotion(success)`, `playAnimation(success_bounce)` |
| `AGENT_FAILED_TASK` | `setEmotion(error)`, `playAnimation(error_shake)` |
| `NETWORK_OFFLINE` | `setEmotion(offline)`, `setGlowIntensity(0.15)` |
| `MEMORY_UPDATED` | `setEmotion(updating)`, `reactToNotification(memory)` |

## Requisitos de Integracao

- Todos os comandos devem ser idempotentes quando possivel.
- Eventos de erro nao podem travar o personagem em animacao infinita.
- Runtime deve aceitar fallback 2D/sprite quando 3D nao estiver disponivel.
- O contrato deve funcionar com assets GLB/GLTF e sprites renderizados.
- Estados devem ser serializaveis em JSON.
- Mudancas visuais devem ser desacopladas da logica do agente.
