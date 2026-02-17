type InputProps = {
  placeholder?: string
  type?: string
}

export default function Input({
  placeholder,
  type = "text",
}: InputProps) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  )
}
