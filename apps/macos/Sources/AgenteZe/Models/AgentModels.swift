import Foundation

struct AgentResponse: Decodable {
    let requestID: String
    let status: String
    let message: String
    let memorySummary: String
    let mcpEvents: [MCPEvent]
    let errors: [String]

    enum CodingKeys: String, CodingKey {
        case requestID = "request_id"
        case status
        case message
        case memorySummary = "memory_summary"
        case mcpEvents = "mcp_events"
        case errors
    }
}

struct MCPEvent: Decodable, Identifiable {
    var id: String { toolName }

    let toolName: String
    let status: String
    let risk: String
    let message: String

    enum CodingKeys: String, CodingKey {
        case toolName = "tool_name"
        case status
        case risk
        case message
    }
}
