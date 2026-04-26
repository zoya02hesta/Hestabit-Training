type ModalProps = {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}

export default function Modal({
  isOpen,
  onClose,
  children,
}: ModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
      <div className="bg-white rounded-xl p-6 w-96 shadow-lg relative">
        
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500"
        >
          ✕
        </button>

        {children}

      </div>
    </div>
  )
}
