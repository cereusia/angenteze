// swift-tools-version: 5.9

import PackageDescription

let package = Package(
    name: "AgenteZeMac",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(name: "AgenteZe", targets: ["AgenteZe"])
    ],
    targets: [
        .executableTarget(
            name: "AgenteZe",
            path: "Sources/AgenteZe"
        )
    ]
)
