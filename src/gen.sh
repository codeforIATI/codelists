#!/bin/bash

rm -rf codelists
rm -rf docs
cp -r static docs

if [ -d IATI-Codelists-NonEmbedded ]; then
    cd IATI-Codelists-NonEmbedded || exit 1
    git pull
    git checkout master
    cd ..
else
    git clone --branch master https://github.com/codeforIATI/IATI-Codelists-NonEmbedded.git
fi

if [ -d Unofficial-Codelists ]; then
    cd Unofficial-Codelists || exit 1
    git pull
    git checkout master
    cd ..
else
    git clone --branch master https://github.com/codeforIATI/Unofficial-Codelists.git
fi

for v in 2.03 1.05; do
    i=$(echo $v | head -c 1)

    if [ -d IATI-Codelists-$i ]; then
        cd IATI-Codelists-$i || exit 1
        git pull
        git checkout version-$v
        cd ..
    else
        git clone --branch version-$v https://github.com/codeforIATI/IATI-Codelists.git IATI-Codelists-$i
    fi

    echo ' *** Copy source XML to CLv3 ***'
    mkdir -p docs/.vuepress/public/api/$i/clv2/xml docs/.vuepress/public/api/$i/clv3/xml
    cp -r IATI-Codelists-$i/xml/*.xml docs/.vuepress/public/api/$i/clv3/xml
    cp -r IATI-Codelists-NonEmbedded/xml/*.xml docs/.vuepress/public/api/$i/clv3/xml
    cp -r Unofficial-Codelists/xml/*.xml docs/.vuepress/public/api/$i/clv3/xml

    echo ' *** Convert CLv3 XML to CLv2 XML ***'
    for f in docs/.vuepress/public/api/$i/clv3/xml/*; do
        python src/v3tov2.py $f > docs/.vuepress/public/api/$i/clv2/xml/`basename $f`;
    done
    echo ' *** Generate CLv3 other formats (CSV; JSON; XLSX) ***'
    python src/gen.py $i docs/.vuepress/public/api/$i/clv3

    echo ' *** Copy CLv3 other formats (CSV; JSON; XLSX) to CLv2 ***'
    cp -r docs/.vuepress/public/api/$i/clv3/{codelists.json,codelists.xml,csv,json,xlsx} docs/.vuepress/public/api/$i/clv2/

    echo ' *** Convert CLv2 all formats to CLv1 ***'
    python src/v2tov1.py docs/.vuepress/public/api/$i/clv2 docs/.vuepress/public/api/$i/clv1

    echo ' *** Copy Clv3 all formats to root ***'
    cp -r docs/.vuepress/public/api/$i/clv3/* docs/.vuepress/public/api/$i

    python src/gen_api_root.py api/$i docs/.vuepress/public/api/$i
done

echo ' *** Copy v2 all formats to root ***'
cp -r docs/.vuepress/public/api/2/clv* docs/.vuepress/public/api
cp -r docs/.vuepress/public/api/2/clv3/* docs/.vuepress/public/api
python src/gen_api_root.py api docs/.vuepress/public/api
