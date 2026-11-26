// Prints an inline SVG QR code for a URL, using macOS CoreImage (no installs).
// Usage: swift tools/qr.swift https://pedromosquera.github.io/ai-workshop-bcn/
import CoreImage
import Foundation

guard CommandLine.arguments.count == 2 else {
    FileHandle.standardError.write("usage: swift tools/qr.swift <url>\n".data(using: .utf8)!)
    exit(2)
}
let url = CommandLine.arguments[1]

let filter = CIFilter(name: "CIQRCodeGenerator")!
filter.setValue(url.data(using: .utf8), forKey: "inputMessage")
filter.setValue("M", forKey: "inputCorrectionLevel")
let image = filter.outputImage!
let size = Int(image.extent.width)

var pixels = [UInt8](repeating: 0, count: size * size)
let context = CGContext(data: &pixels, width: size, height: size, bitsPerComponent: 8, bytesPerRow: size,
                        space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
context.draw(CIContext().createCGImage(image, from: image.extent)!, in: CGRect(x: 0, y: 0, width: size, height: size))

// One subpath per horizontal run of dark modules keeps the SVG small.
var d = ""
for y in 0..<size {
    var x = 0
    while x < size {
        guard pixels[y * size + x] < 128 else { x += 1; continue }
        let start = x
        while x < size && pixels[y * size + x] < 128 { x += 1 }
        d += "M\(start) \(y)h\(x - start)v1h-\(x - start)z"
    }
}
print("<svg viewBox=\"0 0 \(size) \(size)\" shape-rendering=\"crispEdges\" role=\"img\" aria-label=\"QR code for \(url)\"><path d=\"\(d)\"/></svg>")
