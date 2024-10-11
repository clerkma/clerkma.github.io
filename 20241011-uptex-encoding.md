# upTeX中的编码

2024年upTeX中增加了超过`0x10FFFF`的code point模型。该模型针对部分grapheme cluster。

* Kana (Semi-)Voiced Sound Mark:
  * `(?P<ucv>[\u3000-\u31FF\u1AFF0-\u1B16F])(?P<uvs>[\u3099-\u309A])`
  * `((uvs - 0x3099) << 17) + 0x220000 + ucv`
* Emoji Modifier Fitzpatric:
  * `(?P<ucv>[\u2600-\u27BF\u1F300-\u1F9FF])(?P<uvs>[\u1F3FB-\u1F3FF])`
  * `((uvs - 0x1F3FB) << 17) + 0x260000 + ucv`
* RGI Emoji Flag Sequence:
  * `(?P<ucv>[\u1F1E6-\u1F1FF])(?P<uvs>[\u1F1E6-\u1F1FF])`
  * `((ucv & 0xFF) << 8) + (uvs & 0xFF) + 0x250000`
* VS1 ~ VS16
  * `(?P<ucv>[\u0000-\u2FFFF])(?P<uvs>[\uFE00-\uFE0F])`
  * `((uvs - 0xFE00) << 18) + 0x400000 + ucv`
* BMP + [VS17 ~ VS256]
  * `(?P<ucv>[\u0000-\uFFFF])(?P<uvs>[\uE0100-\uE01EF])`
  * ` ((uvs - 0xE0100) << 18) + 0x800000 + ucv`
* SIP + [VS17 ~ VS32]
  * `(?P<ucv>[\u10000-\u2FFFF])(?P<uvs>[\uE0100-\uE010F])`
  * `((uvs - 0xE0100) << 18) + 0x800000 + ucv`
* TIP + [VS17 ~ VS32]
  * `(?P<ucv>[\u30000-\u32FFFF])(?P<uvs>[\uE0100-\uE010F])`
  * `((uvs - 0xE0100) << 18) + 0x800000 + ucv`
