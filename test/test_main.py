from atcoder_doctest import atcoder_doctest
import responses

body = """
<title>contest title</title>
<span class="lang-ja">
  <pre>A B</pre>
<pre id="pre-sample0">
Sample0</pre>
<pre id="pre-sample1">
Sample1</pre>
</pre>
</span>
"""

expect = """contest title
http://atcoder.jp/test/test_case
A B
Sample0
Sample1
"""


@responses.activate
def test_get_body(capsys):
    responses.add(
        responses.GET, "http://atcoder.jp/test/test_case", body=body,
    )

    atcoder_doctest.get_body("http://atcoder.jp/test/test_case")
    out, err = capsys.readouterr()

    assert expect == out
