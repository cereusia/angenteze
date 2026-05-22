import AppKit

final class AppDelegate: NSObject, NSApplicationDelegate {
    private let hotKeyController = HotKeyController()

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        hotKeyController.registerDefaultHotKey {
            AppController.shared.togglePrompt()
        }
    }

    func applicationWillTerminate(_ notification: Notification) {
        hotKeyController.unregister()
    }
}
