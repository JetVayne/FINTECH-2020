# Seshat & Co-occurrence Matrix Graph

## Seshat - A pdf to JSON convert-tool on Python 3

### Intro
當初看到這個作業，我一直很想要試試能否用個方法去分析論文，而由於是要分析與 BMI 相關之論文，所以 Data 勢必不多，
所以希望能從資料中獲取更多的資訊，於是自己刻了一個 Pdf 轉 JSON 的工具(自己刻是因為網路上的套件都寫得很糟而且不能用)，將 Pdf 轉成樹狀結構，訴求重點為: 將Outline(子標題) 萃取出來，做為一個 KEY ，而其對應的 Value 為該 Outline 的內文(這也是目前的open-src欠缺的，大都只能無序的提取文字)，大部分開源套件，無法做到子標題與內文對應

最後大部分的檔案都能正確的轉成 JSON 結構，但是後來卻發現我無法拿這點繼續往下利用，花了非常多時間做這個工具，卻無法利用以結構化的優勢的到更多 Data Info ，這有點可惜

### Work Flow
Get Pdf Object > Covert to MarkDown Structure > Extract Outline > Parse to JSON Structure

### Installation
- pip3 install -r requirements.txt

### How to Use
Beware you are at the same dir of seshat.py
```python=3.7
from seshat import Seshat

# the directory path with the pdf-files that you want to convert
paper_dir = 'paper'

seshat = Seshat(paper_dir)
seshat.launch()


```

## Data Structure of Output JSON
### PaperJson
    - ['Title'] -> String
    
    - ['Author'] -> String
    
    - ['Subject'] -> String
    
    - ['KeyWords'] -> JSON Array
    
    - ['Outlines'] -> JSON Array
    
        - {Outline} -> JSON Object
        
            - ['index'] -> Int 
            
            - ['name'] -> String
            
            - ['type'] -> String
            
            - ['level'] -> Int
            
            - ['content'] -> String
            
            - ['detail'] -> String
    
    - ['Date'] -> YYYY-MM-dd
    
    - ['HasInfo'] -> Boolean
    
    - ['HasOLF'] -> Boolean
    
    - ['ForceSplit'] -> Boolean


### Co-occurrence Matrix Graph


使用 Seshat 生成 JSON > 利用 Stanza 斷詞並為 Term 做權重排序 > Plotly 繪製
