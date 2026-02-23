type CardProps = {
  title?: string
  subtitle?: string
  children: React.ReactNode
  className?: string   // ✅ add this
}

export default function Card({
  title,
  subtitle,
  children,
  className = "",   // ✅ and extract it here
}: CardProps) {
  return (
    <div className={`bg-white rounded-2xl shadow-sm border p-6 ${className}`}>
      
      {title && (
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-800">
            {title}
          </h2>
          {subtitle && (
            <p className="text-sm text-gray-500 mt-1">
              {subtitle}
            </p>
          )}
        </div>
      )}

      {children}

    </div>
  )
}
