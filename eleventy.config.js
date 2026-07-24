module.exports = function (eleventyConfig) {
  // Page templates are plain HTML + JSON front matter; only layouts use Nunjucks.
  // Static files (assets, redirects, 404/thanks/subscribed, newsletter) are
  // copied by `npm run build:static` — see package.json.
  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
    htmlTemplateEngine: false,
    markdownTemplateEngine: false,
  };
};
