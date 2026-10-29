import manifest from "../data/previews.json";

export type Preview = { src: string; width: number; height: number };

const BASE = import.meta.env.BASE_URL.replace(/\/$/, "");

/** Prefix an internal path with the site's base path. */
export const u = (path = "/") => `${BASE}${path.startsWith("/") ? path : `/${path}`}`;

/** Preview images for a piece (empty when previews have not been built). */
export const previewsFor = (slug: string): Preview[] =>
  ((manifest as Record<string, Preview[]>)[slug] ?? []).map((p) => ({ ...p, src: u(`/${p.src}`) }));

export const headshot = (): Preview | undefined => previewsFor("_headshot")[0];

export const EMAIL = "markwell.skyler@gmail.com";
export const LINKEDIN = "https://www.linkedin.com/in/skyler-markwell-3979b9216";
