// Import libraries
const util = require("util")
const xml2js = require('xml2js')
const parseString = require('xml2js').parseString
const Fs = require("fs")
const Path = require("path")
const ParseXML = util.promisify(xml2js.parseString)
const fsExtra = require('fs-extra')

console.log('Parsing...');

// Load XML file

const createWriteStream = function(folder) {
  fsExtra.ensureDirSync(folder)
  return Fs.createWriteStream(`${folder}/README.md`)
}

const parseXMLFile = async (src) => {
  const data = Fs.readFileSync(Path.resolve(src))
  if (!(data)) {
    throw new Error(`"${src}" is not found.`)
  }
  const xml = await ParseXML(data.toString())
  return xml
}

// Write to markdown file

const writeCodelists = async(stream, codelist_items, language) => {
  stream.write("\n\nCode | Name | Description\n--- | --- | ---")
  for (var codelist_item of codelist_items) {
    var code = codelist_item.code[0]
    if (language == null) {
      var name = codelist_item.name[0].narrative[0]
      var description = codelist_item.description[0].narrative[0]
    } else {
      var name = codelist_item.name[0].narrative[1] ? codelist_item.name[0].narrative[1]._ : ''
      var description = codelist_item.description[0].narrative[1] ? codelist_item.description[0].narrative[1]._ : ''
    }
    stream.write(`\n${code} | ${name} | ${description}`)
  }
}

// Create markdown file

const createMarkdownFile = async(codelistName) => {
  const xmlData = await parseXMLFile(`codelists/${codelistName}.xml`)
  const codelist_names = xmlData.codelist.metadata[0].name[0].narrative
  for (var codelist_name of codelist_names) {
    if (typeof codelist_name == 'string') {
      const folderPath = `docs/${codelistName}`
      const stream = createWriteStream(folderPath)
      stream.write('# ' + codelist_name)
      writeCodelists(stream, xmlData.codelist["codelist-items"][0]["codelist-item"], null)
    } else {
      const lang = codelist_name.$['xml:lang']
      const folderPath = `docs/${lang}/${codelistName}`
      const stream = createWriteStream(folderPath)
      stream.write('# ' + codelist_name._)
      writeCodelists(stream, xmlData.codelist["codelist-items"][0]["codelist-item"], lang)
    }
  }
  addToLocales(codelistName, ['fr'])
}

const setup = async() => {
  fsExtra.emptyDirSync("docs/")
  fsExtra.copySync("static/", "docs/")
}

const addToLocales = async(codelistName, langs) => {
  const locales = JSON.parse(Fs.readFileSync("docs/.vuepress/locales.json"))
  locales["/"].sidebar.push(`/${codelistName}/`)
  for (var lang of langs) {
    locales[`/${lang}/`].sidebar.push(`/${lang}/${codelistName}/`)
  }
  Fs.writeFileSync("docs/.vuepress/locales.json", JSON.stringify(locales))
}

setup()
createMarkdownFile('Sector')
createMarkdownFile('FinanceType')

