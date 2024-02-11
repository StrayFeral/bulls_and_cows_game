#!/usr/bin/env bash

fn=""
ext=""
pkg=$1

section=$2

proj=${pkg%_*}
proj=${proj%_*}

man=$proj
man="${man//\-/"_"}"

if [[ -z $pkg ]]
then
    echo "USAGE: makedeb.sh DIRECTORYNAME [SECTION]"
    echo "EXAMPLE: makedeb.sh foo-1.0-1_all 1"
    echo ""
    echo "SECTION: Software section. Example: 6 is 'games'."
    exit 1
fi


echo "MAKING PACKAGE '$pkg'"
echo "================================================================"


# Man page
if [[ ! -z $section ]]
then
    echo "Making man page..."

    fn="$man.$section"
    #ext=${fn##*.}
    ext=$section

    cp "man_pages/$fn" /tmp/
    gzip -n --best "/tmp/$fn"
    sudo mv "/tmp/$fn.gz" "$pkg/usr/share/man/man$ext/"
fi

# Changelog
if [[ -f "changelogs/$pkg.txt" ]]
then
    echo "Changelog found..."
    cp "changelogs/$pkg.txt" "/tmp/changelog.Debian"
    gzip -n --best "/tmp/changelog.Debian"
    sudo mv "/tmp/changelog.Debian.gz" "$pkg/usr/share/doc/$proj/"
fi

echo "Some setup..."
sudo chmod -R 0755 $pkg/usr
sudo chown -R 0:0 $pkg/usr

# Man page
if [[ ! -z $section ]]
then
    sudo chmod -x "$pkg/usr/share/man/man$ext/$fn.gz"
fi

# Changelog
if [[ -f "changelogs/$pkg.txt" ]]
then
    sudo chmod -x "$pkg/usr/share/doc/$proj/changelog.Debian.gz"
fi

sudo chmod -x "$pkg/usr/share/doc/$proj/copyright"

echo "Making the package..."
sudo dpkg-deb --build $pkg

echo "------------------------------------------------[ LINTIAN OUTPUT"

lintian "$pkg.deb"
mv "$pkg.deb" DEBPACKAGES/

echo ""
echo "Done."
