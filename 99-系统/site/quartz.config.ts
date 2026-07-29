import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * 全球风电行业数据库 —— Quartz 站点配置
 * 由 .github/workflows/deploy.yml 在构建时复制进 Quartz 仓库根目录。
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "全球风电行业数据库",
    pageTitleSuffix: "",
    // ⚠️ 必须保持 false。
    // 开启 SPA 后，Quartz 会用 fetch 抓回页面再塞进当前文档，而不是真正跳转。
    // 首页（index.html）是 build_dashboard.py 生成的独立页面，它的交互全靠内联
    // <script>：SPA 注入的内联脚本不会执行，DOMContentLoaded 也早已触发过，
    // 结果就是从笔记站点点回首页时，Tab 栏和表格全空、搜索框连 placeholder 都没有。
    // 代价只是页面切换变成整页加载，这个站体量很小，感知不到。
    enableSPA: false,
    enablePopovers: true,
    analytics: null,              // 内部资料，不接入任何分析
    locale: "zh-CN",
    baseUrl: "wind-db.pages.dev", // 部署后改成你的实际域名
    ignorePatterns: [
      "90-模板/**",
      "99-系统/scripts/**",
      "99-系统/日志/**",
      "**/*.xlsx",
      "**/~$*",
      "private",
      "templates",
      ".obsidian",
    ],
    defaultDateType: "modified",
    generateSocialImages: false,
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Sans SC",
        body: "Noto Sans SC",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#ffffff",
          lightgray: "#e5e9f0",
          gray: "#8b95a5",
          darkgray: "#1a1a2e",
          dark: "#142640",
          secondary: "#1b3a5c",
          tertiary: "#3d6ea5",
          highlight: "rgba(61, 110, 165, 0.12)",
          textHighlight: "#fff3c4",
        },
        darkMode: {
          light: "#0f1b2a",
          lightgray: "#1f2d3f",
          gray: "#5a6b80",
          darkgray: "#c8d3e0",
          dark: "#eaf0f7",
          secondary: "#7aa5d2",
          tertiary: "#a0c4e8",
          highlight: "rgba(122, 165, 210, 0.15)",
          textHighlight: "#8b6914",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({ priority: ["frontmatter", "git", "filesystem"] }),
      Plugin.SyntaxHighlighting({ theme: { light: "github-light", dark: "github-dark" }, keepBackground: false }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
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
      Plugin.ContentIndex({ enableSiteMap: true, enableRSS: true }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
