// Quartz configuration for the published llm-wiki site.
//
// This file is *overlaid* onto a pinned Quartz checkout at build time by
// scripts/build-site.sh (it is copied into .quartz/quartz.config.ts). The
// `./quartz/...` imports below resolve inside that checkout, not in this repo —
// so an "unresolved import" warning here is expected and harmless.
//
// We keep Quartz's defaults and customize only the minimum: site title, the
// GitHub Pages base URL, and a couple of build-cost trims. The published site
// is sourced from the curated wiki/ layer only (see scripts/build-site.sh,
// which passes `--directory wiki`); the immutable raw/ twins are never built.

import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "llm-wiki",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    // No third-party analytics on the published site.
    analytics: null,
    locale: "en-US",
    // GitHub Pages project site: https://bwbensonjr.github.io/llm-wiki/
    baseUrl: "bwbensonjr.github.io/llm-wiki",
    // wiki/ carries an Obsidian vault config that is not reader-facing content.
    ignorePatterns: [".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Schibsted Grotesk",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#faf8f8",
          lightgray: "#e5e5e5",
          gray: "#b8b8b8",
          darkgray: "#4e4e4e",
          dark: "#2b2b2b",
          secondary: "#284b63",
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#fff23688",
        },
        darkMode: {
          light: "#161618",
          lightgray: "#393639",
          gray: "#646464",
          darkgray: "#d4d4d4",
          dark: "#ebebec",
          secondary: "#7b97aa",
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      // Resolves Obsidian [[wikilinks]] in the rendered HTML.
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      // "shortest" resolves links by filename (slug), independent of folder —
      // matching the wiki's linking convention.
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // CustomOgImages() omitted: it pulls in a headless browser and slows the
      // build substantially. Re-add if per-page social preview images are wanted.
    ],
  },
}

export default config
