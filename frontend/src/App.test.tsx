import { screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "@/App";
import { render } from "@/test/render";

describe("App", () => {
  it("renders the application title", () => {
    render(<App />);

    expect(screen.getByRole("heading", { name: /sports tournament/i })).toBeInTheDocument();
  });

  it("reports backend status once the health query resolves", async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent(/backend\s+ok/i);
    });
  });
});
