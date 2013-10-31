################
#### Armen's Reviews
################


What is the function of configs/test/desktop_unittest.py?
#### This file is gone now in favor of individual OS configs.

The configs/test files have few inconsistencies from one $platform_unittest.py file to another (e.g. "all_mochitest_suites" vs "all_mochi_suites".
Not sure what aki said but I would prefer of having common values be loaded from a common file (_common.py) like "global_*", "repos" and similar.
#### unified all common values and used full names where appropriate

::: configs/test/desktop_unittest.py
@@ +13,5 @@
> +BINARY = "firefox-{version}.en-US.{OS_ARCH}.{OS_EXTENSION}"
> +TESTS = "firefox-{version}.en-US.{OS_ARCH}.tests.zip"
> +
> +config = {
> +

No empty lines please.
##### removed empty lines from configs

@@ +16,5 @@
> +config = {
> +
> +        # for develepors in future. Not implemented yet.
> +        "url_base" : FTP,
> +        "file_archives" : {"bin_archive" : BINARY, "tests_archive" :  TESTS},

I would call this "files", "binary_files" and "tests_file" but that it is only my opinion.
Just the word "archive" does not ring with me (I might have used it previously though)
##### no archive naming conventions and bin is expanded to binary

@@ +25,5 @@
> +            "dest": "tools"
> +        }],
> +
> +        # I will put these in configs in the case that someone wants to try one
> +        # of there own dirs

Being explicit is good.
#### this code has been removed entirely

@@ +43,5 @@
> +            "symbols_path" : "--symbols-path={symbols_path}"
> +        },
> +
> +        #global mochitest options
> +        "global_mochi_options" : {

I would use "global_mochitest_options" to be more consistent.
#### global concept has been removed in favor of more explicit, simple options
#### that are 'unlinked' from eachother

@@ +58,5 @@
> +            'xpcshell_name' : 'firefox/{xpcshell_name}'
> +        },
> +
> +        #local mochi suites
> +        "all_mochi_suites" :

"all_mochitest_suites"
#### fixed

::: configs/test/linux_unittest.py
@@ +5,5 @@
> +
> +
> +config = {
> +
> +        ###### paths/urls can be implemented on command line as well

4 spaces of indentation please. No new line.
#### fixed

@@ +7,5 @@
> +config = {
> +
> +        ###### paths/urls can be implemented on command line as well
> +        "installer_url" : None, # eg: "http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/
> +                                                # mozilla-central-win32/1334941863/firefox-14.0a1.en-US.win32.zip"

The e.g. refers to a windows file instead of a linux tar ball being this the "linux_unittest.py" file.
#### code removed entirely

@@ +20,5 @@
> +        #######
> +
> +
> +        "symbols_url" : None, # eg: "http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/
> +                                        # mozilla-central-win32/1334941863/firefox-14.0a1.en-US.crashreporter-symbols.zip"

What are all these "None" values?
The comments are kind of noisy and broken into multiple lines. Could you make them one line? and just add comments for the ones that can be more confusing?
#### code removed entirely


::: scripts/desktop_unittest.py
@@ +31,5 @@
> +            {
> +                "action" : "append",
> +                "dest" : "specified_mochitest_suites",
> +                "type": "string",
> +                "help": """Specify which mochi suite to run.

"mochitest" for consistency.
#### fixed


@@ +85,5 @@
> +                "default": False,
> +                "help": """Does nothing ATM but I would like it to run a 'quick' set of test suites to
> +                see if there are any serious issues that can be noticed immediately.""",
> +            }
> +        ],

If it is not implemented we should take it in another bug.
#### removed

@@ +100,5 @@
> +     {'mozprofile': os.path.join('tests', 'mozbase', 'mozprofile')},
> +     {'mozprocess': os.path.join('tests', 'mozbase', 'mozprocess')},
> +     {'mozrunner': os.path.join('tests', 'mozbase', 'mozrunner')},
> +     {'peptest': os.path.join('tests', 'peptest')},
> +    ]

You can probably start with a minimum set and add as you see it fail. Probably easier when you trigger this on buildbot on all platforms.
#### addressed

@@ +126,5 @@
> +                    Please ensure that if the '--run-all-suites' flag was enabled
> +                    then do not specify to run only specific suites like '--mochitest-suite browser-chrome'""")
> +        self.glob_test_options = []
> +        self.glob_mochi_options = []
> +        self.xpcshell_options = []

I don't see 'self.xpcshell_options' being used.
#### N/A anymore as I removed that code

@@ +139,5 @@
> +
> +    ###### helper methods
> +
> +    def check_if_valid_config(self):
> +        suite_categories = ['mochitests', 'reftests', 'xpcshell']

I wonder if this list should be defined explicitly in the config files rather than being a magic list.
#### its now global

@@ +145,5 @@
> +        if not c.get('run_all_suites'):
> +            return True # configs are valid
> +
> +        is_valid = True
> +        for cat in suite_categories:

I prefer "category" or "c" but this is just an opinion.
#### replaced with category

@@ +149,5 @@
> +        for cat in suite_categories:
> +            specific_suites = c.get('specified_{cat}_suites'.format(cat=cat))
> +            if specific_suites:
> +                if specific_suites != 'all':
> +                    is_valid = False

I am not sure what are we validating in this for loop.
#### so what is happening here is that if we make it to this code
#### then c.get('run_all_suites') is True and therefore we can not
#### specify specific suites

Are we just checking that we don't run the script with something like this?
--xpcshell-suite all

Is this what we are trying to avoid?
#### specify specific suites

@@ +169,5 @@
> +            dirs['abs_app_install_dir'], 'firefox')
> +        dirs['abs_app_plugins_dir'] = os.path.join(
> +            dirs['abs_app_dir'], 'plugins')
> +        dirs['abs_app_components_dir'] = os.path.join(
> +            dirs['abs_app_dir'], 'components')

Would this look better?

dirs = {
   'abs_app_install_dir': os.path.join(abs_dirs['abs_work_dir'], 'application'),
   'abs_app_dir': os.path.join(dirs['abs_app_install_dir'], 'firefox'),
   ...
}

I think we can look at this section together and try to figure out a cleaner way.
I believe you are trying to check that if keys in *dirs* does not exist in *abs_dirs* then add it to *abs_dir*.
You could probably do it on a for loop or doing something like abs_dir.get(key_you_want, value_you_want_if_key_you_want_does_not_exist_in_abs_dir) (if a in dictionary return dict['a'] else return value b)

#### cleaned up with you

@@ +274,5 @@
> +            Please make sure you are either:
> +                    (1) specifing it in the config file under binary_path
> +                    (2) specifing it on command line with the '--binary-path' flag""")
> +
> +    def query_glob_mochi_options(self, **kwargs):

"query_glob_mochitest_options"

Are "query_glob_{reftest,xpcshell}_options" needed?
#### N/A as this code has been completely replaced

@@ +318,5 @@
> +        return suites
> +
> +    def copy_tree(self, src, dest, log_level='info', error_level='error'):
> +        """an implementation of shutil.copytree however it allows
> +        you to copy to a 'dest' that already exists"""

Should this be in a library class? I might not be making sense so feel free to discuss back or disregard.
#### copy_tree is now in script.py


@@ +349,5 @@
> +    def pull_other_repos(self):
> +        dirs = self.query_abs_dirs()
> +
> +        if self.config.get('repos'):
> +            dirs = self.query_abs_dirs()

IIUC it seems that you are running this twice.
#### named more appropriately this will just clone 'tools'

@@ +380,5 @@
> +
> +    def run_tests(self):
> +        self.mochitests()
> +        self.reftests()
> +        self.xpcshell()

I almost feel that we should not have to have categories at all.
I almost feel that we should only call mozharness with --suite and let the script determine what to do.

The functions mochitests(), reftests() and xpcshell() are very much alike.
I feel that we might be making things a little more difficult for us in the long term or fixing things in one place rather than another.

aki, what do you think?
I know this would be substantial change but I believe worth considering it now rather than later.

I am also OK with getting off my horse since both approaches would still work.
#### this has had the most change in my upcoming patch. A lot of consolidation has been implemented

@@ +448,5 @@
> +        """run tests for xpcshell"""
> +        c = self.config
> +        dirs = self.query_abs_dirs()
> +        app_xpcshell_path = os.path.join(dirs['abs_app_dir'], c['xpcshell_name'])
> +        bin_xpcshell_path = os.path.join(dirs['abs_test_bin_dir'], c['xpcshell_name'])

I wouldn't create these 2 variables just to use it once in:
self.copyfile(bin_xpcshell_path, app_xpcshell_path)
but that's just my opinion.
#### addressed




################
#### AKI'S REVIEWS ####
################

[reply] [-] Comment 16 Aki Sasaki [:aki] 2012-05-30 16:27:13 PDT

Comment on attachment 628470 [details] [diff] [review]
fixed style and unused reboot variable for buildbot-configs repo

My main 2 concerns here, outside of Armen's nits, are:

1) branch selection (Armen already pointed this out).  This should be fine for testing, however.
#### still in testing but can change to whatever you prefer when requested
2) wondering whether we have flexibility to have branch-specific configurations here.  But this is a good start.  When we end up replacing the unit test configs in UNITTEST_SUITES that may become a more pressing need; for now this should work.
#### branch specifics are still not implemented. Currently focused on what I had. It is not clear
#### what specifics I am going to run into as I have not looked 'deep' enough yet

Aki Sasaki [:aki] 2012-05-30 17:28:07 PDT
Depends on: 701506
[wrap] [reply] [-] Comment 17 Aki Sasaki [:aki] 2012-05-30 17:56:30 PDT

Comment on attachment 628048 [details] [diff] [review]
patch for mozharness repo

> diff --git a/configs/test/linux_unittest.py b/configs/test/linux_unittest.py

Hm, I've been using the configs/test/ directory for mozharness-testing config files rather than firefox-testing config files (e.g. test.illegal_suffix).

I'm open, but I think we should keep the two in separate locations.
Do you think I should move the mozharness-testing files elsewhere?  Or put these in a configs/unittest/ or something?
#### unittest configs moved to configs/unittests

As an non-blocker enhancement, we might want user-friendly standalone configs for these at some point.
#### still WIP as I have just added 3 OS seperate configs however there are options to ignore buildbot
#### specifics for the configs for developers. I would like to make this more simplified however

>+config = {
>+
>+        ###### paths/urls can be implemented on command line as well
>+        "installer_url" : None, # eg: "http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/

I tend to omit the lines that are None in production configs to keep them smaller and more readable.  The comments + empty config items are ok for now; they do belong in the standalone configs where users might hand-edit.
#### this code has been removed entirely

>+        #global unittest options
>+        "global_test_options" : {
>+            "app_name" : "--appname={binary_path}",
>+            "util_path" : "--utility-path=tests/bin",
>+            "extra_prof_path" : "--extra-profile-file=tests/bin/plugins",
>+            "symbols_path" : "--symbols-path={symbols_path}"
>+        },
>+
>+        #global mochitest options

I have the feeling we'll need to revisit this layout at some point.
For instance, when we add a new command line option on one branch but don't want it on the others.
However, I'm not sure how to guide you at this point; just noting.
I think we shouldn't change anything until we know what to change.
#### global concept has been removed in favor of more explicit, simple options
#### that are 'unlinked' from eachother

>+    # TODO find out which modules I do and dont need here
>+    virtualenv_modules = [

You probably need mozinstall and all of its dependencies.
That's actually in the test zip, so we're good.
#### kept all but peptest (can put peptest back in if we unify everything together)

I marked bug 701506 as a blocker, but it's probably not a hard blocker, as long as mozbase stays inside the test zip.

>+                    'pull-other-repos',

Haha.
Any reason you're naming it "pull-other-repos"?
#### fixed

Also, what do you need in build/tools?
I wasn't able to find a need for it.  If we need it, great; if we don't, let's take this out.  Lean&mean.
#### still here as I have been told to leave it until later once I replace the reboot step

>+        if not self.check_if_valid_config():
>+            self.fatal("""Config options are not valid.
>+                    Please ensure that if the '--run-all-suites' flag was enabled
>+                    then do not specify to run only specific suites like '--mochitest-suite browser-chrome'""")

We could do this inside of self._pre_config_lock() if you want.
#### done

>+        self.glob_test_options = []
>+        self.glob_mochi_options = []

Glob can be shorthand for a wildcard or '*'.
https://en.wikipedia.org/wiki/Glob_%28programming%29
I appreciate the attempt to reduce the amount of typing, but let's say 'global' here :)
#### done

>+        self.ran_preflight_run_commands = False

Do you need this anymore?
Afaict, this is checked and set in preflight_run_tests(), which is called once.
#### removed

>+        self.test_url = self.config.get('test_url')

c.get is equivalent to self.config.get with less typing; no preference here.
#### using c everywhere now

>+        self.installer_path = c.get('installer_path') or self.guess_installer_path()

I'd like to avoid this.
I haven't gotten to bug 753547 yet, but when I do, we'll specify installer_path's.
#### no more guessing

Here's the code I'll be leveraging:

http://hg.mozilla.org/build/mozharness/file/636e0f7b6ab6/mozharness/mozilla/testing/testbase.py#l143

Essentially, if we say we want the installer_path to be installer.exe, it'll download the installer to work_dir/installer.exe, even if it was firefox-15.0a1.en-US.win32.installer.exe.  That's good for knowing where the path to the installer is, without having to guess.
#### we now specify installer.zip or whatever

>+    def check_if_valid_config(self):
>+        suite_categories = ['mochitests', 'reftests', 'xpcshell']

These three suites are kind of hardcoded in this script, which might be ok.
This list might be nice to define as a global.
#### done

>+    def query_abs_dirs(self):
>+        if self.abs_dirs:
>+            return self.abs_dirs
>+        abs_dirs = super(DesktopUnittest, self).query_abs_dirs()
>+
>+        # TODO not make this so ugly

Wow.  Do you need all of these directories to be specified?
#### they are cleaned up however I can address further which we *need*

>+        c = self.config
>+        dirs = {}
>+        dirs['abs_app_install_dir'] = os.path.join(
>+            abs_dirs['abs_work_dir'], 'application')
>+
>+        dirs['abs_app_dir'] = os.path.join(
>+            dirs['abs_app_install_dir'], 'firefox')

I'd rather not hardcode firefox anywhere in here.
Can this go in the config files without making things too ugly?
#### done


>+    def query_glob_options(self, **kwargs):

I think I'll have to look deeper into how this runs before I have a solid opinion here, other than spelling out 'global'.
#### global concept gone

>+                    (1) specifing it in the config file under binary_path
>+                    (2) specifing it on command line with the '--binary-path' flag)

sp: 'specifying' :)
#### fixed :)

>+    def copy_tree(self, src, dest, log_level='info', error_level='error'):

We should probably use INFO and ERROR here (import them from mozharness.base.log like this:
http://hg.mozilla.org/build/mozharness/file/636e0f7b6ab6/mozharness/base/script.py#l33
#### fixed

>+        try:
>+            files = os.listdir(src)
>+            files.sort()
>+            for f in files:
>+                abs_src_f = os.path.join(src, f)
>+                abs_dest_f = os.path.join(dest, f)
>+                self.copyfile(abs_src_f , abs_dest_f)

It looks like this isn't recursive?
If we can make this recursive, I think we can move this to OSMixin.
#### OK so it is recursive with some bells and whistles. I think it is now overcomplicated
# even though I like it. It may be difficult to maintain and the three modes
# might be in excess


Overall, this looks good.  It feels a bit complex dealing with all the suites like this; I'm wondering if we'll need to refactor this later for simplicity, but I can't say for sure.  I'd like to see this running in staging!

Attachment #628048 - Flags: review?(aki@mozilla.com) → feedback+
[reply] [-] Comment 18 Aki Sasaki [:aki] 2012-05-30 18:02:13 PDT

Comment on attachment 628470 [details] [diff] [review]
fixed style and unused reboot variable for buildbot-configs repo

One thing to note here:

In bug 758988, I added a script_maxtime setting for mozharness-based tests.
This is currently capped at 1200 seconds (20min) globally, but we can override it by setting a script_maxtime in the suites dict.

1200 is pretty strict; we can bump this to 3600 or 7200, but if we need to allow for longer-running unit tests, we'll need to do that per-suite.
#### I am using script_maxtime and bumped it up to 7200



