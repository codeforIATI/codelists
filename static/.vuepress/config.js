var fs = require("fs")
var locales = JSON.parse(fs.readFileSync("docs/.vuepress/locales.json"))
BASE_URL = process.env.CODELISTS_BASE_URL || ''
module.exports = {
  locales: locales,
  themeConfig: {
    nav: [{
      text: 'API',
      link: `${BASE_URL}/api/`
    }],
    locales: locales,
    logo: 'https://codeforiati.org/assets/img/logo.png',
    prevLinks: false,
    nextLinks: false
  }
}
