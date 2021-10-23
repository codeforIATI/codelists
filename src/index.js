// Import libraries
const Fs = require('fs')
const fsExtra = require('fs-extra')

console.log('Parsing codelists...')

// Create file to write to

const createWriteStream = function (folder) {
  fsExtra.ensureDirSync(folder)
  return Fs.createWriteStream(`${folder}/README.md`)
}

// Write to file

const createMarkdownFiles = async () => {
  Fs.readFile('docs/.vuepress/public/api/codelists.json', 'utf8', function (err, data) {
    if (err) { throw err }
    var codelists = JSON.parse(data)
    var sidebar = {'/': [], '/fr/': []}
    codelists.forEach(codelistSlug => {
      ['en', 'fr'].forEach(lang => {
        Fs.readFile(`docs/.vuepress/public/api/json/${lang}/${codelistSlug}.json`, 'utf8', function (err, data) {
          if (err) { throw err }
          var codelistData = JSON.parse(data)
          var codelistName = codelistData.metadata.name || codelistSlug
          const path = (lang === 'en') ? '/' : `/${lang}/`
          sidebar[path].push([`${path}${codelistSlug}/`, codelistName])

          if (sidebar[path].length === codelists.length) {
            const locales = JSON.parse(Fs.readFileSync('docs/.vuepress/locales.json'))
            sidebar[path].sort(function (a, b) { return (a[1] > b[1]) ? 1 : -1 })
            locales[path].sidebar = locales[path].sidebar.concat(sidebar[path])
            Fs.writeFileSync('docs/.vuepress/locales.json', JSON.stringify(locales))
          }
          const folderPath = `docs${path}${codelistSlug}`
          const stream = createWriteStream(folderPath)
          stream.write(`---
title: ${codelistName}
---
<CodelistPage codelist="${codelistSlug}" lang="${lang}"/>`)
        })
      })
    })
  })
}

const setup = async () => {
  fsExtra.emptyDirSync('docs/')
  fsExtra.copySync('static/', 'docs/')
}

// setup()
createMarkdownFiles()
