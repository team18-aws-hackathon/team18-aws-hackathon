interface InputProps {
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
}

export const Input = ({ placeholder, value, onChange }: InputProps) => {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      className="w-full p-4 rounded-xl border-2 border-gray-300 text-base outline-0 bg-white focus:border-lime-500 focus:bg-lime-100 transition-colors duration-200"
    />
  )
}