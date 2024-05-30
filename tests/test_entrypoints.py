def test_opera_rtc_s1_browse(script_runner):
    ret = script_runner.run(['python', '-m', 'opera_rtc_s1_browse', '-h'])
    assert ret.success
