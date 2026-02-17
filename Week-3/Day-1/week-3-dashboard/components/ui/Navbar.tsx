export default function Navbar() {
  return (
    <header className="h-16 bg-white shadow-sm border-b flex items-center justify-between px-6">
      
      <h1 className="text-lg font-semibold text-gray-700">
        Dashboard
      </h1>

      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="Search..."
          className="border rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <div className="w-9 h-9 bg-gray-300 rounded-full"></div>
      </div>

    </header>
  )
}
