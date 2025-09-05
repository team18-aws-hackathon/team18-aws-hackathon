interface HeaderProps {
  title: string
  showBack?: boolean
  onBack?: () => void
  rightIcon?: React.ReactNode
}

export const Header = ({ title, showBack, onBack, rightIcon }: HeaderProps) => {
  return (
    <div className={`p-5 flex items-center justify-between text-lg font-semibold ${
      showBack 
        ? 'bg-white text-gray-800' 
        : 'bg-beige-500 text-white'
    }`}>
      {showBack && (
        <button 
          onClick={onBack}
          className="bg-transparent border-0 text-xl cursor-pointer text-gray-800 p-0"
        >
          ←
        </button>
      )}
      <div className="flex-1 text-center">
        <div>{title}</div>
      </div>
      {rightIcon && <div>{rightIcon}</div>}
    </div>
  )
}