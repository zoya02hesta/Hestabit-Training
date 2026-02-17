import "./globals.css"



import Navbar from "@/components/ui/Navbar";
import Sidebar from "@/components/ui/Sidebar";
import "./globals.css";

export default function RootLayout({ 
    children,
}: {
  children: React.ReactNode

}) {
  return (
    <html lang="en">
      <body className="bg-gray-100">
        <Sidebar />
        
        <div className="ml-64">
          <Navbar />
          <main className="p-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
