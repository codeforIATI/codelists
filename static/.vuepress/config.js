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
    logo: `${BASE_URL}/assets/img/logo.png?v=7ddc8d1394de72bd6ae00937b90158393b9bb996`
  }
}
