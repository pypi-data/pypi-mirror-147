def test_package_import():
    import botcity.plugins.ftp as plugin
    assert plugin.__file__ != ""
