import SwiftUI

struct MenuBarView: View {
    @EnvironmentObject private var appState: AppState

    var body: some View {
        Button("Abrir Prompt") {
            AppController.shared.showPrompt()
        }
        .keyboardShortcut(" ", modifiers: [.command, .option, .control])

        Divider()

        Text(appState.isRunning ? "Backend consultando..." : "Backend local pronto")

        if let lastError = appState.lastError {
            Text(lastError)
                .lineLimit(1)
        }

        Divider()

        Button("Sair") {
            AppController.shared.quit()
        }
        .keyboardShortcut("q", modifiers: [.command])
    }
}
