import Foundation

struct BackendClient {
    var repositoryRoot: URL = RepositoryRootResolver.resolve()

    func send(prompt: String, confirmedTools: [String] = []) async throws -> AgentResponse {
        try await Task.detached(priority: .userInitiated) {
            try run(prompt: prompt, confirmedTools: confirmedTools)
        }.value
    }

    private func run(prompt: String, confirmedTools: [String]) throws -> AgentResponse {
        let corePath = repositoryRoot.appendingPathComponent("agent-core")
        let process = Process()
        let pythonExecutable = resolvePythonExecutable()
        process.executableURL = pythonExecutable.executableURL
        var arguments = pythonExecutable.prefixArguments + [
            "-m",
            "agenteze_core",
            "run",
            "--prompt",
            prompt,
            "--source",
            "macos"
        ]

        for toolName in confirmedTools.sorted() {
            arguments.append("--confirm-tool")
            arguments.append(toolName)
        }

        process.arguments = arguments
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

    private func resolvePythonExecutable() -> PythonExecutable {
        let fileManager = FileManager.default
        let environment = ProcessInfo.processInfo.environment

        if let override = environment["AGENTEZE_PYTHON_EXECUTABLE"],
           fileManager.isExecutableFile(atPath: override) {
            return PythonExecutable(
                executableURL: URL(fileURLWithPath: override),
                prefixArguments: []
            )
        }

        let embedded = repositoryRoot
            .appendingPathComponent("apps/macos/Resources/python/.venv/bin/python3")
        if fileManager.isExecutableFile(atPath: embedded.path) {
            return PythonExecutable(executableURL: embedded, prefixArguments: [])
        }

        return PythonExecutable(
            executableURL: URL(fileURLWithPath: "/usr/bin/env"),
            prefixArguments: ["python3"]
        )
    }
}

private struct PythonExecutable {
    let executableURL: URL
    let prefixArguments: [String]
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
