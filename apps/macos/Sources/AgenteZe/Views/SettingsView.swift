import SwiftUI

struct SettingsView: View {
    @EnvironmentObject private var appState: AppState

    var body: some View {
        Form {
            Section("Backend") {
                LabeledContent("Status") {
                    Text(appState.isRunning ? "Executando" : "Pronto")
                }

                LabeledContent("Memoria") {
                    Text(appState.memorySummary)
                        .lineLimit(2)
                }
            }

            Section("Atalho") {
                Text("Control + Option + Command + Space")
            }
        }
        .padding()
    }
}
