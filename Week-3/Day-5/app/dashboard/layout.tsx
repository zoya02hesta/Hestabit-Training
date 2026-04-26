import Sidebar from "@/components/ui/Sidebar";
import Navbar from "@/components/ui/Navbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex">
      <Sidebar />

      <div className="ml-72 w-full">
        <Navbar />

        <main className="p-8 bg-gray-100 min-h-screen">
          {children}
        </main>
      </div>
    </div>
  );
}
