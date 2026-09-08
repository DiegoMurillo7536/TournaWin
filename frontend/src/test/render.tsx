import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render as rtlRender, type RenderOptions } from "@testing-library/react";
import type { ReactElement, ReactNode } from "react";

/** Render with a fresh QueryClient so cached data never leaks between tests. */
export function render(ui: ReactElement, options?: Omit<RenderOptions, "wrapper">) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, staleTime: 0 } },
  });

  const Wrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );

  return rtlRender(ui, { wrapper: Wrapper, ...options });
}

export * from "@testing-library/react";
