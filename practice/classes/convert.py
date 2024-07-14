# altered from https://github.com/aleckretch/Romaji-to-Japanese-Converter

hiragana = {'a':'あ','i':'い','u':'う','e':'え','o':'お',
    'ka':'か','ki':'き','ku':'く','ke':'け','ko':'こ',
    'ga':'が','gi':'ぎ','gu':'ぐ','ge':'げ','go':'ご',
    'sa':'さ','shi':'し','su':'す','se':'せ','so':'そ',
    'za':'ざ','ji':'じ','zu':'ず','ze':'ぜ','zo':'ぞ',
    'ta':'た','chi':'ち','tsu':'つ','te':'て','to':'と',
    'da':'だ','zu':'づ','de':'で','do':'ど',
    'na':'な','ni':'に','nu':'ぬ','ne':'ね','no':'の',
    'ha':'は','hi':'ひ','fu':'ふ','he':'へ','ho':'ほ',
    'ba':'ば','bi':'び','bu':'ぶ','be':'べ','bo':'ぼ',
    'pa':'ぱ','pi':'ぴ','pu':'ぷ','pe':'ぺ','po':'ぽ',
    'ma':'ま','mi':'み','mu':'む','me':'め','mo':'も',
    'ya':'や','yu':'ゆ','yo':'よ',
    'ra':'ら','ri':'り','ru':'る','re':'れ','ro':'ろ',
    'wa':'わ','wo':'を',
    'n':'ん',
    'kya':'きゃ','kyu':'きゅ','kyo':'きょ',
    'gya':'ぎゃ','gyu':'ぎゅ','gyo':'ぎょ',
    'sha':'しゃ','shu':'しゅ','sho':'しょ',
    'ja':'じゃ','ju':'じゅ','jo':'じょ',
    'cha':'ちゃ','chu':'ちゅ','cho':'ちょ',
    'nya':'にゃ','nyu':'にゅ','nyo':'にょ',
    'hya':'ひゃ','hyu':'ひゅ','hyo':'ひょ',
    'bya':'びゃ','byu':'びゅ','byo':'びょ',
    'pya':'ぴゃ','pyu':'ぴゅ','pyo':'ぴょ',
    'mya':'みゃ','myu':'みゅ','myo':'みょ',
    'rya':'りゃ','ryu':'りゅ','ryo':'りょ',
    'vu':'ゔ',
    'small-tsu':'っ'}

def romajiToJapanese(romaji):
    romaji = romaji.lower()
    resultStr = ''
    i = 0
    
    while i < len(romaji):
        if (i+2) < len(romaji) and romaji[i] == 'n' and romaji[(i+1):(i+2)] == 'n' and romaji[(i+1):(i+3)] not in hiragana: 
            resultStr += hiragana['small-tsu']
            i += 1
        else:
            checkLen = min(3, len(romaji) - i)
            
            while checkLen > 0:
                checkStr = romaji[i:i+checkLen]
                
                if checkStr in hiragana:
                    resultStr += hiragana[checkStr]
                    i += checkLen
                    
                    if (i < len(romaji)):
                        if romaji[i] == 'o' and romaji[(i-1):i] == 'o':
                            resultStr += hiragana['u']
                            i += 1
                            
                        elif romaji[i] == 'e' and romaji[(i-1):i] == 'e':
                            resultStr += hiragana['i']
                            i += 1
                    break
                  
                elif checkLen == 1:
                    if checkStr not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']: 
                        resultStr += checkStr
                        
                    elif (i+1) < len(romaji): 
                        if checkStr == romaji[(i+1):(i+2)]:
                            resultStr += hiragana['small-tsu']
                    i += 1
                    break	
                  
                checkLen -= 1
                
    return resultStr