interface TextAreaProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
}

export const TextArea = ({ placeholder, value, onChange }: TextAreaProps) => {
  return (
    <textarea
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      className="w-full min-h-[400px] p-4 rounded-xl border-2 border-gray-300 text-base outline-0 resize-none font-inherit focus:border-rose-300 transition-colors duration-200"
    />
  );
};
