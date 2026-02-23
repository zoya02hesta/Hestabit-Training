"use client"

import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"

export default function ProfilePage() {
  return (
    <div className="space-y-6">
      
      <h1 className="text-2xl font-bold">Profile</h1>

      <Card>
        <div className="flex flex-col md:flex-row gap-8">

          {/* Avatar Section */}
          <div className="flex flex-col items-center">
            <img
              src="https://i.pravatar.cc/150?img=5"
              alt="User"
              className="w-32 h-32 rounded-full object-cover"
            />
            <Button variant="outline" className="mt-4">
              Change Photo
            </Button>
          </div>

          {/* Info Section */}
          <div className="flex-1 space-y-4">
            
            <div>
              <label className="text-sm text-gray-500">
                Full Name
              </label>
              <Input placeholder="Zoya Fatima" />
            </div>

            <div>
              <label className="text-sm text-gray-500">
                Email
              </label>
              <Input
                type="email"
                placeholder="zoyaf.hestabit@gmail.com"
              />
            </div>

            <div>
              <label className="text-sm text-gray-500">
                Job Title
              </label>
              <Input placeholder="Trainee SDE" />
            </div>

            <Button className="mt-4">
              Save Changes
            </Button>

          </div>

        </div>
      </Card>

    </div>
  )
}
