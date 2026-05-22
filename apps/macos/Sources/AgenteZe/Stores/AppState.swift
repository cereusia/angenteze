import Foundation

@MainActor
final class AppState: ObservableObject {
    @Published var prompt: String = ""
    @Published var responseText: String = "Pronto para receber uma intencao."
    @Published var memorySummary: String = "Memoria local ainda nao consultada."
    @Published var mcpEvents: [MCPEvent] = []
    @Published var isRunning: Bool = false
    @Published var lastError: String?

    let backendClient: BackendClient

    init(backendClient: BackendClient) {
        self.backendClient = backendClient
    }

    func submitPrompt() {
        let text = prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty, !isRunning else {
            return
        }

        isRunning = true
        lastError = nil

        Task {
            do {
                let response = try await backendClient.send(prompt: text)
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
