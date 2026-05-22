import SwiftUI

struct PromptView: View {
    @EnvironmentObject private var appState: AppState
    @FocusState private var promptFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            header
            promptEditor
            actions
            confirmationPanel
            responsePanel
        }
        .padding(18)
        .onAppear {
            promptFocused = true
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Agente Ze")
                .font(.title2.weight(.semibold))

            Text("Control + Option + Command + Space")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }

    private var promptEditor: some View {
        TextEditor(text: $appState.prompt)
            .font(.body.monospaced())
            .focused($promptFocused)
            .frame(minHeight: 110)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(.quaternary)
            )
    }

    private var actions: some View {
        HStack {
            Button {
                appState.submitPrompt()
            } label: {
                if appState.isRunning {
                    ProgressView()
                        .controlSize(.small)
                } else {
                    Text("Enviar")
                }
            }
            .keyboardShortcut(.return, modifiers: [.command])
            .disabled(appState.prompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || appState.isRunning)

            Button("Limpar") {
                appState.prompt = ""
                promptFocused = true
            }

            Spacer()
        }
    }

    private var responsePanel: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Resposta")
                .font(.headline)

            ScrollView {
                Text(appState.responseText)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .textSelection(.enabled)
            }
            .frame(minHeight: 120)

            Text(appState.memorySummary)
                .font(.caption)
                .foregroundStyle(.secondary)
                .lineLimit(2)

            if !appState.mcpEvents.isEmpty {
                Text("MCP: \(mcpSummary)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }

            if let lastError = appState.lastError {
                Text(lastError)
                    .font(.caption)
                    .foregroundStyle(.red)
                    .textSelection(.enabled)
            }
        }
        .padding(12)
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }

    @ViewBuilder
    private var confirmationPanel: some View {
        let pendingEvents = appState.pendingConfirmationEvents

        if !pendingEvents.isEmpty {
            VStack(alignment: .leading, spacing: 10) {
                HStack(spacing: 8) {
                    Image(systemName: "checkmark.shield")
                        .foregroundStyle(.orange)

                    Text("Confirmacao MCP")
                        .font(.headline)
                }

                ForEach(pendingEvents) { event in
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(event.toolName)
                                    .font(.subheadline.weight(.semibold))
                                    .lineLimit(1)

                                Text("\(event.risk.uppercased()) · \(event.reason)")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                                    .lineLimit(2)
                            }

                            Spacer()

                            Button {
                                appState.denyTool(event)
                            } label: {
                                Label("Negar", systemImage: "xmark.circle")
                            }

                            Button {
                                appState.confirmTool(event)
                            } label: {
                                Label("Confirmar", systemImage: "checkmark.circle")
                            }
                            .buttonStyle(.borderedProminent)
                        }
                    }
                    .padding(10)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(.quaternary)
                    )
                }
            }
            .padding(12)
            .background(.regularMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 8))
        }
    }

    private var mcpSummary: String {
        appState.mcpEvents
            .map { event in
                "\(event.toolName) [\(event.permission)]"
            }
            .joined(separator: ", ")
    }
}
