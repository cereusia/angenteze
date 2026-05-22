import AppKit
import SwiftUI

@MainActor
final class PromptWindowController {
    private let appState: AppState
    private var window: NSWindow?

    init(appState: AppState) {
        self.appState = appState
    }

    func show() {
        let window = window ?? makeWindow()
        self.window = window
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }

    func toggle() {
        guard let window, window.isVisible else {
            show()
            return
        }
        window.orderOut(nil)
    }

    private func makeWindow() -> NSWindow {
        let view = PromptView()
            .environmentObject(appState)

        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 680, height: 460),
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false
        )
        window.title = "Agente Ze"
        window.center()
        window.contentViewController = NSHostingController(rootView: view)
        window.isReleasedWhenClosed = false
        return window
    }
}
