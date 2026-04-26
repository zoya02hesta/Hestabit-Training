"use client"

import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"

export default function BillingPage() {
  return (
    <div className="space-y-6">

      <h1 className="text-2xl font-bold">Billing</h1>

      {/* Current Plan */}
      <Card title="Current Plan" subtitle="Manage your subscription">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          
          <div>
            <h2 className="text-lg font-semibold text-gray-800">
              Pro Plan
            </h2>
            <p className="text-sm text-gray-500">
              $29/month • Renews on 25th July
            </p>
          </div>

          <div className="flex items-center gap-4">
            <Badge variant="working">Active</Badge>
            <Button variant="outline">Change Plan</Button>
          </div>

        </div>
      </Card>

      {/* Payment Method */}
      <Card title="Payment Method">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

          <div className="flex items-center gap-4">
            <div className="bg-blue-600 text-white px-4 py-2 rounded-lg">
              VISA
            </div>
            <div>
              <p className="text-sm font-medium">
                **** **** **** 4587
              </p>
              <p className="text-xs text-gray-500">
                Exp 09/27
              </p>
            </div>
          </div>

          <Button variant="outline">
            Update Card
          </Button>

        </div>
      </Card>

      {/* Billing History */}
      <Card title="Billing History">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            
            <thead className="border-b text-gray-500">
              <tr>
                <th className="py-3">Date</th>
                <th>Invoice</th>
                <th>Amount</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr className="border-b">
                <td className="py-4">Jun 25, 2025</td>
                <td>#INV-1045</td>
                <td>$29.00</td>
                <td><Badge variant="done">Paid</Badge></td>
              </tr>

              <tr className="border-b">
                <td className="py-4">May 25, 2025</td>
                <td>#INV-1034</td>
                <td>$29.00</td>
                <td><Badge variant="done">Paid</Badge></td>
              </tr>

              <tr>
                <td className="py-4">Apr 25, 2025</td>
                <td>#INV-1021</td>
                <td>$29.00</td>
                <td><Badge variant="done">Paid</Badge></td>
              </tr>
            </tbody>

          </table>
        </div>
      </Card>

    </div>
  )
}
