import manifest from "../data/previews.json";
import photoManifest from "../data/photos.json";

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

type PhotoEntry = { srcset?: Preview[]; width: number; height: number; video?: string; poster?: string };
export type Photo = { src: string; srcset: string; width: number; height: number; video?: string; poster?: string };

/** A photo from Skyler's library (undefined when photos have not been built). */
export const photo = (key: string): Photo | undefined => {
  const e = (photoManifest as Record<string, PhotoEntry>)[key];
  if (!e) return undefined;
  if (e.video) return { src: u(`/${e.poster}`), srcset: "", width: e.width, height: e.height, video: u(`/${e.video}`), poster: u(`/${e.poster}`) };
  const set = e.srcset ?? [];
  return { src: u(`/${set[0].src}`), srcset: set.map((x) => `${u(`/${x.src}`)} ${x.width}w`).join(", "), width: e.width, height: e.height };
};
