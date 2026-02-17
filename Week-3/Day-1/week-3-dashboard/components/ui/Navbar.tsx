export default function Navbar() {
  return (
    <header className="h-20 bg-white/70 backdrop-blur-md border-b border-gray-200 flex items-center justify-between px-8 sticky top-0 z-50">
      
      {/* Left */}
      <div>
        <h1 className="text-xl font-semibold text-gray-800">
          Dashboard
        </h1>
        <p className="text-sm text-gray-500">
          Welcome back 👋
        </p>
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">

        {/* Search */}
        <input
          type="text"
          placeholder="Search..."
          className="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Notification */}
        <button className="p-2 rounded-lg hover:bg-gray-100">
          🔔
        </button>

        {/* Profile */}
        <div className="flex items-center gap-2 cursor-pointer">
          <div className="w-9 h-9 rounded-full bg-blue-500"></div>
          <span className="text-sm font-medium text-gray-700">
            Zoya
          </span>
        </div>
      </div>
    </header>
  );
}
