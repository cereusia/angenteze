import Foundation

struct BackendClient {
    var repositoryRoot: URL = RepositoryRootResolver.resolve()

    func send(prompt: String) async throws -> AgentResponse {
        try await Task.detached(priority: .userInitiated) {
            try run(prompt: prompt)
        }.value
    }

    private func run(prompt: String) throws -> AgentResponse {
        let corePath = repositoryRoot.appendingPathComponent("agent-core")
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        process.arguments = [
            "python3",
            "-m",
            "agenteze_core",
            "run",
            "--prompt",
            prompt,
            "--source",
            "macos"
        ]
        process.currentDirectoryURL = repositoryRoot

        var environment = ProcessInfo.processInfo.environment
        environment["AGENTEZE_ROOT"] = repositoryRoot.path
        environment["PYTHONPATH"] = corePath.path
        process.environment = environment

        let outputPipe = Pipe()
        let errorPipe = Pipe()
        process.standardOutput = outputPipe
        process.standardError = errorPipe

        try process.run()
        process.waitUntilExit()

        let outputData = outputPipe.fileHandleForReading.readDataToEndOfFile()
        let errorData = errorPipe.fileHandleForReading.readDataToEndOfFile()

        guard process.terminationStatus == 0 else {
            let stderr = String(data: errorData, encoding: .utf8) ?? "Unknown backend error"
            throw BackendClientError.processFailed(stderr)
        }

        do {
            return try JSONDecoder().decode(AgentResponse.self, from: outputData)
        } catch {
            let stdout = String(data: outputData, encoding: .utf8) ?? ""
            throw BackendClientError.invalidJSON(stdout)
        }
    }
}

enum BackendClientError: LocalizedError {
    case processFailed(String)
    case invalidJSON(String)

    var errorDescription: String? {
        switch self {
        case .processFailed(let message):
            return "Backend local falhou: \(message)"
        case .invalidJSON(let payload):
            return "Backend local retornou JSON invalido: \(payload)"
        }
    }
}
