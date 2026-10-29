// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

// GitHub Pages project site. When a custom domain is added, set `site` to it and remove `base`.
export default defineConfig({
  site: "https://judemarkwell.github.io",
  base: "/SkylerMarkwellPortfolio",
  trailingSlash: "always",
  vite: { plugins: [tailwindcss()] },
});
