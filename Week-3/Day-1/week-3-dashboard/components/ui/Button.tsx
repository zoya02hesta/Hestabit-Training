type ButtonProps = {
  children: React.ReactNode
  variant?: "primary" | "secondary" | "outline"
  onClick?: () => void
}

export default function Button({
  children,
  variant = "primary",
  onClick,
}: ButtonProps) {
  
  const baseStyles =
    "px-4 py-2 rounded-lg text-sm font-medium transition"

  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    outline: "border border-gray-300 text-gray-700 hover:bg-gray-100",
  }

  return (
    <button
      onClick={onClick}
      className={`${baseStyles} ${variants[variant]}`}
    >
      {children}
    </button>
  )
}
