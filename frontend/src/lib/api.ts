/**
 * Thin fetch wrapper.
 *
 * Types come from `src/lib/api-types.ts`, generated from the backend's OpenAPI schema
 * via `pnpm gen:api`. Never hand-write API types: the backend contract is the source
 * of truth, so a backend change should surface as a compile error here.
 */

const BASE_URL = import.meta.env["VITE_API_BASE_URL"] ?? "/api";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });

  if (!response.ok) {
    throw new ApiError(response.status, `Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}
