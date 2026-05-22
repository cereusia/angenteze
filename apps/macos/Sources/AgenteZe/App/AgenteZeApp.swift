import SwiftUI

@main
struct AgenteZeApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate

    var body: some Scene {
        MenuBarExtra("Agente Ze", systemImage: "bolt.circle") {
            MenuBarView()
                .environmentObject(AppController.shared.state)
        }
        .menuBarExtraStyle(.menu)

        Settings {
            SettingsView()
                .environmentObject(AppController.shared.state)
                .frame(width: 420)
        }
    }
}
