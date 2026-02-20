
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"

export default function Home() {
  return (
    <div className="p-8 bg-gray-100 min-h-screen space-y-8">

      {/* Authors Table */}
      <Card title="Authors Table">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-gray-400 uppercase text-xs">
              <tr>
                <th className="pb-3">Author</th>
                <th className="pb-3">Function</th>
                <th className="pb-3">Status</th>
              </tr>
            </thead>
<tbody className="divide-y">
  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">
        
        {/* Avatar */}
        <img
          src="https://i.pravatar.cc/40?img=1"
          alt="Esthera Jackson"
          className="w-10 h-10 rounded-full object-cover"
        />

        {/* Name + Email */}
        <div>
          <p className="font-semibold text-gray-800">
            Esthera Jackson
          </p>
          <p className="text-sm text-gray-400">
            esthera.jackson@mail.com
          </p>
        </div>

      </div>
    </td>

    <td>Manager</td>

    <td>
      <Badge variant="online">Online</Badge>
    </td>
  </tr>

  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">
        <img
          src="https://i.pravatar.cc/40?img=2"
          alt="Alexa Liras"
          className="w-10 h-10 rounded-full object-cover"
        />
        <div>
          <p className="font-semibold text-gray-800">
            Alexa Liras
          </p>
          <p className="text-sm text-gray-400">
            alexa.liras@mail.com
          </p>
        </div>
      </div>
    </td>
    <td>Programmer</td>
    <td>
      <Badge variant="offline">Offline</Badge>
    </td>
  </tr>

  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">
        <img
          src="https://i.pravatar.cc/40?img=3"
          alt="Laurent Perrier"
          className="w-10 h-10 rounded-full object-cover"
        />
        <div>
          <p className="font-semibold text-gray-800">
            Laurent Perrier
          </p>
          <p className="text-sm text-gray-400">
            laurent@mail.com
          </p>
        </div>
      </div>
    </td>
    <td>Executive</td>
    <td>
      <Badge variant="online">Online</Badge>
    </td>
  </tr>

  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">
        <img
          src="https://i.pravatar.cc/40?img=4"
          alt="Michael Chan"
          className="w-10 h-10 rounded-full object-cover"
        />
        <div>
          <p className="font-semibold text-gray-800">
            Michael Chan
          </p>
          <p className="text-sm text-gray-400">
            michael.chan@mail.com
          </p>
        </div>
      </div>
    </td>
    <td>Designer</td>
    <td>
      <Badge variant="offline">Offline</Badge>
    </td>
  </tr>
</tbody>

          </table>
        </div>
      </Card>

      {/* Projects Table */}
      <Card
        title="Projects"
        subtitle="30 done this month"
      >
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-left text-gray-400 uppercase text-xs">
              <tr>
                <th className="pb-3">Companies</th>
                <th className="pb-3">Budget</th>
                <th className="pb-3">Status</th>
              </tr>
            </thead>

            <tbody className="divide-y">
  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">

        {/* Logo */}
        <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
          <span className="text-purple-600 font-bold">C</span>
        </div>

        {/* Project Info */}
        <div>
          <p className="font-semibold text-gray-800">
            Chakra Soft UI Version
          </p>
          <p className="text-sm text-gray-400">
            React + Chakra UI
          </p>
        </div>

      </div>
    </td>

    <td>$14,000</td>

    <td>
      <Badge variant="working">Working</Badge>
    </td>
  </tr>

  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">

        <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
          <span className="text-blue-600 font-bold">P</span>
        </div>

        <div>
          <p className="font-semibold text-gray-800">
            Add Progress Track
          </p>
          <p className="text-sm text-gray-400">
            Backend Module
          </p>
        </div>

      </div>
    </td>

    <td>$3,000</td>

    <td>
      <Badge variant="canceled">Canceled</Badge>
    </td>
  </tr>

  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">

        <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
          <span className="text-green-600 font-bold">M</span>
        </div>

        <div>
          <p className="font-semibold text-gray-800">
            Launch our Mobile App
          </p>
          <p className="text-sm text-gray-400">
            Flutter + Firebase
          </p>
        </div>

      </div>
    </td>

    <td>$32,000</td>

    <td>
      <Badge variant="done">Done</Badge>
    </td>
  </tr>

  <tr>
    <td className="py-4">
      <div className="flex items-center gap-4">

        <div className="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center">
          <span className="text-orange-600 font-bold">D</span>
        </div>

        <div>
          <p className="font-semibold text-gray-800">
            Database Migration
          </p>
          <p className="text-sm text-gray-400">
            PostgreSQL Upgrade
          </p>
        </div>

      </div>
    </td>

    <td>$12,000</td>

    <td>
      <Badge variant="working">Working</Badge>
    </td>
  </tr>
</tbody>
          </table>
        </div>
      </Card>

    </div>
  )
}
