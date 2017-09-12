developer=http://indiecomputing.com/
url=${developer}
maintainer=http://indiecomputing.com/
pkgname=$(basename $(pwd))
pkgver=0.3
pkgrel=1
pkgdesc="Generate task lists which can be worked down using taliworkdown"
arch=('any')
license=("GPL")
options=('!strip')
depends=('python')

package() {
# Code
    install -D -m755 ${startdir}/taligen.py ${pkgdir}/usr/bin/taligen
}
