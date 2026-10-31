import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const work = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/work" }),
  schema: z.object({
    title: z.string(),
    kind: z.enum(["Curriculum design", "Assessment design", "Data and progress monitoring", "Family engagement", "Advocacy and leadership", "Classroom systems", "Lesson design", "Teacher resources"]),
    madeFor: z.string(),
    format: z.string(),
    languages: z.string().default("English"),
    layout: z.enum(["single", "stack", "clipped", "pair", "ring"]).default("single"),
    tilt: z.number().default(0),
    featured: z.boolean().default(false),
    order: z.number(),
    lede: z.string(),
    alts: z.array(z.string()),
    pairLabel: z.string().optional(),
    prompt: z.string(),
    why: z.string().optional(),
    photos: z.array(z.object({ key: z.string(), alt: z.string(), caption: z.string() })).default([]),
  }),
});

export const collections = { work };
