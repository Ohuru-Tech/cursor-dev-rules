---
description: Next.js development standards and best practices for App Router, server components, layouts, loading states, and API integration
globs:
  - "**/app/**/*.tsx"
  - "**/app/**/*.ts"
  - "**/app/**/*.jsx"
  - "**/app/**/*.js"
  - "**/pages/**/*.tsx"
  - "**/pages/**/*.tsx"
  - "**/next.config.js"
  - "**/next.config.ts"
alwaysApply: false
---

# Next.js Development Standards

Follow these standards when developing Next.js applications with App Router.

## Server Components and Server Functions

Prefer server components and server functions:

- **Default to server**: Use Server Components by default - they're the default in App Router
- **Server functions**: Create server functions (Server Actions) for mutations and data fetching
- **Client components**: Only use `"use client"` when necessary (interactivity, browser APIs, hooks)
- **Research hooks**: Research and use appropriate hooks - don't default to `useEffect` and `useState` for everything

### Server Components Examples

```tsx
// ✅ Good: Server Component (default)
// app/users/page.tsx
import { fetchUsers } from '@/lib/api/users';

export default async function UsersPage() {
  const users = await fetchUsers();
  
  return (
    <div>
      <h1>Users</h1>
      <UserList users={users} />
    </div>
  );
}

// ✅ Good: Server Action
// app/actions/users.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  // Server-side logic
  await saveUser(name);
  revalidatePath('/users');
}

// ✅ Good: Client Component only when needed
// app/components/UserForm.tsx
'use client';

import { useFormState } from 'react-dom';
import { createUser } from '@/app/actions/users';

export function UserForm() {
  const [state, formAction] = useFormState(createUser, null);
  // Client-side interactivity needed
}
```

## Loading and Zero States

Always implement separate loading and zero states:

- **loading.tsx**: Create `loading.tsx` files for route-level loading states
- **Suspense boundaries**: Use Suspense for component-level loading states
- **Zero states**: Create dedicated zero/empty state components
- **Loading indicators**: Show appropriate loading indicators during navigation

### Loading States Examples

```tsx
// ✅ Good: Route-level loading
// app/users/loading.tsx
export default function UsersLoading() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900" />
    </div>
  );
}

// ✅ Good: Component-level loading with Suspense
// app/users/page.tsx
import { Suspense } from 'react';
import { UserList } from '@/components/UserList';
import { UserListSkeleton } from '@/components/UserListSkeleton';

export default function UsersPage() {
  return (
    <div>
      <h1>Users</h1>
      <Suspense fallback={<UserListSkeleton />}>
        <UserList />
      </Suspense>
    </div>
  );
}

// ✅ Good: Zero state component
// components/EmptyState.tsx
export function EmptyState({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <p className="text-gray-500 text-lg">{message}</p>
    </div>
  );
}

// app/users/page.tsx
export default async function UsersPage() {
  const users = await fetchUsers();
  
  if (users.length === 0) {
    return <EmptyState message="No users found" />;
  }
  
  return <UserList users={users} />;
}
```

## Layouts and Loading Files

Use Next.js layouts and loading files properly:

- **layout.tsx**: Create layout files for shared UI across routes
- **Nested layouts**: Use nested layouts for route groups
- **loading.tsx**: Create loading files at route level for automatic loading states
- **error.tsx**: Create error boundaries with error.tsx files
- **not-found.tsx**: Create custom 404 pages with not-found.tsx

### Layout Examples

```tsx
// ✅ Good: Root layout
// app/layout.tsx
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav>Navigation</nav>
        <main>{children}</main>
        <footer>Footer</footer>
      </body>
    </html>
  );
}

// ✅ Good: Nested layout
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard-container">
      <aside>Dashboard Sidebar</aside>
      <section>{children}</section>
    </div>
  );
}

// ✅ Good: Route-level loading
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return <DashboardSkeleton />;
}
```

## Navigation Indicators

Provide proper indicators when navigating between pages:

- **Loading states**: Show loading indicators during route transitions
- **Progress bars**: Use loading bars or spinners during navigation
- **Optimistic UI**: Show optimistic updates when appropriate
- **Transition feedback**: Provide visual feedback during page transitions

### Navigation Examples

```tsx
// ✅ Good: Navigation with loading indicator
// components/Navigation.tsx
'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useTransition } from 'react';

export function Navigation() {
  const router = useRouter();
  const pathname = usePathname();
  const [isPending, startTransition] = useTransition();
  
  function handleNavigate(href: string) {
    startTransition(() => {
      router.push(href);
    });
  }
  
  return (
    <nav>
      {isPending && <LoadingBar />}
      <Link href="/users" onClick={() => handleNavigate('/users')}>
        Users
      </Link>
    </nav>
  );
}
```

## Next.js Image Component

Use Next.js Image component properly with responsive sizing:

- **Always use Image**: Use `next/image` instead of `<img>` tag
- **Responsive sizes**: Always specify `sizes` prop for responsive images
- **Width and height**: Provide width and height for layout shift prevention
- **Optimization**: Let Next.js handle image optimization
- **Placeholder**: Use blur placeholders for better UX

### Image Examples

```tsx
// ✅ Good: Responsive Image with sizes
import Image from 'next/image';

export function ProductImage({ src, alt }: { src: string; alt: string }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      className="w-full h-auto"
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  );
}

// ✅ Good: Fixed aspect ratio with responsive width
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  sizes="100vw"
  className="w-full h-auto aspect-[2/1]"
/>

// ❌ Bad: Fixed sizing
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  className="w-[1200px] h-[600px]"
/>

// ❌ Bad: Using img tag
<img src="/hero.jpg" alt="Hero" />
```

## Responsive Sizing

Always prefer responsive sizing, never use fixed sizing:

- **Relative units**: Use rem, em, %, vw, vh instead of px for sizing
- **Flexible layouts**: Use flexbox and grid for responsive layouts
- **Container queries**: Use container queries when appropriate
- **Max-width**: Use max-width instead of fixed width
- **Tailwind classes**: Use Tailwind responsive classes (sm:, md:, lg:, xl:)

### Responsive Sizing Examples

```tsx
// ✅ Good: Responsive with Tailwind
<div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {items.map(item => <Card key={item.id} item={item} />)}
  </div>
</div>

// ✅ Good: Responsive with CSS
.container {
  width: 100%;
  max-width: 1200px;
  padding: 1rem clamp(1rem, 4vw, 2rem);
}

// ❌ Bad: Fixed sizing
<div className="w-[1200px] px-[40px]">
  <div className="grid grid-cols-3 gap-[20px]">
    {items.map(item => <Card key={item.id} item={item} />)}
  </div>
</div>
```

## API Integration and Error Handling

Separate API concerns and implement proper error handling:

- **Server functions**: Create server functions for API calls
- **Error handlers**: Create general error handlers that can queue toasts or return errors
- **Separate concerns**: Keep API calling/formatting logic separate from UI/UX logic
- **Ask for API details**: When API responses/errors aren't available, ask the user for the structure
- **Type safety**: Type API responses properly

### API Integration Examples

```typescript
// ✅ Good: Server function with error handling
// lib/api/users.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface ApiError {
  message: string;
  code?: string;
}

export async function fetchUsers(): Promise<{ data?: User[]; error?: ApiError }> {
  try {
    const response = await fetch(`${process.env.API_URL}/users`, {
      cache: 'no-store',
    });
    
    if (!response.ok) {
      const error = await response.json();
      return { error: { message: error.message || 'Failed to fetch users', code: error.code } };
    }
    
    const data = await response.json();
    return { data };
  } catch (error) {
    return { 
      error: { 
        message: error instanceof Error ? error.message : 'An unexpected error occurred' 
      } 
    };
  }
}

// ✅ Good: Error handler utility
// lib/utils/error-handler.ts
import { toast } from 'sonner';

export interface ErrorHandlerOptions {
  showToast?: boolean;
  defaultMessage?: string;
}

export function handleApiError(
  error: unknown,
  options: ErrorHandlerOptions = {}
): string {
  const { showToast = true, defaultMessage = 'An error occurred' } = options;
  
  let message = defaultMessage;
  
  if (error instanceof Error) {
    message = error.message;
  } else if (typeof error === 'object' && error !== null && 'message' in error) {
    message = String(error.message);
  }
  
  if (showToast) {
    toast.error(message);
  }
  
  return message;
}

// ✅ Good: Server component using API
// app/users/page.tsx
import { fetchUsers } from '@/lib/api/users';
import { handleApiError } from '@/lib/utils/error-handler';

export default async function UsersPage() {
  const result = await fetchUsers();
  
  if (result.error) {
    // Handle error appropriately
    return <ErrorMessage message={result.error.message} />;
  }
  
  return <UserList users={result.data || []} />;
}

// ✅ Good: Client component with error handling
// components/UserForm.tsx
'use client';

import { useActionState } from 'react';
import { createUser } from '@/app/actions/users';
import { handleApiError } from '@/lib/utils/error-handler';
import { toast } from 'sonner';

export function UserForm() {
  const [state, formAction, isPending] = useActionState(createUser, null);
  
  if (state?.error) {
    handleApiError(state.error, { showToast: true });
  }
  
  return (
    <form action={formAction}>
      {/* Form fields */}
    </form>
  );
}
```

## Hooks Usage

Research and use appropriate hooks - don't spam "use client", "useEffect", "useState":

- **Server by default**: Keep components as Server Components when possible
- **Appropriate hooks**: Use the right hook for the job (useTransition, useActionState, useOptimistic)
- **Avoid unnecessary effects**: Don't use useEffect for derived state or data fetching
- **Research patterns**: Research Next.js and React patterns before implementing

### Hooks Examples

```tsx
// ✅ Good: Using useTransition for navigation
'use client';

import { useTransition } from 'react';
import { useRouter } from 'next/navigation';

export function Navigation() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  
  function navigate(path: string) {
    startTransition(() => {
      router.push(path);
    });
  }
  
  return (
    <button onClick={() => navigate('/users')} disabled={isPending}>
      {isPending ? 'Loading...' : 'Go to Users'}
    </button>
  );
}

// ✅ Good: Using useActionState for forms
'use client';

import { useActionState } from 'react';
import { createUser } from '@/app/actions/users';

export function UserForm() {
  const [state, formAction, isPending] = useActionState(createUser, null);
  
  return (
    <form action={formAction}>
      <input name="name" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
      {state?.error && <p className="error">{state.error}</p>}
    </form>
  );
}

// ✅ Good: Using useOptimistic for optimistic updates
'use client';

import { useOptimistic } from 'react';

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );
  
  async function addTodo(formData: FormData) {
    const newTodo = { id: Date.now(), text: formData.get('text') as string };
    addOptimisticTodo(newTodo);
    await createTodo(newTodo);
  }
  
  return (
    <form action={addTodo}>
      {/* Form */}
    </form>
  );
}

// ❌ Bad: Unnecessary useEffect and useState
'use client';

import { useEffect, useState } from 'react';

export function UserList() {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);
  
  // Should be a Server Component instead
}
```

## File Organization

Organize files following Next.js App Router conventions:

```text
app/
├── layout.tsx           # Root layout
├── page.tsx             # Home page
├── loading.tsx          # Root loading state
├── error.tsx            # Root error boundary
├── not-found.tsx        # 404 page
├── globals.css          # Global styles
├── users/
│   ├── layout.tsx       # Nested layout
│   ├── page.tsx         # Users list page
│   ├── loading.tsx      # Route loading state
│   ├── error.tsx        # Route error boundary
│   └── [id]/
│       ├── page.tsx     # User detail page
│       └── loading.tsx
├── actions/             # Server actions
│   └── users.ts
└── components/          # Shared components
    ├── ui/              # UI components
    └── features/        # Feature components
```

## Best Practices

- **Server-first**: Default to Server Components, only use Client Components when needed
- **Type safety**: Use TypeScript for all files
- **Error boundaries**: Implement error.tsx files at appropriate levels
- **Metadata**: Use metadata API for SEO and social sharing
- **Route handlers**: Use route handlers for API endpoints when needed
- **Middleware**: Use middleware for authentication, redirects, and request modification
- **Environment variables**: Use environment variables for configuration
- **Code splitting**: Leverage Next.js automatic code splitting
- **Performance**: Use Next.js built-in optimizations (Image, Font, Script)
