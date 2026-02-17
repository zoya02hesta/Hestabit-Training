import "./globals.css"
import Sidebar from "@/components/ui/Sidebar"
import Navbar from "@/components/ui/Navbar"

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex">
          
          <Sidebar />

          <div className="flex-1 bg-gray-100 min-h-screen">
            <Navbar />
            <main className="p-6">
              {children}
            </main>
          </div>

        </div>
      </body>
    </html>
  )
}
