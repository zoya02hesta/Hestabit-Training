import Link from "next/link";

const navItems = [
  { name: "Dashboard", icon: "📊" },
  { name: "Tables", icon: "📋" },
  { name: "Billing", icon: "💳" },
  { name: "Profile", icon: "👤" },
  { name: "Sign In", icon: "🔐" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen bg-white shadow-lg border-r border-gray-200 p-6 fixed left-0 top-0">
      
      {/* Logo */}
      <div className="mb-10">
        <h2 className="text-lg font-bold text-blue-600">
          Purity UI
        </h2>
      </div>

      {/* Nav Items */}
      <nav className="flex flex-col gap-2">
        {navItems.map((item, index) => (
          <Link
            key={index}
            href="#"
            className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-blue-50 hover:text-blue-600 transition"
          >
            <span>{item.icon}</span>
            <span className="font-medium">{item.name}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
