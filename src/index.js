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
  Fs.readFile('docs/.vuepress/public/clv3/codelists.json', 'utf8', function (err, data) {
    if (err) { throw err }
    var codelists = JSON.parse(data)
    codelists.sort()
    codelists.forEach(codelistSlug => {
      ['en', 'fr'].forEach(lang => {
        Fs.readFile(`docs/.vuepress/public/clv3/json/${lang}/${codelistSlug}.json`, 'utf8', function (err, data) {
          if (err) { throw err }
          var codelistData = JSON.parse(data)
          var codelistName = codelistData.metadata.name || codelistSlug
          addToLocales(codelistSlug, codelistName, lang)
          const path = (lang === 'en') ? '/' : `/${lang}/`
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

const addToLocales = async (codelistSlug, codelistName, lang) => {
  const locales = JSON.parse(Fs.readFileSync('docs/.vuepress/locales.json'))
  if (lang === 'en') {
    locales['/'].sidebar.push([`/${codelistSlug}/`, codelistName])
  } else {
    locales[`/${lang}/`].sidebar.push([`/${lang}/${codelistSlug}/`, codelistName])
  }
  Fs.writeFileSync('docs/.vuepress/locales.json', JSON.stringify(locales))
}

// setup()
createMarkdownFiles()
