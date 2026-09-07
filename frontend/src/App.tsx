import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";

interface Health {
  status: string;
  environment: string;
}

export function App() {
  const { data, isPending, isError } = useQuery({
    queryKey: ["health"],
    queryFn: () => apiFetch<Health>("/health"),
  });

  return (
    <main className="mx-auto flex min-h-dvh max-w-2xl flex-col justify-center gap-4 px-4 py-8">
      <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Sports Tournament</h1>
      <p className="text-sm text-muted-foreground">
        Scaffold is running. Backend connectivity check:
      </p>
      <div className="rounded-lg border border-border p-4 text-sm" role="status">
        {isPending && <span>Checking backend…</span>}
        {isError && <span className="text-red-600">Backend unreachable</span>}
        {data && (
          <span>
            Backend <strong>{data.status}</strong> ({data.environment})
          </span>
        )}
      </div>
    </main>
  );
}
