interface BadgeProps {
  children: React.ReactNode;
  variant?: 'primary' | 'accent' | 'success' | 'warning' | 'danger' | 'gray';
  size?: 'sm' | 'md';
}

const variantClasses = {
  primary: 'bg-primary-100 text-primary-800',
  accent: 'bg-accent-100 text-accent-800',
  success: 'bg-green-100 text-green-800',
  warning: 'bg-yellow-100 text-yellow-800',
  danger: 'bg-red-100 text-red-800',
  gray: 'bg-gray-100 text-gray-800',
};

const sizeClasses = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-sm',
};

export function Badge({ children, variant = 'primary', size = 'sm' }: BadgeProps) {
  return (
    <span
      className={`
        inline-flex items-center font-medium rounded-full
        ${variantClasses[variant]}
        ${sizeClasses[size]}
      `}
    >
      {children}
    </span>
  );
}

// Difficulty badge helper
export function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const variants: Record<string, 'success' | 'warning' | 'danger' | 'accent'> = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger',
    expert: 'accent',
  };

  return (
    <Badge variant={variants[difficulty] || 'gray'}>
      {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
    </Badge>
  );
}

// Status badge helper
export function StatusBadge({ status }: { status: string }) {
  const variants: Record<string, 'gray' | 'primary' | 'success' | 'warning'> = {
    draft: 'gray',
    in_progress: 'primary',
    published: 'success',
    archived: 'warning',
  };

  const labels: Record<string, string> = {
    draft: 'Draft',
    in_progress: 'In Progress',
    published: 'Published',
    archived: 'Archived',
  };

  return <Badge variant={variants[status] || 'gray'}>{labels[status] || status}</Badge>;
}
