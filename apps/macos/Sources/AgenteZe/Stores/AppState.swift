import Foundation

@MainActor
final class AppState: ObservableObject {
    @Published var prompt: String = ""
    @Published var responseText: String = "Pronto para receber uma intencao."
    @Published var memorySummary: String = "Memoria local ainda nao consultada."
    @Published var mcpEvents: [MCPEvent] = []
    @Published var isRunning: Bool = false
    @Published var lastError: String?
    @Published var confirmedToolNames: Set<String> = []
    @Published var deniedToolNames: Set<String> = []

    let backendClient: BackendClient

    var pendingConfirmationEvents: [MCPEvent] {
        mcpEvents.filter { event in
            event.isPendingConfirmation
                && !confirmedToolNames.contains(event.toolName)
                && !deniedToolNames.contains(event.toolName)
        }
    }

    init(backendClient: BackendClient) {
        self.backendClient = backendClient
    }

    func submitPrompt() {
        let text = prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty, !isRunning else {
            return
        }

        confirmedToolNames = []
        deniedToolNames = []
        sendPrompt(text, confirmedTools: [])
    }

    func confirmTool(_ event: MCPEvent) {
        var updated = confirmedToolNames
        updated.insert(event.toolName)
        confirmedToolNames = updated
        sendPrompt(prompt.trimmingCharacters(in: .whitespacesAndNewlines), confirmedTools: Array(updated))
    }

    func denyTool(_ event: MCPEvent) {
        var updated = deniedToolNames
        updated.insert(event.toolName)
        deniedToolNames = updated
    }

    private func sendPrompt(_ text: String, confirmedTools: [String]) {
        guard !text.isEmpty, !isRunning else {
            return
        }

        isRunning = true
        lastError = nil

        Task {
            do {
                let response = try await backendClient.send(
                    prompt: text,
                    confirmedTools: confirmedTools
                )
                responseText = response.message
                memorySummary = response.memorySummary
                mcpEvents = response.mcpEvents
                lastError = response.errors.first
            } catch {
                responseText = "Nao foi possivel consultar o backend local."
                lastError = error.localizedDescription
            }

            isRunning = false
        }
    }
}
