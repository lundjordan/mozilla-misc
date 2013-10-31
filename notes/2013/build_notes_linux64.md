# Build Steps for building Firefox on linux64
https://tbpl.mozilla.org/php/getParsedLog.php?id=26306880&full=1&branch=mozilla-central

# steps

##### MozillaBuildFactory

### 438         self.addInitialSteps()
========= Started setProps: basedir  => '/builds/slave/m-cen-lx-000000000000'
========= Started setProps: echo hashType => 'sha512'
========= Started clobber: rm -rf '$(basedir)/tools'
========= Started clone: hg clone $(tools_repo) tools => 'http://hg.mozilla.org/build/tools'
========= Started setProps: toolsdir  => '$(basedir)/tools'
 440     def addInitialSteps(self):
 441         self.addStep(SetProperty(
 442             name='set_basedir',
 443             command=['bash', '-c', 'pwd'],
 444             property='basedir',
 445             workdir='.',
 446         ))
 447         self.addStep(SetProperty(
 448             name='set_hashType',
 449             command=['echo', self.hashType],
 450             property='hashType',
 451             workdir='.',
 452         ))
 453         # We need the basename of the current working dir so we can
 454         # ignore that dir when purging builds later.
 455         self.addStep(SetProperty(
 456             name='set_builddir',
 457             command=['bash', '-c', 'basename "$PWD"'],
 458             property='builddir',
 459             workdir='.',
 460         ))
 461         self.addStep(ShellCommand(
 462                      name='rm_buildtools',
 463                      command=['rm', '-rf', 'tools'],
 464                      description=['clobber', 'build tools'],
 465                      haltOnFailure=True,
 466                      log_eval_func=rc_eval_func({0: SUCCESS, None: RETRY}),
 467                      workdir='.'
 468                      ))
 469         self.addStep(MercurialCloneCommand(
 470                      name='clone_buildtools',
 471                      command=['hg', 'clone', self.buildToolsRepo, 'tools'],
 472                      description=['clone', 'build tools'],
 473                      log_eval_func=rc_eval_func({0: SUCCESS, None: RETRY}),
 474                      workdir='.',
 475                      retry=False  # We cannot use retry.py until we have this repo checked out
 476                      ))
 477         self.addStep(SetProperty(
 478             name='set_toolsdir',
 479             command=['bash', '-c', 'pwd'],
 480             property='toolsdir',
 481             workdir='tools',
 482         ))

========= Started checking: python m-cen-lx-000000000000000000000/tools/clobberer/clobberer.py -s tools -t 168 http://clobberer.pvt.build.mozilla.org/index.php mozilla-central 'Linux mozilla-central build' m-cen-lx-000000000000000000000 bld-linux64-ec2-487 http://buildbot-master65.srv.releng.usw2.mozilla.com:8001/

 484         if self.clobberURL is not None:
 485             self.addStep(MozillaClobberer(
 486                          name='checking_clobber_times',
 487                          branch=self.clobberBranch,
 488                          clobber_url=self.clobberURL,
 489                          clobberer_path=WithProperties(
 490                          '%(builddir)s/tools/clobberer/clobberer.py'),
 491                          clobberTime=self.clobberTime
 492                          ))


========= Started setProps: purge_actual purge_target python tools/buildfarm/maintenance/purge_builds.py -s 12 -n info -n 'rel-*:45d' -n 'tb-rel-*:45d' .. /mock/users/cltbld/home/cltbld/build => purge_actual: '167.25GB' purge_target: '12GB'

 494         if self.buildSpace > 0:
 495             command = ['python', 'tools/buildfarm/maintenance/purge_builds.py',
 496                        '-s', str(self.buildSpace)]
 497 
 498             for i in self.ignore_dirs:
 499                 command.extend(["-n", i])
 500 
 501             # These are the base_dirs that get passed to purge_builds.py.
 502             # The mock dir is only present on linux slaves, but since
 503             # not all classes that inherit from MozillaBuildFactory provide
 504             # a platform property we can use for limiting the base_dirs, it
 505             # is easier to include mock by default and simply have
 506             # purge_builds.py skip the dir when it isn't present.
 507             command.extend(["..", "/mock/users/cltbld/home/cltbld/build"])
 508 
 509             def parse_purge_builds(rc, stdout, stderr):
 510                 properties = {}
 511                 for stream in (stdout, stderr):
 512                     m = re.search('unable to free (?P<size>[.\d]+) (?P<unit>\w+) ', stream, re.M)
 513                     if m:
 514                         properties['purge_target'] = '%s%s' % (
 515                             m.group('size'), m.group('unit'))
 516                     m = None
 517                     m = re.search('space only (?P<size>[.\d]+) (?P<unit>\w+)',
 518                                   stream, re.M)
 519                     if m:
 520                         properties['purge_actual'] = '%s%s' % (
 521                             m.group('size'), m.group('unit'))
 522                     m = None
 523                     m = re.search('(?P<size>[.\d]+) (?P<unit>\w+) of space available', stream, re.M)
 524                     if m:
 525                         properties['purge_actual'] = '%s%s' % (
 526                             m.group('size'), m.group('unit'))
 527                 if 'purge_target' not in properties:
 528                     properties['purge_target'] = '%sGB' % str(self.buildSpace)
 529                 return properties
 530 
 531             self.addStep(SetProperty(
 532                          name='clean_old_builds',
 533                          command=command,
 534                          description=['cleaning', 'old', 'builds'],
 535                          descriptionDone=['clean', 'old', 'builds'],
 536                          haltOnFailure=True,
 537                          workdir='.',
 538                          timeout=3600,  # One hour, because Windows is slow
 539                          extract_fn=parse_purge_builds,
 540                          log_eval_func=lambda c, s: regex_log_evaluator(
 541                          c, s, purge_error),
 542                          env=self.env,
 543                          ))


========= Started mock-tgt: sh -c 'rm -f /builds/mock_mozilla/mozilla-centos6-x86_64/buildroot.lock; mock_mozilla -r mozilla-centos6-x86_64 --orphanskill'
========= Started mock-tgt: mock_mozilla -r mozilla-centos6-x86_64 --init
545         if self.use_mock:
546             self.addStep(MockReset(
547                 target=self.mock_target,
548             ))
    def __init__(self, target, **kwargs):
        kwargs['command'] = "sh -c " \
            "'rm -f /builds/mock_mozilla/%s/buildroot.lock; " \
            "mock_mozilla -r %s --orphanskill'" % (target, target)
        assert target is not None, "target is required"
        self.super_class = ShellCommand
        self.super_class.__init__(self, **kwargs)
        self.target = target
        self.description = ['mock-tgt', target]
        self.addFactoryArguments(target=target)
549             self.addStep(MockInit(
550                 target=self.mock_target,
551             ))
552             self.addMockSteps()



========= Started mock_mozilla: mock_mozilla -r mozilla-centos6-x86_64 --copyin /home/cltbld/.ssh /home/mock_mozilla/.ssh
========= Started mock_mozilla: mock_mozilla -r mozilla-centos6-x86_64 --cwd / --shell '/usr/bin/env  chown -R mock_mozilla /home/mock_mozilla/.ssh'

 339     def addMockSteps(self):
 340         # do not add the steps more than once per instance
 341         if (hasattr(self, '_MockMixin_added_mock_steps')):
 342             return
 343         self._MockMixin_added_mock_steps = 1
 344 
 345         if self.mock_copyin_files:
 346             for source, target in self.mock_copyin_files:
 347                 self.addStep(ShellCommand(
 348                     name='mock_copyin_%s' % source.replace('/', '_'),
 349                     command=['mock_mozilla', '-r', self.mock_target,
 350                              '--copyin', source, target],
 351                     haltOnFailure=True,
 352                 ))
 353                 self.addStep(MockCommand(
 354                     name='mock_chown_%s' % target.replace('/', '_'),
 355                     command='chown -R mock_mozilla %s' % target,
 356                     target=self.mock_target,
 357                     mock=True,
 358                     workdir='/',
 359                     mock_args=[],
 360                     mock_workdir_prefix=None,
 361                 ))

========= Started mock_mozilla: mock_mozilla -r mozilla-centos6-x86_64 --cwd / --unpriv --shell '/usr/bin/env  mkdir -p /builds/slave/m-cen-lx-000000000000000000000/build'

 362         # This is needed for the builds to start
 363         self.addStep(MockCommand(
 364             name='mock_mkdir_basedir',
 365             command=WithProperties(
 366                 "mkdir -p %(basedir)s" + "/%s" % self.baseWorkDir),
 367             target=self.mock_target,
 368             mock=True,
 369             workdir='/',
 370             mock_workdir_prefix=None,
 371         ))


========= Started mock_mozilla -r mozilla-centos6-x86_64 --install autoconf213 python zip mozilla-python27-mercurial git ccache glibc-static libstdc++-static perl-Test-Simple perl-Config-General gtk2-devel libnotify-devel yasm alsa-lib-devel libcurl-devel wireless-tools-devel libX11-devel libXt-devel mesa-libGL-devel gnome-vfs2-devel GConf2-devel wget mpfr xorg-x11-font* imake gcc45_0moz3 gcc454_0moz1 gcc472_0moz1 gcc473_0moz1 yasm ccache valgrind pulseaudio-libs-devel gstreamer-devel gstreamer-plugins-base-devel freetype-2.3.11-6.el6_1.8.x86_64 freetype-devel-2.3.11-6.el6_1.8.x86_64 
    in build dir

 372         if self.use_mock and self.mock_packages:
 373             self.addStep(MockInstall(
 374                 target=self.mock_target,
 375                 packages=self.mock_packages,
 376             ))

##### 

========= Started set_buildids (results: 0, elapsed: 0 secs) (at 2013-08-08 04:42:51.976331) =========
not sure if i need this line 814
========= Finished set_

========= Started 'ccache -z'
     in dir /builds/slave/m-cen-l64-00000000000000000000/build
1004         if self.enable_ccache:
1005             self.addStep(ShellCommand(command=['ccache', '-z'],
1006                                       name="clear_ccache_stats", warnOnFailure=False,
1007                                       flunkOnFailure=False, haltOnFailure=False, env=self.env))

 ========= Started remove mozharness
    rm -rf mozharness
     in dir /builds/slave/m-cen-l64-00000000000000000000/
  ========= Started checkout mozharness
    python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py -s 1 -r 5 -t 1260 hg clone http://hg.mozilla.org/build/mozharness mozharness
     in dir /builds/slave/m-cen-l64-00000000000000000000/
  ========= Started updating mozharness to production
    hg update -r production
     in dir /builds/slave/m-cen-l64-00000000000000000000/mozharness '

1008         if mozharnessRepoPath:
1009             assert mozharnessRepoPath and mozharnessTag
1010             self.mozharnessRepoPath = mozharnessRepoPath
1011             self.mozharnessTag = mozharnessTag
1012             self.addMozharnessRepoSteps()

1064     def addMozharnessRepoSteps(self):
1065         self.addStep(ShellCommand(
1066             name='rm_mozharness',
1067             command=['rm', '-rf', 'mozharness'],
1068             description=['removing', 'mozharness'],
1069             descriptionDone=['remove', 'mozharness'],
1070             haltOnFailure=True,
1071             workdir='.',
1072         ))
1073         self.addStep(MercurialCloneCommand(
1074             name='hg_clone_mozharness',
1075             command=['hg', 'clone', self.getRepository(
1076                 self.mozharnessRepoPath), 'mozharness'],
1077             description=['checking', 'out', 'mozharness'],
1078             descriptionDone=['checkout', 'mozharness'],
1079             haltOnFailure=True,
1080             workdir='.',
1081         ))
1082         self.addStep(ShellCommand(
1083             name='hg_update_mozharness',
1084             command=['hg', 'update', '-r', self.mozharnessTag],
1085             description=['updating', 'mozharness', 'to', self.mozharnessTag],
1086             workdir='mozharness',
1087             haltOnFailure=True
1088         ))





### now lets:
1137     def addBuildSteps(self):
1138         self.addPreBuildSteps()
1139         self.addSourceSteps()
1140         self.addConfigSteps()
1141         self.addDoBuildSteps()
1142         if self.signingServers and self.enableSigning:
1143             self.addGetTokenSteps()
1144         if self.doBuildAnalysis:
1145             self.addBuildAnalysisSteps()
1146         if self.doPostLinkerSize: # XXX TODO I dont think this is hit
1147             self.addPostLinkerSizeSteps()

1.   ========= Started delete old package
    rm -rf obj-firefox/dist/firefox-* obj-firefox/dist/fennec* obj-firefox/dist/seamonkey* obj-firefox/dist/thunderbird* obj-firefox/dist/install/sea/*.exe 
     in dir /builds/slave/m-cen-l64-00000000000000000000/build

1149     def addPreBuildSteps(self):
1150         if self.nightly:
1151             self.addStep(ShellCommand(
1152                          name='rm_builddir',
1153                          command=['rm', '-rf', 'build'],
1154                          env=self.env,
1155                          workdir='.',
1156                          timeout=60 * 60  # 1 hour
1157                          ))
1158         pkg_patterns = []
1159         for product in ('firefox-', 'fennec', 'seamonkey', 'thunderbird'):
1160             pkg_patterns.append('%s/dist/%s*' % (self.mozillaObjdir,
1161                                                  product))
1162            
1163         self.addStep(ShellCommand(
1164                      name='rm_old_pkg',
1165                      command="rm -rf %s %s/dist/install/sea/*.exe " %
1166                     (' '.join(pkg_patterns), self.mozillaObjdir),
1167                      env=self.env,
1168                      description=['deleting', 'old', 'package'],
1169                      descriptionDone=['delete', 'old', 'package']
1170                      ))
1171         if self.nightly:
1172             self.addStep(ShellCommand(
1173                          name='rm_old_symbols',
1174                          command="find 20* -maxdepth 2 -mtime +7 -exec rm -rf {} \;",
1175                          env=self.env,
1176                          workdir='.',
1177                          description=['cleanup', 'old', 'symbols'],
1178                          flunkOnFailure=False
1179                          ))



1.  ========= Started downloading to buildprops.json
    # no output
1.  ========= Started 'python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py ...'
    python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py -s 1 -r 5 -t 3660 python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/hgtool.py --mirror http://hg-internal.dmz.scl3.mozilla.com/mozilla-central --bundle http://ftp.mozilla.org/pub/mozilla.org/firefox/bundles/mozilla-central.hg http://hg.mozilla.org/mozilla-central build
     in dir /builds/slave/m-cen-l64-00000000000000000000/. (timeout 3720 secs)
1.  ========= Started set props: got_revision
    hg parent '--template={node}'
     in dir /builds/slave/m-cen-l64-00000000000000000000/build
1.  ========= Started set props: comments
comments: merge b2g-inbound to mozilla-central

GOT TO HERE!

1239     def addSourceSteps(self):
1240         if self.useSharedCheckouts:
1241             self.addStep(JSONPropertiesDownload(
1242                 name="download_props",
1243                 slavedest="buildprops.json",
1244                 workdir='.'
1245             ))
1246        
1247             self.addStep(self.makeHgtoolStep(wc='build', workdir='.'))
             684     def makeHgtoolStep(self, name='hg_update', repo_url=None, wc=None,
             685                        mirrors=None, bundles=None, env=None,
             686                        clone_by_revision=False, rev=None, workdir='build',
             687                        use_properties=True, locks=None, autoPurge=False):
             688 
             689         if not env:
             690             env = self.env
             691 
             692         if use_properties:
             693             env = env.copy()
             694             env['PROPERTIES_FILE'] = 'buildprops.json'
             695 
             696         cmd = ['python', WithProperties(
             697             "%(toolsdir)s/buildfarm/utils/hgtool.py")]
             698 
             699         if clone_by_revision:
             700             cmd.append('--clone-by-revision')
             701 
             702         if mirrors is None and self.baseMirrorUrls:
             703             mirrors = ["%s/%s" % (url, self.repoPath)
             704                        for url in self.baseMirrorUrls]
             705 
             706         if mirrors:
             707             for mirror in mirrors:
             708                 cmd.extend(["--mirror", mirror])
             709 
             710         if bundles is None and self.baseBundleUrls:
             711             bundles = ["%s/%s.hg" % (url, self.getRepoName(
             712                 self.repository)) for url in self.baseBundleUrls]
             713 
             714         if bundles:
             715             for bundle in bundles:
             716                 cmd.extend(["--bundle", bundle])
             717 
             718         if not repo_url:
             719             repo_url = self.repository
             720 
             721         if rev:
             722             cmd.extend(["--rev", rev])
             723 
             724         cmd.append(repo_url)
             725 
             726         if wc:
             727             cmd.append(wc)
             728 
             729         if locks is None:
             730             locks = []
             731 
             732         if autoPurge:
             733             cmd.append('--purge')
             734 
             735         return RetryingShellCommand(
             736             name=name,
             737             command=cmd,
             738             timeout=60 * 60,
             739             env=env,
             740             workdir=workdir,
             741             haltOnFailure=True,
             742             flunkOnFailure=True,
             743             locks=locks,
             744         )

1248        
1249             self.addStep(SetProperty(
1250                 name='set_got_revision',
1251                 command=['hg', 'parent', '--template={node}'],
1252                 extract_fn=short_hash
1253             ))
1254         else:           
1255             self.addStep(Mercurial(
1256                          name='hg_update',
1257                          mode='update',
1258                          baseURL='http://%s/' % self.hgHost,
1259                          defaultBranch=self.repoPath,
1260                          timeout=60 * 60,  # 1 hour
1261                          ))
1262            
1263         if self.buildRevision:                  
1264             self.addStep(ShellCommand(
1265                          name='hg_update',
1266                          command=['hg', 'up', '-C', '-r', self.buildRevision],
1267                          haltOnFailure=True
1268                          ))
1269             self.addStep(SetProperty(
1270                          name='set_got_revision',
1271                          command=['hg', 'identify', '-i'],
1272                          property='got_revision'
1273                          ))
1274            
1275         if self.gaiaRepo:
1276             self.addGaiaSourceSteps()
1277         self.addStep(SetBuildProperty(
1278             name='set_comments',
1279             property_name="comments",
1280             value=lambda build: build.source.changes[-
1281                                                      1].comments if len(
1282                                                          build.source.changes) > 0 else "",
1283         ))





========= Started got mozconfig
python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py -s 1 -r 5 -t 1260 bash -c 'if [ -f "browser/config/mozconfigs/linux64/nightly" ]; then                        echo Using in-tree mozconfig;                        cp browser/config/mozconfigs/linux64/nightly .mozconfig;                    else                        echo Downloading mozconfig;                        wget -O .mozconfig http://hg.mozilla.org/build/buildbot-configs/raw-file/production/mozilla2/linux64/mozilla-central/nightly/mozconfig;                    fi'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build
========= Started 'cat .mozconfig'
cat .mozconfig
 in dir /builds/slave/m-cen-l64-00000000000000000000/build

========= Started '/builds/slave/m-cen-l64-00000000000000000000/tools/scripts/tooltool/fetch_and_unpack.sh browser/config/tooltool-manifests/linux64/releng.manifest ...'
/builds/slave/m-cen-l64-00000000000000000000/tools/scripts/tooltool/fetch_and_unpack.sh browser/config/tooltool-manifests/linux64/releng.manifest http://runtime-binaries.pvt.build.mozilla.org/tooltool /tools/tooltool.py setup.sh
 in dir /builds/slave/m-cen-l64-00000000000000000000/build ' '

1285     def addConfigSteps(self):
1286         assert self.configRepoPath is not None
1287         assert self.configSubDir is not None
1288         assert self.mozconfig is not None
1289            
1290         configRepo = self.getRepository(self.configRepoPath)
1291         hg_mozconfig = '%s/raw-file/%s/%s/%s/mozconfig' % (
1292             configRepo, self.mozconfigBranch, self.configSubDir, self.mozconfig)
1293         if self.srcMozconfig:  
1294             cmd = ['bash', '-c',
1295                    '''if [ -f "%(src_mozconfig)s" ]; then
1296                         echo Using in-tree mozconfig;
1297                         cp %(src_mozconfig)s .mozconfig;
1298                     else
1299                         echo Downloading mozconfig;
1300                         wget -O .mozconfig %(hg_mozconfig)s;
1301                     fi'''.replace("\n", "") % {'src_mozconfig': self.srcMozconfig, 'hg_mozconfig': hg_mozconfig}]
1302         else:
1303             cmd = ['wget', '-O', '.mozconfig', hg_mozconfig]
1304            
1305         self.addStep(RetryingShellCommand(
1306             name='get_mozconfig',
1307             command=cmd,
1308             description=['getting', 'mozconfig'],
1309             descriptionDone=['got', 'mozconfig'],
1310             haltOnFailure=True
1311         ))
1312         self.addStep(ShellCommand(
1313                      name='cat_mozconfig',
1314                      command=['cat', '.mozconfig'],
1315                      ))
1316         if self.tooltool_manifest_src:
1317             self.addStep(ShellCommand(
1318                 name='run_tooltool',
1319                 command=[
1320                     WithProperties(
1321                         '%(toolsdir)s/scripts/tooltool/fetch_and_unpack.sh'),
1322                     self.tooltool_manifest_src,
1323                     self.tooltool_url_list[0],
1324                     self.tooltool_script,
1325                     self.tooltool_bootstrap
1326                 ],
1327                 haltOnFailure=True,
1328             ))          




========= Started compile (results: 0, elapsed: 1 hrs, 10 mins, 17 secs) (at 2013-08-08 04:44:54.182430) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" LC_ALL="C" CCACHE_COMPRESS="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" MOZ_SIGN_CMD="python /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/signtool.py --cachedir /builds/slave/m-cen-l64-00000000000000000000/signing_cache -t /builds/slave/m-cen-l64-00000000000000000000/token -n /builds/slave/m-cen-l64-00000000000000000000/nonce -c /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/host.cert -H signing4.srv.releng.scl3.mozilla.com:9110 -H signing5.srv.releng.scl3.mozilla.com:9110 -H signing6.srv.releng.scl3.mozilla.com:9110" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" MOZ_CRASHREPORTER_NO_REPORT="1" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make -f client.mk build '"'"'MOZ_BUILD_DATE=20130808043413'"'"''
 in dir /builds/slave/m-cen-l64-00000000000000000000/build

1330     def addDoBuildSteps(self):
1331         workdir = WithProperties('%(basedir)s/build')
1332         if self.platform.startswith('win'):
1333             workdir = "build"
1334         command = self.makeCmd + ['-f', 'client.mk', 'build',
1335                                   WithProperties('MOZ_BUILD_DATE=%(buildid:-)s')]
1336 
1337         if self.profiledBuild:
1338             command.append('MOZ_PGO=1')
1339         self.addStep(MockCommand(
1340                      name='compile',
1341                      command=command,
1342                      description=['compile'],
1343                      env=self.env,
1344                      haltOnFailure=True,
1345                      timeout=2 * 3600,  # max of 2 hours without output before killing
1346                      maxTime=int(4.5 * 3600),  # max of 4.5 hours total runtime before killing
1347                      mock=self.use_mock,
1348                      target=self.mock_target,
1349                      workdir=workdir,
1350                      mock_workdir_prefix=None,
1351                      ))


========= Started remove old nonce
rm -f nonce
 in dir /builds/slave/m-cen-l64-00000000000000000000/
========= Started downloading to token (results: 0, elapsed: 0 secs) (at 2013-08-08 05:55:11.621185) =========
Slave: bld-linux64-ec2-395
IP: 10.132.52.115
Duration: 21600
URI: https://signing4.srv.releng.scl3.mozilla.com:9110/token
========= Finished downloading to token (results: 0, elapsed: 0 secs) (at 2013-08-08 05:55:11.805300) =========

 746     def addGetTokenSteps(self):
 747         token = "token"
 748         nonce = "nonce"
 749         self.addStep(ShellCommand(
 750             command=['rm', '-f', nonce],
 751             workdir='.',
 752             name='rm_nonce',
 753             description=['remove', 'old', 'nonce'],
 754         ))
 755         self.addStep(SigningServerAuthenication(
 756             servers=self.signingServers,
 757             server_cert=SIGNING_SERVER_CERT,
 758             slavedest=token,
 759             workdir='.',
 760             name='download_token',
 761         ))


========= Started set props: testresults num_ctors
python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/count_ctors.py obj-firefox/dist/bin/libxul.so
 in dir /builds/slave/m-cen-l64-00000000000000000000/build

1380     def addBuildAnalysisSteps(self):
1381         if self.platform in ('linux', 'linux64'):
1382             # Analyze the number of ctors
1383             def get_ctors(rc, stdout, stderr):
1384                 try:
1385                     output = stdout.split("\t")
1386                     num_ctors = int(output[0])
1387                     testresults = [(
1388                         'num_ctors', 'num_ctors', num_ctors, str(num_ctors))]
1389                     return dict(num_ctors=num_ctors, testresults=testresults)
1390                 except:
1391                     return {'testresults': []}
1392 
1393             self.addStep(SetProperty(
1394                 name='get_ctors',
1395                 command=['python', WithProperties('%(toolsdir)s/buildfarm/utils/count_ctors.py'),
1396                          '%s/dist/bin/libxul.so' % self.mozillaObjdir],
1397                 extract_fn=get_ctors,
1398             ))
1399 
1400             if self.graphServer: # yes we use graphServer
                    ###### THIS ALL HAPPENS IN BELOW STEPS
1401                 self.addBuildInfoSteps()
1402                 self.addStep(
1403                     JSONPropertiesDownload(slavedest="properties.json"))
1404                 gs_env = self.env.copy()
1405                 gs_env['PYTHONPATH'] = WithProperties(
1406                     '%(toolsdir)s/lib/python')
1407                 self.addStep(GraphServerPost(server=self.graphServer,
1408                                              selector=self.graphSelector,
1409                                              branch=self.graphBranch,
1410                                              resultsname=self.baseName,
1411                                              env=gs_env,
1412                                              flunkOnFailure=False,
1413                                              haltOnFailure=False,
1414                                              propertiesFile="properties.json"))
1415             else:
1416                 self.addStep(OutputStep(
1417                     name='tinderboxprint_ctors',
1418                     data=WithProperties(
1419                         'TinderboxPrint: num_ctors: %(num_ctors:-unknown)s'),
1420                 ))

1422     def addPostLinkerSizeSteps(self): # XXX TODO not hit
1423         # Analyze the linker max vsize
1424         def get_linker_vsize(rc, stdout, stderr):
1425             try:
1426                 vsize = int(stdout)
1427                 testresults = [ ('libxul_link', 'libxul_link', vsize, str(vsize)) ]
1428                 return dict(vsize=vsize, testresults=testresults)
1429             except:
1430                 return {'testresults': []}
1431 
1432         self.addStep(SetProperty(
1433             name='get_linker_vsize',
1434             command=['cat', '%s\\toolkit\\library\\linker-vsize' % self.mozillaObjdir],
1435             extract_fn=get_linker_vsize,
1436             ))
1437         self.addBuildInfoSteps()



========= Started set props: buildid (results: 0, elapsed: 0 secs) (at 2013-08-08 05:55:12.283915) =========
python build/config/printconfigsetting.py build/obj-firefox/dist/bin/application.ini App BuildID
 in dir /builds/slave/m-cen-l64-00000000000000000000/
========= Started set props: sourcestamp (results: 0, elapsed: 0 secs) (at 2013-08-08 05:55:12.411652) =========
python build/config/printconfigsetting.py build/obj-firefox/dist/bin/application.ini App SourceStamp
 in dir /builds/slave/m-cen-l64-00000000000000000000/


1353     def addBuildInfoSteps(self):
1354         """Helper function for getting build information into properties.
1355         Looks for self._gotBuildInfo to make sure we only run this set of steps
1356         once."""
1357         if not getattr(self, '_gotBuildInfo', False):
1358             self.addStep(SetProperty(
1359                 command=[
1360                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1361                 'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1362                 'App', 'BuildID'],
1363                 property='buildid',
1364                 workdir='.',
1365                 description=['getting', 'buildid'],
1366                 descriptionDone=['got', 'buildid'],
1367             ))
1368             self.addStep(SetProperty(
1369                 command=[
1370                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1371                 'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1372                 'App', 'SourceStamp'],
1373                 property='sourcestamp',
1374                 workdir='.',
1375                 description=['getting', 'sourcestamp'],
1376                 descriptionDone=['got', 'sourcestamp']
1377             ))
1378             self._gotBuildInfo = True



======== Started downloading to properties.json (results: 0, elapsed: 0 secs) (at 2013-08-08 05:55:12.475367) =========
========= Finished downloading to properties.json (results: 0, elapsed: 0 secs) (at 2013-08-08 05:55:12.491835) =========
========= Started graph server post results complete (results: 0, elapsed: 0 secs) (at 2013-08-08 05:55:12.492270) =========
python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py -s 5 -t 120 -r 8 python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/graph_server_post.py --server graphs.mozilla.org --selector /server/collect.cgi --branch Firefox --buildid 20130808043413 --sourcestamp 264e54846d4a --resultsname Linux_x86-64_mozilla-central --properties-file properties.json --timestamp 1375961946
 in dir /builds/slave/m-cen-l64-00000000000000000000/build

1402                 self.addStep(
1403                     JSONPropertiesDownload(slavedest="properties.json"))
1404                 gs_env = self.env.copy()
1405                 gs_env['PYTHONPATH'] = WithProperties(
1406                     '%(toolsdir)s/lib/python')
1407                 self.addStep(GraphServerPost(server=self.graphServer,
1408                                              selector=self.graphSelector,
1409                                              branch=self.graphBranch,
1410                                              resultsname=self.baseName,
1411                                              env=gs_env,
1412                                              flunkOnFailure=False,
1413                                              haltOnFailure=False,
1414                                              propertiesFile="properties.json"))
1415             else:
1416                 self.addStep(OutputStep(
1417                     name='tinderboxprint_ctors',
1418                     data=WithProperties(
1419                         'TinderboxPrint: num_ctors: %(num_ctors:-unknown)s'),
1420                 ))


# now lets:
1035         if self.uploadSymbols or (not self.disableSymbols and self.packageTests):
1036             self.addBuildSymbolsStep()
1037         if self.uploadSymbols: # I don't think this is done
1038             self.addUploadSymbolsStep()
            # XXX TODO I think enablePackaging is always true ?
1039         if self.enablePackaging or self.uploadPackages:
1040             self.addPackageSteps()
1041         if self.uploadPackages:
1042             self.addUploadSteps()
1043         if self.testPrettyNames:
1044             self.addTestPrettyNamesSteps()
1045         if self.l10nCheckTest:
1046             self.addL10nCheckTestSteps()
1047         if self.checkTest:
1048             self.addCheckTestSteps()
1049         if self.valgrindCheck: # XXX TODO not hit
1050             self.addValgrindCheckSteps()
1051         if self.createSnippet: # XXX TODO not hit
1052             self.addUpdateSteps()
1053         if self.triggerBuilds: # XXX TODO not hit
1054             self.addTriggeredBuildsSteps()
1055         if self.doCleanup: # XXX TODO not hit
1056             self.addPostBuildCleanupSteps()
1057         if self.enable_ccache:
1058             self.addStep(ShellCommand(command=['ccache', '-s'],
1059                                       name="print_ccache_stats", warnOnFailure=False,
1060                                       flunkOnFailure=False, haltOnFailure=False, env=self.env))
1061         if self.buildsBeforeReboot and self.buildsBeforeReboot > 0:
1062             self.addPeriodicRebootSteps()

========= Started 'mock_mozilla -r ...' (results: 0, elapsed: 8 mins, 32 secs) (at 2013-08-08 05:55:13.296771) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" LC_ALL="C" CCACHE_COMPRESS="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" MOZ_SIGN_CMD="python /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/signtool.py --cachedir /builds/slave/m-cen-l64-00000000000000000000/signing_cache -t /builds/slave/m-cen-l64-00000000000000000000/token -n /builds/slave/m-cen-l64-00000000000000000000/nonce -c /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/host.cert -H signing4.srv.releng.scl3.mozilla.com:9110 -H signing5.srv.releng.scl3.mozilla.com:9110 -H signing6.srv.releng.scl3.mozilla.com:9110" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" MOZ_CRASHREPORTER_NO_REPORT="1" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make buildsymbols'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox

1838     def addBuildSymbolsStep(self):
1839         objdir = WithProperties('%(basedir)s/build/' + self.objdir)
1840         if self.platform.startswith('win'):
1841             objdir = 'build/%s' % self.objdir
1842         self.addStep(MockCommand(
1843                      name='make_buildsymbols',
1844                      command=self.makeCmd + ['buildsymbols'],
1845                      env=self.env,
1846                      workdir=objdir,
1847                      mock=self.use_mock,
1848                      target=self.mock_target,
1849                      mock_workdir_prefix=None,
1850                      haltOnFailure=True,
1851                      timeout=60 * 60,
1852                      ))



========= Started 'mock_mozilla -r ...' (results: 0, elapsed: 1 mins, 35 secs) (at 2013-08-08 06:03:45.579776) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" MOZ_SIGN_CMD="python /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/signtool.py --cachedir /builds/slave/m-cen-l64-00000000000000000000/signing_cache -t /builds/slave/m-cen-l64-00000000000000000000/token -n /builds/slave/m-cen-l64-00000000000000000000/nonce -c /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/host.cert -H signing4.srv.releng.scl3.mozilla.com:9110 -H signing5.srv.releng.scl3.mozilla.com:9110 -H signing6.srv.releng.scl3.mozilla.com:9110" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" CCACHE_COMPRESS="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" LC_ALL="C" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make package-tests'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox
========= Started 'mock_mozilla -r ...' (results: 0, elapsed: 1 mins, 25 secs) (at 2013-08-08 06:05:20.855951) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" MOZ_SIGN_CMD="python /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/signtool.py --cachedir /builds/slave/m-cen-l64-00000000000000000000/signing_cache -t /builds/slave/m-cen-l64-00000000000000000000/token -n /builds/slave/m-cen-l64-00000000000000000000/nonce -c /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/host.cert -H signing4.srv.releng.scl3.mozilla.com:9110 -H signing5.srv.releng.scl3.mozilla.com:9110 -H signing6.srv.releng.scl3.mozilla.com:9110" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" CCACHE_COMPRESS="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" LC_ALL="C" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make package'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox (timeout 1200 secs)

1578     def addPackageSteps(self, pkgArgs=None, pkgTestArgs=None):
1579         pkgArgs = pkgArgs or []
1580         pkgTestArgs = pkgTestArgs or []
1581            
1582         if self.env:
1583             pkg_env = self.env.copy()
1584         else:
1585             pkg_env = {}
1586            
1587         objdir = WithProperties('%(basedir)s/build/' + self.objdir)
1588         if self.platform.startswith('win'):   
1589             objdir = "build/%s" % self.objdir 
1590         workdir = WithProperties('%(basedir)s/build')
1591         if self.platform.startswith('win'):
1592             workdir = "build/"
1593         if 'rpm' in self.platform_variation: # XXX TODO SUPPORT THIS
1594             pkgArgs.append("MOZ_PKG_FORMAT=RPM")
1595         if self.packageSDK: # XXX TODO I DON'T THINK THIS IS HIT!
1596             self.addStep(MockCommand(
1597                          name='make_sdk',
1598                          command=self.makeCmd + ['-f', 'client.mk', 'sdk'],
1599                          env=pkg_env,
1600                          workdir=workdir,
1601                          mock=self.use_mock,
1602                          target=self.mock_target,
1603                          haltOnFailure=True,
1604                          mock_workdir_prefix=None,
1605                          ))
1606         if self.packageTests:
1607             self.addStep(MockCommand(
1608                          name='make_pkg_tests',
1609                          command=self.makeCmd + [
1610                              'package-tests'] + pkgTestArgs,
1611                          env=pkg_env,
1612                          workdir=objdir,
1613                          mock=self.use_mock,
1614                          target=self.mock_target,
1615                          mock_workdir_prefix=None,
1616                          haltOnFailure=True,
1617                          ))
1618         self.addStep(MockCommand(
1619             name='make_pkg',
1620             command=self.makeCmd + ['package'] + pkgArgs,
1621             env=pkg_env,
1622             workdir=objdir,
1623             mock=self.use_mock,
1624             target=self.mock_target,
1625             mock_workdir_prefix=None,
1626             haltOnFailure=True,      
1627         )) 


========= Started find filepath (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:46.461196) =========
bash -c 'find build/obj-firefox/dist -maxdepth 1 -type f -name *.linux-x86_64*.tar.bz2'
 in dir /builds/slave/m-cen-l64-00000000000000000000/

1629         # Get package details
1630         self.packageFilename = self.getPackageFilename(self.platform,
1631                                                        self.platform_variation)
1632         if self.packageFilename and 'rpm' not in self.platform_variation and self.productName not in ('xulrunner', 'b2g'):
1633             self.addFilePropertiesSteps(filename=self.packageFilename,
1634                                         directory='build/%s/dist' % self.mozillaObjdir,
1635                                         fileType='package',
1636                                         haltOnFailure=True)

 631     def addFilePropertiesSteps(self, filename, directory, fileType,
 632                                doStepIf=True, maxDepth=1, haltOnFailure=False):
 633         self.addStep(FindFile(
 634             name='find_filepath',
 635             description=['find', 'filepath'],
 636             doStepIf=doStepIf,
 637             filename=filename,
 638             directory=directory,
 639             filetype='file',
 640             max_depth=maxDepth,
 641             property_name='filepath',
 642             workdir='.',
 643             haltOnFailure=haltOnFailure
 644         )) 

 # XXX TODO
1637         # Windows special cases
1638         if self.enableInstaller and self.productName != 'xulrunner':
1639             self.addStep(ShellCommand(
1640                 name='make_installer',
1641                 command=self.makeCmd + ['installer'] + pkgArgs,
1642                 env=pkg_env,
1643                 workdir='build/%s' % self.objdir,
1644                 haltOnFailure=True
1645             ))
1646             self.addFilePropertiesSteps(filename='*.installer.exe',
1647                                         directory='build/%s/dist/install/sea' % self.mozillaObjdir,
1648                                         fileType='installer',
1649                                         haltOnFailure=True)
1650 
1651         if self.productName == 'xulrunner':
1652             self.addStep(SetProperty(
1653                 command=[
1654                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1655                          'build/%s/dist/bin/platform.ini' % self.mozillaObjdir,
1656                          'Build', 'BuildID'],
1657                 property='buildid',
1658                 workdir='.',
1659                 name='get_build_id',
1660             ))
1661         else:
1662             self.addStep(SetProperty(
1663                 command=[
1664                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1665                          'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1666                          'App', 'BuildID'],
1667                 property='buildid',
1668                 workdir='.',
1669                 name='get_build_id',
1670             ))
1671             self.addStep(SetProperty(
1672                 command=[
1673                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1674                          'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1675                          'App', 'Version'],
1676                 property='appVersion',
1677                 workdir='.',
1678                 name='get_app_version',
1679             ))
1680             self.addStep(SetProperty(
1681                 command=[
1682                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1683                          'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1684                          'App', 'Name'],
1685                 property='appName',
1686                 workdir='.',
1687                 name='get_app_name',
1688             ))
1689         self.pkg_env = pkg_env



========= Started set props: packageFilename (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:46.520850) =========
basename build/obj-firefox/dist/firefox-26.0a1.en-US.linux-x86_64.tar.bz2
 in dir /builds/slave/m-cen-l64-00000000000000000000/

 645         self.addStep(SetProperty(
 646             description=['set', fileType.lower(), 'filename'],
 647             doStepIf=doStepIf,
 648             command=['basename', WithProperties('%(filepath)s')],
 649             property=fileType + 'Filename',
 650             workdir='.',
 651             name='set_' + fileType.lower() + '_filename',
 652             haltOnFailure=haltOnFailure
 653         ))

========= Started set props: packageSize (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:46.581323) =========
bash -c 'ls -l build/obj-firefox/dist/firefox-26.0a1.en-US.linux-x86_64.tar.bz2'
 in dir /builds/slave/m-cen-l64-00000000000000000000/

 654         self.addStep(SetProperty(
 655             description=['set', fileType.lower(), 'size', ],
 656             doStepIf=doStepIf,
 657             command=['bash', '-c',
 658                      WithProperties("ls -l %(filepath)s")],
 659             workdir='.',
 660             name='set_' + fileType.lower() + '_size',
 661             extract_fn=self.parseFileSize(propertyName=fileType + 'Size'),
 662             haltOnFailure=haltOnFailure
 663         ))


========= Started set props: packageHash (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:46.664496) =========
bash -c 'openssl dgst -sha512 build/obj-firefox/dist/firefox-26.0a1.en-US.linux-x86_64.tar.bz2'
 in dir /builds/slave/m-cen-l64-00000000000000000000/

 664         self.addStep(SetProperty(
 665             description=['set', fileType.lower(), 'hash', ],
 666             doStepIf=doStepIf,
 667             command=['bash', '-c',
 668                      WithProperties('openssl ' + 'dgst -' + self.hashType +
 669                                     ' %(filepath)s')],
 670             workdir='.',
 671             name='set_' + fileType.lower() + '_hash',
 672             extract_fn=self.parseFileHash(propertyName=fileType + 'Hash'),
 673             haltOnFailure=haltOnFailure
 674         ))




========= Started set props: filepath (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:46.878614) =========
echo "filepath:"
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox/dist
filepath: None

 675         self.addStep(SetProperty(
 676             description=['unset', 'filepath', ],
 677             doStepIf=doStepIf,
 678             name='unset_filepath',
 679             command='echo "filepath:"',
 680             workdir=directory,
 681             extract_fn=self.unsetFilepath,
 682         ))



========= Started set props: buildid (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:46.936838) =========
python build/config/printconfigsetting.py build/obj-firefox/dist/bin/application.ini App BuildID
 in dir /builds/slave/m-cen-l64-00000000000000000000/
buildid: '20130808043413'

BUT WAIT XXX TODO ? WE HAVE ALREADY DETERMINED BUILDID PREVIOUSLY

========= Started set props: appVersion (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:47.014982) =========
python build/config/printconfigsetting.py build/obj-firefox/dist/bin/application.ini App Version
 in dir /builds/slave/m-cen-l64-00000000000000000000/
appVersion: '26.0a1'
========= Started set props: appName (results: 0, elapsed: 0 secs) (at 2013-08-08 06:06:47.079159) =========
python build/config/printconfigsetting.py build/obj-firefox/dist/bin/application.ini App Name
 in dir /builds/slave/m-cen-l64-00000000000000000000/
appName: 'Firefox'

1637         # Windows special cases
1638         if self.enableInstaller and self.productName != 'xulrunner': # XXX TODO XXX DOES NOT GET HIT
1639             self.addStep(ShellCommand(
1640                 name='make_installer',
1641                 command=self.makeCmd + ['installer'] + pkgArgs,
1642                 env=pkg_env,
1643                 workdir='build/%s' % self.objdir,
1644                 haltOnFailure=True
1645             ))
1646             self.addFilePropertiesSteps(filename='*.installer.exe',
1647                                         directory='build/%s/dist/install/sea' % self.mozillaObjdir,
1648                                         fileType='installer',
1649                                         haltOnFailure=True)
1650 
1651         if self.productName == 'xulrunner': # XXX TODO XXX DOES NOT GET HIT
1652             self.addStep(SetProperty(
1653                 command=[
1654                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1655                          'build/%s/dist/bin/platform.ini' % self.mozillaObjdir,
1656                          'Build', 'BuildID'],
1657                 property='buildid',
1658                 workdir='.',
1659                 name='get_build_id',
1660             ))
1661         else:
1662             self.addStep(SetProperty(
1663                 command=[
1664                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1665                          'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1666                          'App', 'BuildID'],
1667                 property='buildid',
1668                 workdir='.',
1669                 name='get_build_id',
1670             ))
1671             self.addStep(SetProperty(
1672                 command=[
1673                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1674                          'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1675                          'App', 'Version'],
1676                 property='appVersion',
1677                 workdir='.',
1678                 name='get_app_version',
1679             ))
1680             self.addStep(SetProperty(
1681                 command=[
1682                     'python', 'build%s/config/printconfigsetting.py' % self.mozillaDir,
1683                          'build/%s/dist/bin/application.ini' % self.mozillaObjdir,
1684                          'App', 'Name'],
1685                 property='appName',
1686                 workdir='.',
1687                 name='get_app_name',
1688             ))
1689         self.pkg_env = pkg_env


========= Started set props: symbolsUrl packageUrl testsUrl jsshellUrl (results: 0, elapsed: 1 mins, 4 secs) (at 2013-08-08 06:06:47.143385) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env MOZ_OBJDIR="obj-firefox" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" SYMBOL_SERVER_USER="ffxbld" DISPLAY=":2" CCACHE_UMASK="002" UPLOAD_USER="ffxbld" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" HG_SHARE_BASE_DIR="/builds/hg-shared" LC_ALL="C" MOZ_CRASHREPORTER_NO_REPORT="1" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" UPLOAD_SSH_KEY="~/.ssh/ffxbld_dsa" TINDERBOX_OUTPUT="1" MOZ_SIGN_CMD="python /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/signtool.py --cachedir /builds/slave/m-cen-l64-00000000000000000000/signing_cache -t /builds/slave/m-cen-l64-00000000000000000000/token -n /builds/slave/m-cen-l64-00000000000000000000/nonce -c /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/host.cert -H signing4.srv.releng.scl3.mozilla.com:9110 -H signing5.srv.releng.scl3.mozilla.com:9110 -H signing6.srv.releng.scl3.mozilla.com:9110" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" UPLOAD_TO_TEMP="1" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" UPLOAD_HOST="stage.mozilla.org" POST_UPLOAD_CMD="post_upload.py --tinderbox-builds-dir mozilla-central-linux64 -p firefox -i 20130808043413 --revision 264e54846d4a --release-to-tinderbox-dated-builds" CCACHE_DIR="/builds/ccache" CCACHE_COMPRESS="1" python '"'"'/builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py'"'"' -s 1 -r 5 -t 2460 make upload'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox
symbolsUrl: 'http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.crashreporter-symbols.zip'
packageUrl: 'http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tar.bz2'
testsUrl: 'http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tests.zip'
jsshellUrl: 'http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/jsshell-linux-x86_64.zip'



1691     def addUploadSteps(self):
1692         if self.multiLocale: # XXX TODO I don't think this is hit
1693             self.doUpload(postUploadBuildDir='en-US')
1694             cmd = ['python', 'mozharness/%s' % self.multiLocaleScript,
1695                    '--config-file', self.multiLocaleConfig]
1696             if self.multiLocaleMerge:
1697                 cmd.append('--merge-locales')
1698             if self.gaiaLanguagesFile:
1699                 cmd.extend(['--gaia-languages-file', WithProperties(
1700                     '%(basedir)s/build/gaia/' + self.gaiaLanguagesFile)])
1701             if self.gaiaL10nRoot:
1702                 cmd.extend(['--gaia-l10n-root', self.gaiaL10nRoot])
1703             if self.geckoLanguagesFile:
1704                 cmd.extend(['--gecko-languages-file', self.geckoLanguagesFile])
1705             if self.geckoL10nRoot:
1706                 cmd.extend(['--gecko-l10n-root', self.geckoL10nRoot])
1707             cmd.extend(self.mozharnessMultiOptions)
1708             self.addStep(MockCommand(
1709                 name='mozharness_multilocale',
1710                 command=cmd,
1711                 env=self.pkg_env,
1712                 workdir=WithProperties('%(basedir)s'),
1713                 haltOnFailure=True,
1714                 mock=self.use_mock,
1715                 target=self.mock_target,
1716                 mock_workdir_prefix=None,
1717             ))
1718             # b2g doesn't get snippets, and these steps don't work it, so don't
1719             # run them
1720             if self.productName != 'b2g':
1721                 self.addFilePropertiesSteps(filename=self.packageFilename,
1722                                             directory='build/%s/dist' % self.mozillaObjdir,
1723                                             fileType='package',
1724                                             haltOnFailure=True)
1725 
1726         if self.createSnippet and 'android' not in self.complete_platform: # XXX TODO I dont think this is hit
1727             self.addCreateUpdateSteps();
1728
1729         # Call out to a subclass to do the actual uploading
1730         self.doUpload(uploadMulti=self.multiLocale)


# I think we use NightlyBuildFactory here
2415     def doUpload(self, postUploadBuildDir=None, uploadMulti=False):
2416         # Because of how the RPM packaging works,
2417         # we need to tell make upload to look for RPMS
2418         if 'rpm' in self.complete_platform: # XXX TOD
2419             upload_vars = ["MOZ_PKG_FORMAT=RPM"]
2420         else:
2421             upload_vars = []
2422         uploadEnv = self.env.copy()
2423         uploadEnv.update({'UPLOAD_HOST': self.stageServer,
2424                           'UPLOAD_USER': self.stageUsername,
2425                           'UPLOAD_TO_TEMP': '1'})
2426         if self.stageSshKey:
2427             uploadEnv['UPLOAD_SSH_KEY'] = '~/.ssh/%s' % self.stageSshKey
2428 
2429         # Always upload builds to the dated tinderbox builds directories
2430         if self.tinderboxBuildsDir is None:
2431             tinderboxBuildsDir = "%s-%s" % (
2432                 self.branchName, self.stagePlatform)
2433         else:
2434             tinderboxBuildsDir = self.tinderboxBuildsDir
2435 
2436         uploadArgs = dict(
2437             upload_dir=tinderboxBuildsDir,
2 38             product=self.stageProduct,
2439             buildid=WithProperties("%(buildid)s"),
2440             revision=WithProperties("%(got_revision)s"),
2441             as_list=False,
2442         )
2443         if self.hgHost.startswith('ssh'): XXX TODO this is never hit anymore 
2444             uploadArgs['to_shadow'] = True
2445             uploadArgs['to_tinderbox_dated'] = False
2446         else:
2447             uploadArgs['to_shadow'] = False
2448             uploadArgs['to_tinderbox_dated'] = True
2449 
2450         if self.nightly: # XXX TODO this does not get hit
2451             uploadArgs['to_dated'] = True
2452             if 'st-an' in self.complete_platform or 'dbg' in self.complete_platform or 'asan' in self.complete_platform:
2453                 uploadArgs['to_latest'] = False
2454             else:
2455                 uploadArgs['to_latest'] = True
2456             if self.post_upload_include_platform:
2457                 # This was added for bug 557260 because of a requirement for
2458                 # mobile builds to upload in a slightly different location
2459                 uploadArgs['branch'] = '%s-%s' % (
2460                     self.branchName, self.stagePlatform)
2461             else:
2462                 uploadArgs['branch'] = self.branchName
2463         if uploadMulti: # XXX TODO
2464             upload_vars.append("AB_CD=multi")
2465         if postUploadBuildDir:
2466             uploadArgs['builddir'] = postUploadBuildDir
2467         uploadEnv['POST_UPLOAD_CMD'] = postUploadCmdPrefix(**uploadArgs)
2468 
2469         if self.productName == 'xulrunner': # XXX TODO this does not get hit
2470             self.addStep(RetryingMockProperty(
2471                          command=self.makeCmd + ['-f', 'client.mk', 'upload'],
2472                          env=uploadEnv,
2473                          workdir='build',
2474                          extract_fn=parse_make_upload,
2475                          haltOnFailure=True,
2476                          description=["upload"],
2477                          timeout=60 * 60,  # 60 minutes
2478                          log_eval_func=lambda c, s: regex_log_evaluator(
2479                          c, s, upload_errors),
2480                          locks=[upload_lock.access('counting')],
2481                          mock=self.use_mock,
2482                          target=self.mock_target,
2483                          ))
2484         else: # This is our make upload
2485             objdir = WithProperties(
2486                 '%(basedir)s/' + self.baseWorkDir + '/' + self.objdir)
2487             if self.platform.startswith('win'):
2488                 objdir = '%s/%s' % (self.baseWorkDir, self.objdir)
2489             self.addStep(RetryingMockProperty(
2490                 name='make_upload',
2491                 command=self.makeCmd + ['upload'] + upload_vars,
2492                 env=uploadEnv,
2493                 workdir=objdir,
2494                 extract_fn=parse_make_upload,
2495                 haltOnFailure=True,
2496                 description=self.makeCmd + ['upload'],
2497                 mock=self.use_mock,
2498                 target=self.mock_target,
2499                 mock_workdir_prefix=None,
2500                 timeout=40 * 60,  # 40 minutes
2501                 log_eval_func=lambda c, s: regex_log_evaluator(
2502                     c, s, upload_errors),
2503                 locks=[upload_lock.access('counting')],
2504             ))




========= Started sendchange (results: 0, elapsed: 0 secs) (at 2013-08-08 06:07:51.999097) =========
    master: buildbot-master81.build.mozilla.org:9301
    branch: mozilla-central-linux64-talos
    revision: 264e54846d4a
    comments: merge b2g-inbound to mozilla-central
    user: sendchange
    files: ['http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tar.bz2']
    properties: [('buildid', '20130808043413'), ('pgo_build', False), ('builduid', u'3b789b4268ee4d398fc2f961fff7ddc9')]
python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py -s 5 -t 1800 -r 5 --stdout-regexp 'change sent successfully' buildbot sendchange --master buildbot-master81.build.mozilla.org:9301 --username sendchange --branch mozilla-central-linux64-talos --revision 264e54846d4a --comments 'merge b2g-inbound to mozilla-central' --property buildid:20130808043413 --property pgo_build:False --property builduid:3b789b4268ee4d398fc2f961fff7ddc9 http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tar.bz2
 in dir /builds/slave/m-cen-l64-00000000000000000000/build
========= Started sendchange
    master: buildbot-master81.build.mozilla.org:9301
    branch: mozilla-central-linux64-opt-unittest
    revision: 264e54846d4a
    comments: merge b2g-inbound to mozilla-central
    user: sendchange-unittest
    files: ['http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tar.bz2', 'http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tests.zip']
    properties: [('buildid', '20130808043413'), ('pgo_build', False), ('builduid', u'3b789b4268ee4d398fc2f961fff7ddc9')]
python /builds/slave/m-cen-l64-00000000000000000000/tools/buildfarm/utils/retry.py -s 5 -t 1800 -r 5 --stdout-regexp 'change sent successfully' buildbot sendchange --master buildbot-master81.build.mozilla.org:9301 --username sendchange-unittest --branch mozilla-central-linux64-opt-unittest --revision 264e54846d4a --comments 'merge b2g-inbound to mozilla-central' --property buildid:20130808043413 --property pgo_build:False --property builduid:3b789b4268ee4d398fc2f961fff7ddc9 http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tar.bz2 http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1375961653/firefox-26.0a1.en-US.linux-x86_64.tests.zip
 in dir /builds/slave/m-cen-l64-00000000000000000000/build

2506         if self.profiledBuild: # XXX TODO for pgo config, add this
2507             talosBranch = "%s-%s-pgo-talos" % (
2508                 self.branchName, self.complete_platform)
2509         else:
2510             talosBranch = "%s-%s-talos" % (
2511                 self.branchName, self.complete_platform)
2512 
2513         sendchange_props = {
2514             'buildid': WithProperties('%(buildid:-)s'),
2515             'builduid': WithProperties('%(builduid:-)s'),
2516         }
2517         if self.nightly: # XXX TODO
2518             sendchange_props['nightly_build'] = True
2519         # Not sure if this having this property is useful now
2520         # but it is
2521         if self.profiledBuild: # XXX TODO
2522             sendchange_props['pgo_build'] = True
2523         else:
2524             sendchange_props['pgo_build'] = False
2525 
2526         if not uploadMulti:
2527             for master, warn, retries in self.talosMasters:
2528                 self.addStep(SendChangeStep(
2529                              name='sendchange_%s' % master,
2530                              warnOnFailure=warn,
2531                              master=master,
2532                              retries=retries,
2533                              branch=talosBranch,
2534                              revision=WithProperties("%(got_revision)s"),
2535                              files=[WithProperties('%(packageUrl)s'),
2536                                     WithProperties('%(testsUrl)s')],
2537                              user="sendchange",
2538                              comments=WithProperties('%(comments:-)s'),
2539                              sendchange_props=sendchange_props,
2540                              env=self.env,
2541                              ))
2542 
2543             files = [WithProperties('%(packageUrl)s')]
2544             if '1.9.1' not in self.branchName:
2545                 files.append(WithProperties('%(testsUrl)s'))
2546 
2547             if self.packageTests:
2548                 for master, warn, retries in self.unittestMasters:
2549                     self.addStep(SendChangeStep(
2550                                  name='sendchange_%s' % master,
2551                                  warnOnFailure=warn,
2552                                  master=master,
2553                                  retries=retries,
2554                                  branch=self.unittestBranch,
2555                                  revision=WithProperties("%(got_revision)s"),
2556                                  files=files,
2557                                  user="sendchange-unittest",
2558                                  comments=WithProperties('%(comments:-)s'),
2559                                  sendchange_props=sendchange_props,
2560                                  env=self.env,
2561                                  ))


========= Started 'mock_mozilla -r ...' (results: 0, elapsed: 1 mins, 3 secs) (at 2013-08-08 06:07:53.428173) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" CCACHE_COMPRESS="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" LC_ALL="C" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make package MOZ_PKG_PRETTYNAMES=1'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox

1517     def addTestPrettyNamesSteps(self):
1518         # Disable signing for l10n check steps
1519         env = self.env
1520         if 'MOZ_SIGN_CMD' in env:
1521             env = env.copy()
1522             del env['MOZ_SIGN_CMD']
1523            
1524         if 'mac' in self.platform: # XXX TODO
1525             # Need to run this target or else the packaging targets will
1526             # fail.
1527             self.addStep(ShellCommand(
1528                          name='postflight_all',
1529                          command=self.makeCmd + [
1530                          '-f', 'client.mk', 'postflight_all'],
1531                          env=env,
1532                          haltOnFailure=False,
1533                          flunkOnFailure=False,
1534                          warnOnFailure=False,
1535                          ))
1536         pkg_targets = ['package']
1537         if self.enableInstaller: # windows XXX TODO
1538             pkg_targets.append('installer')
1539         for t in pkg_targets:
1540             self.addStep(MockCommand(
1541                          name='make %s pretty' % t,
1542                          command=self.makeCmd + [t, 'MOZ_PKG_PRETTYNAMES=1'],
1543                          env=env,
1544                          workdir='build/%s' % self.objdir,
1545                          haltOnFailure=False,
1546                          flunkOnFailure=False,
1547                          warnOnFailure=True,
1548                          mock=self.use_mock,
1549                          target=self.mock_target,
1550                          ))



========= Started 'mock_mozilla -r ...' (results: 0, elapsed: 30 secs) (at 2013-08-08 06:08:56.548805) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" CCACHE_COMPRESS="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" LC_ALL="C" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make -C obj-firefox/tools/update-packaging MOZ_PKG_PRETTYNAMES=1'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build
1551         self.addStep(MockCommand(    
1552                      name='make update pretty',
1553                      command=self.makeCmd + ['-C',
1554                                              '%s/tools/update-packaging' % self.mozillaObjdir,
1555                                              'MOZ_PKG_PRETTYNAMES=1'],
1556                      env=env,
1557                      haltOnFailure=False,
1558                      flunkOnFailure=False,
1559                      warnOnFailure=True,
1560                      workdir='build',
1561                      mock=self.use_mock,
1562                      target=self.mock_target,
1563                      ))




========= Started 'mock_mozilla -r ...' (results: 0, elapsed: 40 secs) (at 2013-08-08 06:09:27.242979) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" CCACHE_COMPRESS="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" LC_ALL="C" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make l10n-check MOZ_PKG_PRETTYNAMES=1'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox (timeout 1200 secs)

1564         if self.l10nCheckTest:
1565             self.addStep(MockCommand(
1566                          name='make l10n check pretty',
1567                          command=self.makeCmd + [
1568                          'l10n-check', 'MOZ_PKG_PRETTYNAMES=1'],
1569                          workdir='build/%s' % self.objdir,
1570                          env=env,
1571                          haltOnFailure=False,
1572                          flunkOnFailure=False,
1573                          warnOnFailure=True,
1574                          mock=self.use_mock,
1575                          target=self.mock_target,
1576                          ))



========= Started 'mock_mozilla -r ...' (results: 0, elapsed: 33 secs) (at 2013-08-08 06:10:08.195626) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" CCACHE_COMPRESS="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" LC_ALL="C" SYMBOL_SERVER_USER="ffxbld" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make l10n-check'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox

1467     def addL10nCheckTestSteps(self):
1468         # We override MOZ_SIGN_CMD here because it's not necessary
1469         # Disable signing for l10n check steps
1470         env = self.env
1471         if 'MOZ_SIGN_CMD' in env:
1472             env = env.copy()
1473             del env['MOZ_SIGN_CMD']
1474            
1475         self.addStep(MockCommand(
1476                      name='make l10n check',
1477                      command=self.makeCmd + ['l10n-check'],
1478                      workdir='build/%s' % self.objdir,
1479                      env=env,                 
1480                      haltOnFailure=False,     
1481                      flunkOnFailure=False,
1482                      warnOnFailure=True,
1483                      mock=self.use_mock,
1484                      target=self.mock_target,
1485                      ))


========= Started check test complete (results: 0, elapsed: 17 mins, 54 secs) (at 2013-08-08 06:10:41.494384) =========
mock_mozilla -r mozilla-centos6-x86_64 --cwd /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox --unpriv --shell '/usr/bin/env HG_SHARE_BASE_DIR="/builds/hg-shared" MINIDUMP_SAVE_PATH="/builds/slave/m-cen-l64-00000000000000000000/minidumps" MOZ_CRASHREPORTER_NO_REPORT="1" MOZ_SYMBOLS_EXTRA_BUILDID="linux64" SYMBOL_SERVER_HOST="symbolpush.mozilla.org" CCACHE_DIR="/builds/ccache" POST_SYMBOL_UPLOAD_CMD="/usr/local/bin/post-symbol-upload.py" MOZ_SIGN_CMD="python /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/signtool.py --cachedir /builds/slave/m-cen-l64-00000000000000000000/signing_cache -t /builds/slave/m-cen-l64-00000000000000000000/token -n /builds/slave/m-cen-l64-00000000000000000000/nonce -c /builds/slave/m-cen-l64-00000000000000000000/tools/release/signing/host.cert -H signing4.srv.releng.scl3.mozilla.com:9110 -H signing5.srv.releng.scl3.mozilla.com:9110 -H signing6.srv.releng.scl3.mozilla.com:9110" SYMBOL_SERVER_SSH_KEY="/home/mock_mozilla/.ssh/ffxbld_dsa" DISPLAY=":2" PATH="/tools/buildbot/bin:/usr/local/bin:/usr/lib64/ccache:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/tools/git/bin:/tools/python27/bin:/tools/python27-mercurial/bin:/home/cltbld/bin" CCACHE_BASEDIR="/builds/slave/m-cen-l64-00000000000000000000" TINDERBOX_OUTPUT="1" CCACHE_COMPRESS="1" SYMBOL_SERVER_PATH="/mnt/netapp/breakpad/symbols_ffx/" MOZ_OBJDIR="obj-firefox" LC_ALL="C" SYMBOL_SERVER_USER="ffxbld" MINIDUMP_STACKWALK="/builds/slave/m-cen-l64-00000000000000000000/tools/breakpad/linux64/minidump_stackwalk" LD_LIBRARY_PATH="/tools/gcc-4.3.3/installed/lib64" CCACHE_UMASK="002" make -k check'
 in dir /builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox
PASSED ALL
make[1]: Leaving directory `/builds/slave/m-cen-l64-00000000000000000000/build/obj-firefox/js/src'
State Changed: unlock buildroot
program finished with exit code 0
elapsedTime=1073.870947
TinderboxPrint: check<br/>27292/0

1450     def addCheckTestSteps(self):
1451         env = self.env.copy()
1452         env['MINIDUMP_STACKWALK'] = getPlatformMinidumpPath(self.platform)
1453         env['MINIDUMP_SAVE_PATH'] = WithProperties('%(basedir:-)s/minidumps')
1454         self.addStep(MockMozillaCheck(
1455                      test_name="check",
1456                      makeCmd=self.makeCmd,
1457                      warnOnWarnings=True,
1458                      workdir=WithProperties(
1459                          '%(basedir)s/build/' + self.objdir),
1460                      timeout=5 * 60,  # 5 minutes.
1461                      env=env,
1462                      target=self.mock_target,
1463                      mock=self.use_mock,
1464                      mock_workdir_prefix=None,
1465                      ))



========= Started 'ccache -s' (results: 0, elapsed: 0 secs) (at 2013-08-08 06:28:35.910178) =========
ccache -s
 in dir /builds/slave/m-cen-l64-00000000000000000000/build

1057         if self.enable_ccache:
1058             self.addStep(ShellCommand(command=['ccache', '-s'],
1059                                       name="print_ccache_stats", warnOnFailure=False,
1060                                       flunkOnFailure=False, haltOnFailure=False, env=self.env))


========= Started maybe rebooting slave lost (results: 0, elapsed: 1 mins, 0 secs) (at 2013-08-08 06:28:36.058512) =========
========= Finished maybe rebooting slave lost (results: 0, elapsed: 1 mins, 0 secs) (at 2013-08-08 06:29:36.223582) =========

 554     def addPeriodicRebootSteps(self):
 555         def do_disconnect(cmd):
 556             try:
 557                 if 'SCHEDULED REBOOT' in cmd.logs['stdio'].getText():
 558                     return True
 559             except:
 560                 pass
 561             return False
 562         self.addStep(DisconnectStep(
 563                      name='maybe_rebooting',
 564                      command=[
 565                      'python', 'tools/buildfarm/maintenance/count_and_reboot.py',
 566                      '-f', '../reboot_count.txt',
 567                      '-n', str(self.buildsBeforeReboot),
 568                      '-z'],
 569                      description=['maybe rebooting'],
 570                      force_disconnect=do_disconnect,
 571                      warnOnFailure=False,
 572                      flunkOnFailure=False,
 573                      alwaysRun=True,
 574                      workdir='.'
 575                      ))


