"use client"

import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"

const users = [
  {
    id: 1,
    name: "Nina Valentine",
    email: "nina@example.com",
    role: "Product Designer",
    status: "online",
  },
  {
    id: 2,
    name: "Arjun Mehta",
    email: "arjun@example.com",
    role: "Frontend Developer",
    status: "working",
  },
  {
    id: 3,
    name: "Sophia Carter",
    email: "sophia@example.com",
    role: "Project Manager",
    status: "offline",
  },
  {
    id: 4,
    name: "Daniel Kim",
    email: "daniel@example.com",
    role: "Backend Engineer",
    status: "done",
  },
]

export default function UsersPage() {
  return (
    <div className="space-y-6">
      
      <h1 className="text-2xl font-bold">Users</h1>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            
            <thead className="border-b text-sm text-gray-500">
              <tr>
                <th className="py-3">Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr
                  key={user.id}
                  className="border-b last:border-none text-sm"
                >
                  <td className="py-4 font-medium">
                    {user.name}
                  </td>
                  <td className="text-gray-500">
                    {user.email}
                  </td>
                  <td>{user.role}</td>
                  <td>
                    <Badge variant={user.status as any}>
                      {user.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>

          </table>
        </div>
      </Card>

    </div>
  )
}
