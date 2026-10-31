import { getCollection, type CollectionEntry } from "astro:content";
import { u } from "./site";

export type Lang = "en" | "es";

/** Pick the string for this language: t("Hello", "Hola"). */
export const tr = (lang: Lang) => (en: string, es: string) => (lang === "es" ? es : en);

/** Link to a page in this language: lp("es", "/gallery/") -> /SkylerMarkwellPortfolio/es/gallery/ */
export const lp = (lang: Lang, path = "/") => u(lang === "es" ? `/es${path.startsWith("/") ? path : `/${path}`}` : path);

/** Same page in the other language, from the current URL. */
export const otherLangPath = (pathname: string) => {
  const base = import.meta.env.BASE_URL.endsWith("/") ? import.meta.env.BASE_URL : `${import.meta.env.BASE_URL}/`;
  const rest = pathname.startsWith(base) ? pathname.slice(base.length) : pathname.replace(/^\//, "");
  return rest.startsWith("es/") || rest === "es"
    ? { lang: "en" as Lang, href: base + rest.replace(/^es\/?/, "") }
    : { lang: "es" as Lang, href: `${base}es/${rest}` };
};

export const KIND_ES: Record<string, string> = {
  "Curriculum design": "Diseño curricular",
  "Assessment design": "Diseño de evaluaciones",
  "Data and progress monitoring": "Datos y seguimiento del progreso",
  "Family engagement": "Participación familiar",
  "Advocacy and leadership": "Defensa y liderazgo",
  "Classroom systems": "Sistemas del salón",
  "Lesson design": "Diseño de lecciones",
  "Teacher resources": "Recursos para maestros",
};
export const kindLabel = (lang: Lang, kind: string) => (lang === "es" ? KIND_ES[kind] ?? kind : kind);

export type WorkItem = {
  id: string;
  data: CollectionEntry<"work">["data"];
  /** the entry whose Markdown body renders on the piece page */
  body: CollectionEntry<"work"> | CollectionEntry<"workEs">;
};

/** All work pieces in this language, sorted. Spanish text is laid over the English entry's structure. */
export async function workIn(lang: Lang): Promise<WorkItem[]> {
  const en = (await getCollection("work")).sort((a, b) => a.data.order - b.data.order);
  if (lang === "en") return en.map((e) => ({ id: e.id, data: e.data, body: e }));
  const es = Object.fromEntries((await getCollection("workEs")).map((e) => [e.id, e]));
  return en.map((e) => {
    const s = es[e.id];
    if (!s) return { id: e.id, data: e.data, body: e };
    const { photos, ...rest } = s.data;
    return { id: e.id, data: { ...e.data, ...rest, photos: photos ?? e.data.photos }, body: s };
  });
}
