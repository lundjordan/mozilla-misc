ALRIGHT LETS DO CREATESUMMARY!!!!

    4)def addCompleteLog(self, name, text):
        log.msg("addCompleteLog(%s)" % name)
        loog = self.step_status.addLog(name)
        size = loog.chunkSize
        for start in range(0, len(text), size):
            loog.addStdout(text[start:start+size])
        loog.finish()
        self._connectPendingLogObservers()

    def _connectPendingLogObservers(self):
        if not self._pendingLogObservers:
            return
        if not self.step_status:
            return
        current_logs = {}
        for loog in self.step_status.getLogs():
            current_logs[loog.getName()] = loog
        for logname, observer in self._pendingLogObservers[:]:
            if logname in current_logs:
                observer.setLog(current_logs[logname])
                self._pendingLogObservers.remove((logname, observer))

#### MOCHITEST
entry point ->
    def createSummary(self, log):
        self.4) addCompleteLog('summary',1-3) summarizeLogMochitest(self.name, log))

        1)def summarizeLogMochitest(name, log):
            infoRe = r"\d+ INFO (Passed|Failed|Todo):\ +(\d+)"
            # Support browser-chrome result summary format which differs from MozillaMochitest's.
            if name == 'mochitest-browser-chrome':
                infoRe = r"\t(Passed|Failed|Todo): (\d+)"

            return 2) summarizeLog(
                name, log, "Passed", "Failed", "Todo",
                infoRe)

            # otherIdent can be None if the test suite does not have this feature (yet).
            2)def summarizeLog(name, log, "Passed", "Failed", "Todo", infoRe):
                # Counts and flags.
                successCount = -1
                failureCount = -1
                otherCount = otherIdent and -1
                crashed = False
                leaked = False

                # Regular expression for result summary details.
                # Reuse 'infoRe'.
                infoRe = re.compile(infoRe)
                # Regular expression for crash and leak detections.
                harnessErrorsRe = re.compile(r"TEST-UNEXPECTED-FAIL \| .* \| (Browser crashed \(minidump found\)|missing output line for total leaks!|negative leaks caught!|leaked \d+ bytes during test execution)")
                # Process the log.
                for line in log.readlines():
                    # Set the counts.
                    m = infoRe.match(line)
                    if m:
                        r = m.group(1)
                        if r == successIdent:
                            successCount = int(m.group(2))
                        elif r == failureIdent:
                            failureCount = int(m.group(2))
                        # If otherIdent == None, then infoRe should not match it,
                        # so this test is fine as is.
                        elif r == otherIdent:
                            otherCount = int(m.group(2))
                        continue
                    # Set the error flags.
                    m = harnessErrorsRe.match(line)
                    if m:
                        r = m.group(1)
                        if r == "Browser crashed (minidump found)":
                            crashed = True
                        elif r == "missing output line for total leaks!":
                            leaked = None
                        else:
                            leaked = True
                        # continue
                # Return the summary.
                return "TinderboxPrint: %s<br/>%s\n" % (name,
                    3) summaryText(successCount, failureCount, otherCount, crashed, leaked))

                # Some test suites (like TUnit) may not (yet) have the knownFailCount feature.
                # Some test suites (like TUnit) may not (yet) have the crashed feature.
                # Expected values for leaked: False, no leak; True, leaked; None, report failure.
                            def emphasizeFailureText(text):
                                return '<em class="testfail">%s</em>' % text
                3)def summaryText(passCount, failCount, knownFailCount=None,
                        crashed=False, leaked=False):
                    # Format the tests counts.
                    if passCount < 0 or failCount < 0 or \
                    (knownFailCount != None and knownFailCount < 0):
                        # Explicit failure case.
                        summary = emphasizeFailureText("T-FAIL")
                    elif passCount == 0 and failCount == 0 and \
                        (knownFailCount == None or knownFailCount == 0):
                        # Implicit failure case.
                        summary = emphasizeFailureText("T-FAIL")
                    else:
                        # Handle failCount.
                        failCountStr = str(failCount)
                        if failCount > 0:
                            failCountStr = emphasizeFailureText(failCountStr)
                        # Format the counts.
                        summary = "%d/%s" % (passCount, failCountStr)
                        if knownFailCount != None:
                            summary += "/%d" % knownFailCount

                    # Format the crash status.
                    if crashed:
                        summary += "&nbsp;%s" % emphasizeFailureText("CRASH")

                    # Format the leak status.
                    if leaked != False:
                        summary += "&nbsp;%s" % emphasizeFailureText((leaked and "LEAK") or "L-FAIL")
                    return summary


        # superResult = shellcommandreporttimeout.evalcmd
        #   superResult = shellcommand.evalcmd 
        #   superResult = loggingBuildStep.evalcmd --> lets say thats SUCCESS

        -> entry point
        def evaluateCommand(self, cmd):
            superResult = self.super_class.evaluateCommand(self, cmd)
            return evaluateMochitest(self.name, cmd.logs['stdio'].getText(),
                                    superResult)
            def evaluateMochitest(name, log, superResult):
                # When a unittest fails we mark it orange, indicating with the
                # WARNINGS status. Therefore, FAILURE needs to become WARNINGS
                # However, we don't want to override EXCEPTION or RETRY, so we still
                # need to use worst_status in further status decisions.
                if superResult == FAILURE:
                    superResult = WARNINGS

                if superResult != SUCCESS:
                    return superResult

                failIdent = r"^\d+ INFO Failed: 0"
                # Support browser-chrome result summary format which differs from MozillaMochitest's.
                if 'browser-chrome' in name:
                    failIdent = r"^\tFailed: 0"
                # Assume that having the 'failIdent' line
                # means the tests run completed (successfully).
                # Also check for "^TEST-UNEXPECTED-" for harness errors.
                if not re.search(failIdent, log, re.MULTILINE) or \
                re.search("^TEST-UNEXPECTED-", log, re.MULTILINE):
                    return worst_status(superResult, WARNINGS)

                return worst_status(superResult, SUCCESS)

#### REFTEST
class ReftestMixin(object):
    warnOnFailure = True
    warnOnWarnings = True

    def getSuiteOptions(self, suite):
        if suite == 'crashtest':
            return ['reftest/tests/testing/crashtest/crashtests.list']
        ...
        ...
        ...
        elif suite == 'reftest-sanity':
            return ['reftest/tests/layout/reftests/reftest-sanity/reftest.list']

    def createSummary(self, log):
        self.addCompleteLog('summary', summarizeLogReftest(self.name, log))

    def evaluateCommand(self, cmd):
        superResult = self.super_class.evaluateCommand(self, cmd)
        return evaluateReftest(cmd.logs['stdio'].getText(), superResult)

def evaluateReftest(log, superResult):
    # When a unittest fails we mark it orange, indicating with the
    # WARNINGS status. Therefore, FAILURE needs to become WARNINGS
    # However, we don't want to override EXCEPTION or RETRY, so we still
    # need to use worst_status in further status decisions.
    if superResult == FAILURE:
        superResult = WARNINGS

    if superResult != SUCCESS:
        return superResult

    # Assume that having the "Unexpected: 0" line
    # means the tests run completed (successfully).
    # Also check for "^TEST-UNEXPECTED-" for harness errors.
    if not re.search(r"^REFTEST INFO \| Unexpected: 0 \(", log, re.MULTILINE) or \
       re.search("^TEST-UNEXPECTED-", log, re.MULTILINE):
        return worst_status(superResult, WARNINGS)

    return worst_status(superResult, SUCCESS)

def worst_status(a, b):
    # SUCCESS > SKIPPED > WARNINGS > FAILURE > EXCEPTION > RETRY
    # Retry needs to be considered the worst so that conusmers don't have to
    # worry about other failures undermining the RETRY.
    for s in (RETRY, EXCEPTION, FAILURE, WARNINGS, SKIPPED, SUCCESS):
        if s in (a, b):
            return s

#### XPCSHELL
class MozillaPackagedXPCShellTests(ShellCommandReportTimeout):
    warnOnFailure = True
    warnOnWarnings = True
    name = "xpcshell"

    def __init__(self, platform, symbols_path=None, **kwargs):
        self.super_class = ShellCommandReportTimeout
        ShellCommandReportTimeout.__init__(self, **kwargs)

        self.addFactoryArguments(platform=platform, symbols_path=symbols_path)

        bin_extension = ""
        if platform.startswith('win'):
            bin_extension = ".exe"
        script = " && ".join(["if [ ! -d %(exedir)s/plugins ]; then mkdir %(exedir)s/plugins; fi",
                  "cp bin/xpcshell" + bin_extension + " %(exedir)s",
                  "cp -R bin/components/* %(exedir)s/components/",
                  "cp -R bin/plugins/* %(exedir)s/plugins/",
                  "python -u xpcshell/runxpcshelltests.py"])

        if symbols_path:
            script += " --symbols-path=%s" % symbols_path
        script += " --manifest=xpcshell/tests/all-test-dirs.list %(exedir)s/xpcshell" + bin_extension

        self.command = ['bash', '-c', WithProperties(script)]

    def createSummary(self, log):
        self.addCompleteLog('summary', summarizeLogXpcshelltests(self.name, log))

    def evaluateCommand(self, cmd):
        superResult = self.super_class.evaluateCommand(self, cmd)
        # When a unittest fails we mark it orange, indicating with the
        # WARNINGS status. Therefore, FAILURE needs to become WARNINGS
        # However, we don't want to override EXCEPTION or RETRY, so we still
        # need to use worst_status in further status decisions.
        if superResult == FAILURE:
            superResult = WARNINGS

        if superResult != SUCCESS:
            return superResult

        # Assume that having the "Failed: 0" line
        # means the tests run completed (successfully).
        # Also check for "^TEST-UNEXPECTED-" for harness errors.
        if not re.search(r"^INFO \| Failed: 0", cmd.logs["stdio"].getText(), re.MULTILINE) or \
           re.search("^TEST-UNEXPECTED-", cmd.logs["stdio"].getText(), re.MULTILINE):
            return worst_status(superResult, WARNINGS)

        return worst_status(superResult, SUCCESS)



######### STRAY OBSERVATIONS
# class MozillaCheck may be legacy
class OutPutParser shtuff
        self.status_levels = status_levels
        if status_levels:
            self.result_status_level = status_levels[-1]

        if error_check.get('status_level'):
            status_level = error_check['status_level']
            if not self.status_levels:
                self.fatal("status_levels can not be none. Its " + \
                        "needed to determine worst status_level")
            self.result_status_level = self.worst_level(status_level,
                    self.result_status_level, levels=self.status_levels)

                    # TODO maybe I don't want to call worst_level on every line in
                    # the log but instead keep track of each seperate {level}_num_count
                    # then assign worst_level after parsing. worst_level would depend on which level
                    # has a non 0 {level}_num_count and is the worst in hierarchy
                    self.result_log_level = self.worst_level(log_level, self.result_log_level)
                    # TODO I dont think we want to break now if I want to
                    # capture worst status? Make sure this does not brake
                    # anything else
                    # break 
        self.result_log_level = INFO

CategoryTestErrorList = {
    'mochitest' : BaseTestError  + [
        {'regex' : re.compile(r'''(\tFailed:\s+[1-9]|\d+ INFO Failed:\s+[1-9]'''),
            'level' : WARNING, 'explanation' : "One or more unittests failed",
            'status_level' : TBPL_WARNING, "save_line" : True},
        ],
    'reftest' : BaseTestError + [
        {'regex' : re.compile(r'''REFTEST INFO \| Unexpected: [^0] \('''),
            'level' : WARNING, 'explanation' : "One or more unittests failed",
            'status_level' : TBPL_WARNING, "save_line" : True},
        ],
    'xpcshell' : BaseTestError + [
        {'regex' : re.compile(r'''INFO \| Failed: [^0]'''), 'level' : WARNING,
                'explanation' : "One or more unittests failed",
                'status_level' : TBPL_WARNING, "save_line" : True},
        ],
}
TinderBoxPrint = {
    "mochitest_summary" : {
        'full_re_substr' : r'''(\d+ INFO (Passed|Failed|Todo):\ +(\d+)|\t(Passed|Failed|Todo): (\d+))''',
        'pass_name' : "Passed",
        'fail_name' : "Failed",
        'known_fail_name' : "Todo",
    },
    "reftest_summary" : {
        'full_re_substr' : r'''REFTEST INFO \| (Successful|Unexpected|Known problems): (\d+) \(''',
        'pass_name' : "Successful",
        'fail_name' : "Unexpected",
        'known_fail_name' : "known problems",
    },
    "xpcshell_summary" : {
        'full_re_substr' : r'''INFO \| (Passed|Failed): (\d+)''',
        'pass_name' : "Passed",
        'fail_name' : "Failed",
        'known_fail_name' : None,
    },
}

BaseTestError = [
    {'regex': re.compile(r'''TEST-UNEXPECTED'''), 'level' : WARNING,
        'explanation' : "Test unexpectingly failed." + \
                " This is a harness error.", "save_line" : True},
]
CategoryTestErrorList = {
    'mochitest' : BaseTestError  + [
        {'regex' : re.compile(r'''(\tFailed:\s+[1-9]|\d+ INFO Failed: [1-9]'''),
            'level' : WARNING, 'explanation' : "1 or more unittests failed from this suite"},
        {'regex' : re.compile(r'''(\d+ INFO (Passed|Failed|Todo):\ +(\d+)|\t(Passed|Failed|Todo): (\d+))'''),
            'level' : INFO, "save_line" : True, "silent" : True},
        ],
    'reftest' : BaseTestError + [
        {'regex' : re.compile(r'''REFTEST INFO \| Unexpected: [1-9]\('''),
            'level' : WARNING, 'explanation' : "One or more unittests failed from this suite"},
        {'regex' : re.compile(r'''REFTEST INFO \| (Successful|Unexpected|Known problems): (\d+) \('''),
            'level' : INFO, "save_line" : True, "silent" : True},
        ],
    'xpcshell' : BaseTestError + [
        {'regex' : re.compile(r'''INFO \| Failed: [^0]'''), 'level' : WARNING,
            'explanation' : "One or more unittests failed from this suite"},
        {'regex' : re.compile(r'''INFO \| (Passed|Failed): (\d+)'''),
            'level' : INFO, "save_line" : True, "silent" : True},
        ],
}
