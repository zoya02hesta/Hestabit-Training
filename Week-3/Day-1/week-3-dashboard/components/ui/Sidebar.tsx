export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-slate-900 text-white p-6">
      <h2 className="text-xl font-bold mb-10 tracking-wide">
        Purity UI
      </h2>

      <nav className="space-y-4 text-sm">
        <a href="#" className="block px-3 py-2 rounded-lg hover:bg-slate-800">
          Dashboard
        </a>
        <a href="#" className="block px-3 py-2 rounded-lg hover:bg-slate-800">
          Tables
        </a>
        <a href="#" className="block px-3 py-2 rounded-lg hover:bg-slate-800">
          Billing
        </a>
        <a href="#" className="block px-3 py-2 rounded-lg hover:bg-slate-800">
          Profile
        </a>
      </nav>
    </aside>
  )
}
