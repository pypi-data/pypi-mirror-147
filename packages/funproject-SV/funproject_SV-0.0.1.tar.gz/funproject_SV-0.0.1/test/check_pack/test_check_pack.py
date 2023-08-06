
from check_pack.check_pack import check_pack, check_pack_name


def test_check_pack():
    expected = "Its been a while...checking now."
    got = check_pack()
    assert got == expected


def test_check_pack_name():
    expected = "Hello SV, Its been a while checking now."
    got = check_pack_name("SV")
    assert got == expected
