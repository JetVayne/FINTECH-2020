# Seshat
# A pdf to JSON convert-tool on Python 3

## Installation
- pip3 install -r requirements.txt

## How to Use
Be ware you are at the same dir of seshat.py
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


    