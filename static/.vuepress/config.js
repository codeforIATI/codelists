var fs = require("fs")
var locales = JSON.parse(fs.readFileSync("docs/.vuepress/locales.json"))
module.exports = {
  locales: locales,
  themeConfig: {
    locales: locales
  }
}

