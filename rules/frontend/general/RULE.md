---
description: General frontend development standards and best practices for modern web applications
globs:
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.css"
  - "**/*.scss"
  - "**/package.json"
  - "**/tsconfig.json"
alwaysApply: false
---

# Frontend Development Standards

Follow these standards when developing frontend applications.

## Component Architecture

Organize components with clear separation of concerns:

- **Component composition**: Build complex UIs from small, reusable components
- **Single responsibility**: Each component should have a single, well-defined purpose
- **Props interface**: Define clear prop interfaces/types for components
- **Component organization**: Group related components in logical directory structures

### Component Structure

```text
components/
├── ui/              # Reusable UI components (buttons, inputs, etc.)
├── features/        # Feature-specific components
├── layouts/         # Layout components
└── common/          # Shared/common components
```

## State Management

Choose appropriate state management patterns:

- **Local state**: Use component state for UI-only concerns (toggles, form inputs)
- **Global state**: Use context, state management libraries (Redux, Zustand) for shared state
- **Server state**: Use React Query, SWR, or similar for server data
- **URL state**: Use URL parameters/query strings for shareable, bookmarkable state

## Responsive Design

Always build responsive, mobile-first interfaces:

- **Mobile-first**: Design for mobile devices first, then enhance for larger screens
- **Flexible layouts**: Use flexbox, grid, and relative units (rem, em, %) instead of fixed pixels
- **Breakpoints**: Use consistent breakpoints across the application
- **Touch targets**: Ensure interactive elements are at least 44x44px for touch devices
- **Viewport meta**: Always include proper viewport meta tag

### Responsive Examples

```css
/* ✅ Good: Responsive with relative units */
.container {
  width: 100%;
  max-width: 1200px;
  padding: 1rem 2rem;
  margin: 0 auto;
}

.card {
  width: 100%;
  padding: 1.5rem;
}

@media (min-width: 768px) {
  .card {
    padding: 2rem;
  }
}

/* ❌ Bad: Fixed sizing */
.container {
  width: 1200px;
  padding: 20px 40px;
}

.card {
  width: 400px;
  padding: 30px;
}
```

## Loading and Error States

Always implement proper loading and error states:

- **Loading states**: Show loading indicators for async operations
- **Error states**: Display user-friendly error messages with recovery options
- **Empty states**: Create meaningful empty states (zero states) when no data is available
- **Skeleton screens**: Use skeleton loaders for better perceived performance

### State Examples

```tsx
// ✅ Good: Proper state handling
function UserList() {
  const { data, isLoading, error } = useUsers();
  
  if (isLoading) {
    return <UserListSkeleton />;
  }
  
  if (error) {
    return <ErrorMessage error={error} onRetry={() => refetch()} />;
  }
  
  if (!data || data.length === 0) {
    return <EmptyState message="No users found" />;
  }
  
  return (
    <ul>
      {data.map(user => <UserItem key={user.id} user={user} />)}
    </ul>
  );
}

// ❌ Bad: Missing states
function UserList() {
  const { data } = useUsers();
  return (
    <ul>
      {data.map(user => <UserItem key={user.id} user={user} />)}
    </ul>
  );
}
```

## API Integration

Handle API calls with proper error handling and separation of concerns:

- **API layer**: Separate API calling logic from UI components
- **Error handling**: Implement consistent error handling across API calls
- **Type safety**: Use TypeScript types/interfaces for API responses
- **Request/response transformation**: Handle data transformation in API layer, not components

### API Integration Examples

```typescript
// ✅ Good: Separated API layer
// api/users.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export async function fetchUsers(): Promise<User[]> {
  const response = await fetch('/api/users');
  if (!response.ok) {
    throw new Error('Failed to fetch users');
  }
  return response.json();
}

// hooks/useUsers.ts
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });
}

// components/UserList.tsx
function UserList() {
  const { data, isLoading, error } = useUsers();
  // UI logic only
}
```

## Accessibility

Build accessible applications:

- **Semantic HTML**: Use semantic HTML elements (nav, main, article, etc.)
- **ARIA attributes**: Use ARIA attributes when semantic HTML isn't sufficient
- **Keyboard navigation**: Ensure all interactive elements are keyboard accessible
- **Focus management**: Manage focus appropriately, especially in modals and dynamic content
- **Color contrast**: Ensure sufficient color contrast (WCAG AA minimum)
- **Alt text**: Always provide alt text for images

## Performance

Optimize for performance:

- **Code splitting**: Use dynamic imports and code splitting for large bundles
- **Lazy loading**: Lazy load components and images when appropriate
- **Memoization**: Use React.memo, useMemo, useCallback when appropriate
- **Debouncing/Throttling**: Debounce/throttle expensive operations (search, scroll handlers)
- **Bundle size**: Monitor and optimize bundle size

## TypeScript

Use TypeScript for type safety:

- **Strict mode**: Enable strict TypeScript settings
- **Type definitions**: Define types/interfaces for all data structures
- **Avoid any**: Avoid using `any` type, use `unknown` when type is truly unknown
- **Generic types**: Use generics for reusable, type-safe components

## Code Organization

Organize code logically:

- **Feature-based**: Organize by features when appropriate
- **Layer-based**: Separate by layers (components, hooks, utils, types)
- **Barrel exports**: Use index files for clean imports
- **Naming conventions**: Use consistent naming (PascalCase for components, camelCase for functions)

## Best Practices

- **DRY principle**: Don't repeat yourself - extract reusable logic
- **Consistent styling**: Use consistent styling approach (CSS modules, styled-components, Tailwind)
- **Environment variables**: Use environment variables for configuration
- **Error boundaries**: Implement error boundaries to catch React errors
- **Testing**: Write tests for critical components and logic
- **Documentation**: Document complex logic and non-obvious decisions
