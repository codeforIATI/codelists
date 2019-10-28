var fs = require("fs")
var locales = JSON.parse(fs.readFileSync("docs/.vuepress/locales.json"))
module.exports = {
  locales: locales,
  themeConfig: {
    locales: locales,
    logo: 'https://codeforiati.org/assets/img/logo.png?v=7ddc8d1394de72bd6ae00937b90158393b9bb996'
  }
}

