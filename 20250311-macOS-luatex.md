# macOS下LuaTeX的字体搜索

在macOS上使用LuaTeX的常见问题就是字体找不到。这大多是为了使用CTeX。

这个问题我之前写过几次了，不过由于macOS系统更新一次，问题可能就会出现一次。

所以首先需要解决的就是字体的位置问题，我们可以使用Swift Playground运行一段代码：
```Swift
import Foundation
import CoreText

let fontset = CTFontCollectionCreateFromAvailableFonts(nil)
let match = CTFontCollectionCreateMatchingFontDescriptors(fontset) as! [CTFontDescriptor]
var path_set: Set<String> = []

for i in 0..<match.count {
    let font = match[i]
    let url = CTFontDescriptorCopyAttribute(font, kCTFontURLAttribute) as! NSURL
    if let directory = url.deletingLastPathComponent {
        let path = directory.path
        path_set.insert(path)
    }
}

for path in path_set.sorted() {
    print(path)
}
```

经过运行，就能知道字体文件装在哪里了。如果系统装了Xcode，可以使用Swift编译（文件名为`show.swift`）：
```bash
swift show.swift
./show
```

那么，在macOS 15.3上，可以看到类似下面输出：
```
/Library/Fonts
/System/Library/AssetsV2/com_apple_MobileAsset_Font7/f879347736afb6e4e0880bcede9df92492c0f040.asset/AssetData
/System/Library/Fonts
/System/Library/Fonts/Supplemental
/System/Library/PrivateFrameworks/FontServices.framework/Resources/Reserved
```

如果我们使用：
```bash
luaotfload-tool --find="KaitiSC"
```

那么会得到：
```
luaotfload | db : Reload initiated (formats: otf,ttf,ttc); reason: Font "KaitiSC" not found.
luaotfload | resolve : sequence of 3 lookups yielded nothing appropriate.
luaotfload | resolve : Cannot find "KaitiSC" in index.
luaotfload | resolve : Hint: use the --fuzzy option to display suggestions.
```

接下来，需要将相关的路径放到TeX Live的配置参数中：
```bash
tlmgr conf texmf OSFONTDIR /System/Library/AssetsV2/com_apple_MobileAsset_Font7
```

然后我们再执行查询命令，就可以得到（ 如果你的电脑处理器比较快，构建相应的缓存会非常快，查询的时候就完成了）：
```
luaotfload | db : Reload initiated (formats: otf,ttf,ttc); reason: Font "KaitiSC" not found.
luaotfload | resolve : Font "KaitiSC" found!
luaotfload | resolve : Resolved file name "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/54a2ad3dac6cac875ad675d7d273dc425010a877.asset/AssetData/Kaiti.ttc", subfont nr. 0
```

如果想要删除`OSFONTDIR`变量，可以执行：
```bash
tlmgr conf texmf --delete OSFONTDIR
```