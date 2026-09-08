import { QueryClient } from "@tanstack/react-query";

/**
 * Server state is cached, stale-able and refetchable — a different problem from UI
 * state. These defaults suit tournament data: it changes when matches are played,
 * not continuously.
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
