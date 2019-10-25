// Import libraries
const util = require("util")
const Fs = require("fs")
const Path = require("path")
const fsExtra = require('fs-extra')

console.log('Parsing codelists...');

// Create file to write to

const createWriteStream = function(folder) {
  fsExtra.ensureDirSync(folder)
  return Fs.createWriteStream(`${folder}/README.md`)
}

// Write to file

const createMarkdownFiles = async() => {
  Fs.readFile('docs/.vuepress/public/clv3/codelists.json', 'utf8', function(err, data) {
    if (err) throw err;
    codelists = JSON.parse(data)
    codelists.sort()
    codelists.forEach(codelist => {
      const folderPath = `docs/${codelist}`
      const stream = createWriteStream(folderPath)
      stream.write(`<CodelistPage codelist="${codelist}" lang="en"/>`)
      const folderPathFR = `docs/fr/${codelist}`
      const streamFR = createWriteStream(folderPathFR)
      streamFR.write(`<CodelistPage codelist="${codelist}" lang="fr"/>`)
      addToLocales(codelist, ['fr'])
    })
  })
}

const setup = async() => {
  fsExtra.emptyDirSync("docs/")
  fsExtra.copySync("static/", "docs/")
}

const addToLocales = async(codelistName, langs) => {
  const locales = JSON.parse(Fs.readFileSync("docs/.vuepress/locales.json"))
  locales["/"].sidebar.push([`/${codelistName}/`, codelistName])
  for (var lang of langs) {
    locales[`/${lang}/`].sidebar.push([`/${lang}/${codelistName}/`, codelistName])
  }
  Fs.writeFileSync("docs/.vuepress/locales.json", JSON.stringify(locales))
}

//setup()
createMarkdownFiles()