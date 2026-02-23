"use client";

import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-full max-w-md space-y-4">
        <h2 className="text-2xl font-bold text-center">Login</h2>

        <Input placeholder="Username" />
        <Input placeholder="Password" type="password" />

        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center gap-2">
            <input type="checkbox" />
            Remember me
          </label>
          <span className="text-blue-500 cursor-pointer">
            Forgot password?
          </span>
        </div>

        <Button className="w-full">Login</Button>
      </Card>
    </div>
  );
}
