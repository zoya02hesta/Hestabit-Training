"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

const navItems = [
  { name: "Dashboard", icon: "📊", href: "/dashboard" },
  { name: "Users", icon: "📋", href: "/dashboard/user" },
  { name: "Billing", icon: "💳", href: "/dashboard/billing" },
  { name: "Profile", icon: "👤", href: "/dashboard/profile" },
  { name: "Sign In", icon: "🔐", href: "/login" },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 h-screen bg-white shadow-lg border-r border-gray-200 p-6 fixed left-0 top-0">
      
      <div className="mb-10">
        <h2 className="text-lg font-bold text-blue-600">
          Purity UI
        </h2>
      </div>

      <nav className="flex flex-col gap-2">
        {navItems.map((item, index) => {
          const isActive = pathname === item.href

          return (
            <Link
              key={index}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                isActive
                  ? "bg-blue-50 text-blue-600 font-semibold"
                  : "text-gray-600 hover:bg-blue-50 hover:text-blue-600"
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
