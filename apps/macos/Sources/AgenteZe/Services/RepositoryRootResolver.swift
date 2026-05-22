import Foundation

enum RepositoryRootResolver {
    static func resolve() -> URL {
        let fileManager = FileManager.default

        if let envRoot = ProcessInfo.processInfo.environment["AGENTEZE_ROOT"] {
            let url = URL(fileURLWithPath: envRoot)
            if isRepositoryRoot(url, fileManager: fileManager) {
                return url
            }
        }

        let candidates = [
            Bundle.main.bundleURL,
            URL(fileURLWithPath: fileManager.currentDirectoryPath),
            URL(fileURLWithPath: CommandLine.arguments.first ?? fileManager.currentDirectoryPath)
                .deletingLastPathComponent()
        ]

        for candidate in candidates {
            if let root = climb(from: candidate, fileManager: fileManager) {
                return root
            }
        }

        return URL(fileURLWithPath: fileManager.currentDirectoryPath)
    }

    private static func climb(from start: URL, fileManager: FileManager) -> URL? {
        var current = start.standardizedFileURL
        if current.pathExtension == "app" {
            current.deleteLastPathComponent()
        }

        while current.path != "/" {
            if isRepositoryRoot(current, fileManager: fileManager) {
                return current
            }
            current.deleteLastPathComponent()
        }

        return nil
    }

    private static func isRepositoryRoot(_ url: URL, fileManager: FileManager) -> Bool {
        fileManager.fileExists(atPath: url.appendingPathComponent("AGENTS.md").path)
            && fileManager.fileExists(atPath: url.appendingPathComponent("agent-core").path)
    }
}
