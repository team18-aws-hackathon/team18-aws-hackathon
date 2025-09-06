interface ButtonProps {
  className?: string;
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'rose';
  fullWidth?: boolean;
}

export const Button = ({
  className,
  children,
  onClick,
  variant = 'primary',
  fullWidth,
}: ButtonProps) => {
  const baseClasses =
    'py-4 px-6 rounded-xl border-0 text-base font-semibold cursor-pointer flex items-center justify-center gap-2';
  const widthClass = fullWidth ? 'w-full' : '';

  const variantClasses = {
    primary: 'bg-beige-500 text-white',
    secondary: 'bg-gradient-to-r from-beige-300 to-beige-400 text-white',
    rose: 'bg-accent-400 hover:bg-accent-500 text-white',
  };

  return (
    <button
      className={`${baseClasses} ${widthClass} ${className || variantClasses[variant]}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
