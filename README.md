# Replicated codelists interface builder

[![Build Status](https://travis-ci.com/codeforIATI/codelists.svg?branch=master)](https://travis-ci.com/codeforIATI/codelists)

Replicated codelists, useful for those using IATI data.

* A script generates markdown files from the XML codelist files. It scrubs the `docs/` folder and then copies in anything from the `static/` folder, at the start of each run. So, don't make any changes inside the `docs/` folder as they will be lost at the start of each build.
* VuePress then builds a nice front end from the markdown files.

## Installing and running

Clone the repository and then install:
```
pip install -r requirements.txt
yarn install
```

Run:

```
yarn run dev
```

You can also run the commands separately, if you would like to have VuePress refresh each time you rebuild the site:

```
yarn run preprocess
```

and

```
yarn run docs:dev
```

The page should be built based on your XML files in `codelists/`. Note that there are a couple of small changes to the existing XML files:

* adding the name of the codelist in each language
* adding a description in each language (though this is not used yet)

## Thoughts

VuePress is quite nice, and I wanted to try doing everything in JavaScript, but perhaps it does make sense to stick with the existing Python scripts, and then either build with Sphinx, or have a second simple step which builds a VuePress site (which doesn't require any other scripts, as long as you have the config file and markdown files set up. 
