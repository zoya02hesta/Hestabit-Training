type BadgeProps = {
  children: React.ReactNode
  variant?: "online" | "offline" | "working" | "done" | "canceled"
}

export default function Badge({
  children,
  variant = "online",
}: BadgeProps) {

  const styles = {
    online: "bg-green-100 text-green-600",
    offline: "bg-gray-200 text-gray-500",
    working: "bg-blue-100 text-blue-600",
    done: "bg-green-100 text-green-600",
    canceled: "bg-red-100 text-red-600",
  }

  return (
    <span className={`text-xs font-medium px-3 py-1 rounded-full ${styles[variant]}`}>
      {children}
    </span>
  )
}
