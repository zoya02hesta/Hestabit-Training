type InputProps = {
  placeholder?: string
  type?: string
  name?: string
  value?: string
  required?: boolean
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
  className?: string
}

export default function Input({
  placeholder,
  type = "text",
  name,
  value,
  required,
  onChange,
  className = "",
}: InputProps) {
  return (
    <input
      type={type}
      name={name}
      value={value}
      required={required}
      onChange={onChange}
      placeholder={placeholder}
      className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${className}`}
    />
  )
}
