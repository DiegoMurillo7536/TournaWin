import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

export const handlers = [
  http.get("/api/health", () => HttpResponse.json({ status: "ok", environment: "test" })),
];

export const server = setupServer(...handlers);
