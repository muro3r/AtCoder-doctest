from pathlib import Path

import pytest
import responses

from atcoder_doctest import atcoder_doctest

TEST_URL = "https://atcoder.jp/contests/test/tasks/test_a"


@responses.activate
def test_get_body(capsys):
    """fetch problem body."""
    body = """
<title>contest title</title>
<span class="lang-ja">
    <pre>A B</pre>
    <pre id="pre-sample0">Sample0</pre>
    <pre id="pre-sample1">Sample1</pre>
    <pre id="pre-sample2">Sample2</pre>
    <pre id="pre-sample3">Sample3</pre>
    </pre>
</span>
"""

    expect = """contest title
https://atcoder.jp/contests/test/tasks/test_a
A B
Sample0
Sample1
Sample2
Sample3

"""

    responses.add(
        responses.GET, TEST_URL, body=body,
    )

    atcoder_doctest.get_body(TEST_URL)
    out, _ = capsys.readouterr()

    assert expect == out


def test_output_file(tmp_path, monkeypatch):
    """write file test"""
    expect = '''"""body"""

def main():
    pass


if __name__ == "__main__":
    main()
'''

    monkeypatch.chdir(tmp_path)

    atcoder_doctest.output(TEST_URL, "body")

    p = Path("test/test_a.py")
    assert p.exists()
    with p.open() as f:
        assert expect == f.read()

    # if already exists
    with pytest.raises(SystemExit) as exited:
        atcoder_doctest.output(TEST_URL, "body")
        assert exited.value.value == 1
