##########linux64
hg clone http://hg.mozilla.org/build/tools tools

python tools/buildfarm/maintenance/purge_builds.py -s 1.0 -n info -n 'rel-*' .. /mock/users/cltbld/home/cltbld/build

wget --progress=dot:mega -N http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1335984981/firefox-15.0a1.en-US.linux-x86_64.tar.bz2

tar -jxvf firefox-15.0a1.en-US.linux-x86_64.tar.bz2

exepath: firefox/firefox-bin

exedir: firefox

symbols_url: http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1335984981/firefox-15.0a1.en-US.linux-x86_64.crashreporter-symbols.zip

wget --progress=dot:mega -N http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1335984981/firefox-15.0a1.en-US.linux-x86_64.tests.zip

python /home/cltbld/talos-slave/test/tools/buildfarm/utils/printbuildrev.py firefox

xset s reset

python reftest/runreftest.py --appname=firefox/firefox-bin --utility-path=bin --extra-profile-file=bin/plugins --symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1335984981/firefox-15.0a1.en-US.linux-x86_64.crashreporter-symbols.zip --extra-profile-file=jsreftest/tests/user.js jsreftest/tests/jstests.list

rm -rf build

python tools/buildfarm/maintenance/count_and_reboot.py -f ../reboot_count.txt -n 1 -z

########################################
#########   MOCHITESTS   ###################
########################################

########################### LINUX32
python mochitest/runtests.py --appname=firefox/firefox-bin --utility-path=bin
--extra-profile-file=bin/plugins --certificate-path=certs --autorun
--close-when-done --console-level=INFO
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux/1336013881/firefox-15.0a1.en-US.linux-i686.crashreporter-symbols.zip
--total-chunks 5 --this-chunk 1 --chunk-by-dir 4

########################### LINUX64
python mochitest/runtests.py --appname=firefox/firefox-bin --utility-path=bin
--extra-profile-file=bin/plugins --certificate-path=certs --autorun
--close-when-done --console-level=INFO
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1336013881/firefox-15.0a1.en-US.linux-x86_64.crashreporter-symbols.zip
--total-chunks 5 --this-chunk 1 --chunk-by-dir 4

########################### Leopard
python mochitest/runtests.py
--appname=./FirefoxNightly.app/Contents/MacOS/firefox-bin --utility-path=bin
--extra-profile-file=bin/plugins --certificate-path=certs --autorun
--close-when-done --console-level=INFO
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-macosx64/1336013881/firefox-15.0a1.en-US.mac.crashreporter-symbols.zip
--total-chunks 5 --this-chunk 1 --chunk-by-dir 4

########################### Snow Leopard
python mochitest/runtests.py
--appname=./FirefoxNightly.app/Contents/MacOS/firefox-bin --utility-path=bin
--extra-profile-file=bin/plugins --certificate-path=certs --autorun
--close-when-done --console-level=INFO
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-macosx64/1336013881/firefox-15.0a1.en-US.mac.crashreporter-symbols.zip
--total-chunks 5 --this-chunk 1 --chunk-by-dir 4

########################### windows32
'python' 'mochitest/runtests.py' '--appname=firefox/firefox.exe'
'--utility-path=bin' '--extra-profile-file=bin/plugins'
'--certificate-path=certs' '--autorun' '--close-when-done'
'--console-level=INFO'
u'--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-win32/1336013881/firefox-15.0a1.en-US.win32.crashreporter-symbols.zip'
'--total-chunks' '5' '--this-chunk' '1' '--chunk-by-dir' '4'

########################### windows64
'python' 'mochitest/runtests.py' '--appname=firefox/firefox.exe'
'--utility-path=bin' '--extra-profile-file=bin/plugins'
'--certificate-path=certs' '--autorun' '--close-when-done'
'--console-level=INFO'
u'--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-win32/1336013881/firefox-15.0a1.en-US.win32.crashreporter-symbols.zip'
'--total-chunks' '5' '--this-chunk' '1' '--chunk-by-dir' '4'

########################################
#########   XPCSHELL ###################
########################################

###########################LINUX64

python /home/cltbld/talos-slave/test/tools/buildfarm/utils/printbuildrev.py
firefox

bash -c 'if [ ! -d firefox/plugins ]; then mkdir firefox/plugins; fi && cp
bin/xpcshell firefox && cp -R bin/components/* firefox/components/ && cp -R
bin/plugins/* firefox/plugins/ && python -u xpcshell/runxpcshelltests.py
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1336062888/firefox-15.0a1.en-US.linux-x86_64.crashreporter-symbols.zip
--manifest=xpcshell/tests/all-test-dirs.list firefox/xpcshell'

########### Win 32
bash -c 'if [ ! -d firefox/plugins ]; then mkdir firefox/plugins; fi && cp
bin/xpcshell firefox && cp -R bin/components/* firefox/components/ && cp -R
bin/plugins/* firefox/plugins/ && python -u xpcshell/runxpcshelltests.py
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux/1336013881/firefox-15.0a1.en-US.linux-i686.crashreporter-symbols.zip
--manifest=xpcshell/tests/all-test-dirs.list firefox/xpcshell'
##################### Windows64
'bash' '-c' u'if [ ! -d firefox/plugins ]; then mkdir firefox/plugins; fi && cp
bin/xpcshell.exe firefox && cp -R bin/components/* firefox/components/ && cp -R
bin/plugins/* firefox/plugins/ && python -u xpcshell/runxpcshelltests.py
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-win32/1336073087/firefox-15.0a1.en-US.win32.crashreporter-symbols.zip
--manifest=xpcshell/tests/all-test-dirs.list firefox/xpcshell.exe'

############# Snow leopard
bash -c 'if [ ! -d ./FirefoxNightly.app/Contents/MacOS/plugins ]; then mkdir
./FirefoxNightly.app/Contents/MacOS/plugins; fi && cp bin/xpcshell
./FirefoxNightly.app/Contents/MacOS && cp -R bin/components/*
./FirefoxNightly.app/Contents/MacOS/components/ && cp -R bin/plugins/*
./FirefoxNightly.app/Contents/MacOS/plugins/ && python -u
xpcshell/runxpcshelltests.py
--symbols-path=http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-macosx64/1336073087/firefox-15.0a1.en-US.mac.crashreporter-symbols.zip
--manifest=xpcshell/tests/all-test-dirs.list
./FirefoxNightly.app/Contents/MacOS/xpcshell'


########## SANITY CHECKS PER OS

### MAC
bash -c 'screenresolution get && screenresolution list && system_profiler
SPDisplaysDataType'

bash ../tools/buildfarm/utils/installdmg.sh firefox-15.0a1.en-US.mac.dmg

