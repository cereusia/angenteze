import AppKit

@MainActor
final class AppController {
    static let shared = AppController()

    let state: AppState
    private lazy var promptWindowController = PromptWindowController(appState: state)

    private init() {
        self.state = AppState(backendClient: BackendClient())
    }

    func showPrompt() {
        promptWindowController.show()
    }

    func togglePrompt() {
        promptWindowController.toggle()
    }

    func quit() {
        NSApp.terminate(nil)
    }
}
