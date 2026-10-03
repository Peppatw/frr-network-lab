# Python 刷題速查表（Day 1–3）

## 迴圈與 index

寫 for loop 前先問：loop 裡要用的是 index（位置）還是 value（數值）？

| 寫法 | 拿到什麼 | 什麼時候用 |
| --- | --- | --- |
| `for x in nums:` | 每個 value | 只需要數值（217、49） |
| `for i in range(len(nums)):` | 每個 index，`nums[i]` 拿值 | 需要位置（Two Sum、387） |
| `for i in range(1, n):` | index 從 1 到 n-1 | 要用前一格 `i-1`（238 left） |
| `for i in range(n-2, -1, -1):` | index 從 n-2 倒著走到 0 | 從右往左（238 right） |
| `while left < right:` | 兩個指標各自移動 | two pointers（125） |

`range(a, b)` 包含 a、不包含 b。

`and` / `or` 會短路：第一個條件就能決定結果時，第二個不會執行。所以「會出錯的檢查」放後面，例如 `i >= len(s) or s[i] != c`。

## List

一排有編號的格子，可以修改；用 `in` 查詢要從頭掃，O(n)。

| 寫法 | 意思 |
| --- | --- |
| `a = [1] * n` | 長度 n、全部是 1 的 list |
| `a.append(x)` | 加到最後 |
| `a[-1]` | 最後一個 |
| `a[-k:]` | 最後 k 個 |
| `a[:-k]` | 最後 k 個以外的 |
| `a[:i]` | index 0 到 i-1 |
| `a.index(x)` | x 第一次出現的 index，x 不存在會出錯，O(n) |
| `x in a` | x 有沒有在裡面，O(n) |
| `a + b` | 接起來，產生新 list |
| `nums[:] = ...` | 改寫原本的 list（`nums = ...` 只是改變變數名稱的指向） |

## String

字串不能修改：`s[0] = 'h'` 會出錯，要改就產生新字串。用 index 拿字元、slicing 都跟 list 一樣。

| 寫法 | 意思 |
| --- | --- |
| `for ch in s:` | 一個一個字元走 |
| `s.lower()` | 轉小寫 |
| `ch.isalnum()` | 是不是字母或數字 |
| `s[::-1]` | 倒過來 |
| `sorted(s)` | 排序，回傳的是 **list**，不是字串 |
| `"".join(chars)` | 把字元 list 接成字串 |
| `"".join(sorted(s))` | 排序後的字串，49 的指紋 |

組字串時先放進 list、最後一次 `join`，不要在 loop 裡 `s += ch`。

## Dict

用 key 查 value，平均 O(1)。要「用什麼去查」就放 key，「查到要拿什麼」就放 value。key 必須不可修改：字串、數字、tuple 可以，list 不行。

| 寫法 | 意思 |
| --- | --- |
| `d = {}` | 空 dict |
| `d[key] = value` | 放進去或覆蓋 |
| `d[key]` | 拿出來，key 不存在會 KeyError |
| `d.get(key, 0)` | 拿出來，不存在就給 0 |
| `key in d` | key 在不在，O(1) |
| `d.values()` / `d.keys()` | 所有 value / key |
| `for k, v in d.items():` | 一對一對走 |
| `list(d.values())` | 轉成 list 回傳 |

計數（242、387、383），四種寫法結果一樣：

```python
# 1. if / else：最直白，先用這個
if ch in count:
    count[ch] += 1
else:
    count[ch] = 1

# 2. get：不存在就當 0
count[ch] = count.get(ch, 0) + 1

# 3. defaultdict：不存在自動是 0，直接 += 1
from collections import defaultdict
count = defaultdict(int)
count[ch] += 1

# 4. Counter：一行數完，面試先問能不能用
from collections import Counter
count = Counter(s)
```

`count[ch] = count.get(ch, 0) + 1` 的順序：先算右邊（讀出舊值 +1），再存到左邊。同樣是 `count[ch]`，在等號右邊是「讀」，在左邊是「寫」。

`count["a"]` 和 `count.get("a")` 拿到的都是數字（`print` 只是顯示出來）。差別只在 key 不存在時：前者 KeyError，後者回傳 None，`get("a", 0)` 回傳 0。

同時拿 key 和 value：

```python
for k, v in d.items():
    rev[v] = k          # key、value 對調
```

**key 重複會被默默覆蓋，不會報錯。** `{"red": 1, "pink": 1}` 對調後只剩 `{1: "pink"}`。要保留全部就用分組，value 放 list。

分組，value 是 list（49）：

```python
if key not in groups:
    groups[key] = []
groups[key].append(s)
```

語法記法：`物件.方法(參數)`，誰的方法誰放前面。方括號 `[]` 是拿東西，圓括號 `()` 是呼叫方法。

## Set

只有 key、沒有 value 的 dict：不重複、沒有順序、查詢 O(1)。只需要知道「有沒有看過」就用 set。

| 寫法 | 意思 |
| --- | --- |
| `a = set()` | 空 set（`{}` 是空 dict） |
| `a = {3, 5}` | 有東西的 set |
| `a.add(x)` | 放進去，重複的不會多一個 |
| `x in a` | 有沒有看過，O(1) |
| `len(set(nums))` | 不重複的個數 |

O(1) 的原因是 hash：用值算出位置直接跳過去，就像交換器查 MAC table。平均 O(1)，碰到 hash collision 會大一些；代價是額外的空間。

## Tuple 與排序

tuple 像不能修改的 list：`t = (3, "a")`，`t[0]` 是 3，`t[1]` 是 "a"。可以當 dict 的 key。

| 寫法 | 意思 |
| --- | --- |
| `pairs.append((c, ch))` | 外層括號是 append，內層是 tuple |
| `pairs.sort(reverse=True)` | 由大到小，原地排序 |
| tuple 排序規則 | 先比第一個元素，一樣才比第二個 |
| `pairs[i][1]` | 先拿第 i 個 tuple，再拿 tuple 的第 1 個（第 i 排、第 1 個座位） |
| `pairs[:k]` | 前 k 個 |
| `for c, ch in pairs[:k]:` | 直接把每個 tuple 拆成兩個變數 |

依次數排序（347）：把 `(次數, 東西)` 放進 list，**次數放前面**，排序時才會依次數排。

```python
pairs = []
for ch, c in count.items():
    pairs.append((c, ch))
pairs.sort(reverse=True)
result = []
for c, ch in pairs[:k]:
    result.append(ch)
```

## 自己跑 Python 檔

- 練習不需要 `class Solution`，從上往下直接寫。LeetCode 用 class 是因為它的評分系統要那樣呼叫
- 寫在 `def` 裡面的程式要被**呼叫**才會執行：`Solution().count_strs()`
- `s.split()`：用空格把句子切成單字 list
- 執行：`python3 檔名.py`；沒輸出時先 `cat 檔名.py` 確認有沒有存檔

## subprocess 與 pytest

```python
def run(node, *cmd):
    return subprocess.run(["docker", "exec", node, *cmd],
                          capture_output=True, text=True)
```

| 寫法 | 意思 |
| --- | --- |
| `def f(node, *cmd)` | 第一個給 node，後面不管幾個全收進 cmd（tuple） |
| `[..., *cmd]` | 把 tuple 攤開放進 list |
| `result.stdout` | 指令的正常輸出 |
| `result.returncode` | 狀態碼：0 成功，非 0 失敗。shell 裡用 `echo $?` 看 |
| `json.loads(result.stdout)` | JSON 字串轉成 list / dict |
| `obj.method()` vs `obj.attr` | 有括號是呼叫方法，沒括號是拿存的值 |

pytest：

| 東西 | 意思 |
| --- | --- |
| `test_` 開頭的檔案和函式 | pytest 自動找到並執行 |
| `assert 條件, "訊息"` | 訊息寫在同一行、用逗號隔開，失敗時會顯示 |
| `return` | **不會讓測試失敗**，測試一定要用 assert |
| `@` decorator | 只作用在正下方那個函式 |
| `@pytest.mark.parametrize("a, b", [...])` | 同一個測試跑多組資料，每組是獨立的 test case；名字要跟函式參數一樣 |
| `@pytest.fixture(scope="session", autouse=True)` | setup；session 整次只跑一次，autouse 自動套用到所有測試 |
| fixture 裡的 `yield` | yield 之前是 setup，之後是 teardown |
| `pytest.fail("...")` 在 fixture 裡 | 報告顯示 **ERROR**（環境有問題），不是 FAILED |
| `python3 -m pytest -v 檔名` | 執行；`-v` 列出每個 case |
| `pytest -m 標記` | 只跑某個 marker 的測試，**不是**執行 pytest 的意思 |

測試設計原則：

- 每個新測試都故意讓它失敗一次，確認它真的有在檢查
- 負向測試要確認「不通的原因」（例如看 ARP 表），不只是「不通」
- 行為測試（通不通）和設定測試（狀態對不對）都要有
- ping 要用資料平面 IP，用到管理網路的 IP 會假通過
- 找東西的變數初始化成 `None`，再 `assert x is not None`，找不到時訊息才清楚

## 解題模式

記模式，不要背 code。複習時先遮住中間欄，自己講出來。

| 題目 | 核心想法 | 時間 / 空間 |
| --- | --- | --- |
| 189 Rotate Array | 先 `k %= n`，把最後 k 個搬到前面 | O(n) / O(n)；三次反轉可到 O(1) |
| 1 Two Sum | dict 存 `數字 → index`，先查再放 | O(n) / O(n) |
| 217 Contains Duplicate | set 記錄看過的數字，先查再放 | O(n) / O(n) |
| 121 Stock | 記錄到今天為止的最低價，每天算一次利潤 | O(n) / O(1) |
| 238 Product Except Self | 左邊乘積 × 右邊乘積，兩個 loop 一前一後 | O(n) / O(n) |
| 242 Valid Anagram | 一個 dict，s 加、t 減，最後全是 0 | O(n) / O(1)（26 字母） |
| 387 First Unique Char | 第一遍數次數，第二遍照原順序找次數 1 | O(n) / O(1) |
| 125 Valid Palindrome | 整理後用左右指標往中間比 | O(n) / O(n)；不整理可到 O(1) |
| 14 Longest Common Prefix | 外層位置、內層字串，不一樣就回傳 `strs[0][:i]` | O(S) / O(1) |
| 49 Group Anagrams | 排序後的字串當指紋，dict 的 value 放 list | O(n·k log k) / O(n·k) |
| 383 Ransom Note | magazine 每個字母的次數 >= ransomNote 的；或 magazine 當庫存，用一個減一個，變負就 False | O(m+n) / O(1) |
| 205 Isomorphic Strings | 兩個 dict 記兩個方向的對應，一次走完，先查再記 | O(n) / O(1) |
| 290 Word Pattern | 先比長度，再用 205 的做法，另一邊換成 split 後的單字 | O(n) / O(n) |
| 347 Top K Frequent | 計數後放 `(次數, 數字)` 排序，取前 k 個；follow-up 用 bucket sort 到 O(n) | O(n log n) / O(n) |

整理出來的通用模式：

- **走一遍、邊走邊記錄**（1、217、121）：只要知道有沒有看過用 set，還要位置用 dict
- **計數**（242、387）：dict 存 `字母 → 次數`
- **分組**（49）：找指紋當 key，value 放 list
- **prefix / suffix**（238）：用前一格的結果算這一格
- **two pointers**（125）：兩端往中間，`while left < right`
- **一對一對應**（205、290）：兩個 dict 各記一個方向，一個 dict 擋不住「兩個不同的對到同一個」
- **計數後排序**（347）：`(次數, 東西)` 的 tuple 排序

## 我的錯誤清單

送出前逐項檢查。同樣的錯會在不同題目重複出現。

- [ ] **位置和數值混用**：`for i in nums` 拿到的是 value，卻拿來當 index（238、49）
- [ ] **變數在 loop 裡被覆蓋**：結果要存進 list，不是每圈 `=`（238、14）
- [ ] **資料變形後還用舊變數**：整理過的 list 要用自己的 `len`（125）；split 之後還用原本的 s（290）
- [ ] **dict 的 value 要存什麼先想清楚**：次數、index、還是對應的東西（205 寫成計數）
- [ ] **if 少了 else**：後面那行每圈都會執行，把結果蓋掉（暖身計數）
- [ ] **複製舊測試沒改完**：名稱、變數、預期值、訊息逐行檢查
- [ ] **assert 檢查錯變數**：`assert port is not None` 永遠通過，等於沒測
- [ ] **容器名稱寫完整**：`clab-lab3-sw1`，不是 `sw1`
- [ ] **手誤**：`vlan` 打成 `vlab`；指令出錯先檢查拼字
- [ ] **資料結構選錯**：查詢用 list 是 O(n)，用 set / dict 是 O(1)（217）
- [ ] **回傳型態不對**：題目要 list 卻回傳 dict 或數字（14、49、238）
- [ ] **會找到自己**：`x in nums` 包含自己，改成先查再放（1、217）
- [ ] **寫特例前先想**：主邏輯能不能自然涵蓋空字串、單一元素（125、49）
- [ ] **語法**：`if` / `for` / `else` 後面的冒號、`==` vs `=`、`*` 不是 `x`、`return` 的縮排位置
- [ ] **自己追兩個測資**：一個會對、一個邊界，再按 Submit
