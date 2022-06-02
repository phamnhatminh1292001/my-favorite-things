from Crypto.Cipher import AES
from Crypto.Util import Counter
import random
import requests


def encrypt():
    url = "http://aes.cryptohack.org//stream_consciousness/encrypt/"
    r = requests.get(url)
    return r.json()['ciphertext']

def checkmessage(str):
    i=0
    print(bytes.fromhex(str))
    while(i<len(str)):
        s=int(str[i]+str[i+1],16)
        if (s<32 or s>126):
            return False
        i+=2
    return True

def xor(s1,s2):
    str=""
    i=0
    while (i<min(len(s1),len(s2))):
        str+=hex(int(s1[i],16)^int(s2[i],16))[2:]
        i+=1
    return str

list=[]
list2=[]
key=[]
count=0
while count<100:
    t=encrypt()
    if t not in list:
        list.append(t)
    count+=1
first_bytes=b'crypto{'

#make a list for all possible key
for j in list:
    t=xor(first_bytes.hex(),j[0:14])
    list2.append(t)
#for each possible key, check if when we xor with other ciphertext, 
# it will return a legal message
for i in list2:
    found=True
    for j in list:
        t=xor(i,j[0:14])
        if not checkmessage(t):
            found=False
            break
    if found==True:
        key.append(i)

for i in list:
    m=xor(key,i[0:14])
    msg={'text':bytes.fromhex(m),'text_hex':m,'cipher_hex':i}
    print(m)

#the rest is just decrypt these message until you find the key
found_key='9c93e4116e3ab156'
msg_list=[]
msg={'text': b"I'm unhappy, I deserve it, the f", 'tex_hex': '49276d20756e68', 'cipher_hex': 'd5b489311b54d9371d6bc63015f6356e62aa73379f547825f762b6d39438aa3203b95a6cee2e786be780ed46c50982106d6727117ef6f2dec5c52e19c7edc38b49bee8693d439d2e0ccea285b7a62cf764971e'}
msg2={'text': b"Dolly will think that I'm leavin", 'tex_hex': '446f6c6c792077', 'cipher_hex': 'd8fc887d171ac63f01779f685dd67b6127ad7e249d11116bee6efac29d2be33a05ec5738ba383b69e08aa80290189505234a201d30e7bcc2ccd42a4093e4ca950cacef7e7810b5630497f199f2b929a56c9e496f1d68c55805b8cc5141a05a1df6039f6e'}
msg3={'text': b'Three boys running, playing at th', 'tex_hex': '54687265652062', 'cipher_hex': 'c8fb96740b1ad33914689f6e40d17b6369be3a65995d3935ea20f1879d29aa3c0dbe457dba717855eb9cf1059f039645'}
msg4={'text': b'Perhaps he has missed the train ', 'tex_hex': '50657268617073', 'cipher_hex': 'ccf696790f4ac276057e9f7454cc35676eaa65208d112c24e66ee2d59d34e47403a25238a02e7864ef8de34a8712d70a22592e5c09e2f2c284d8311282acc79204a3ec657c44952c07c3'}
msg5={'text': b'What a nasty smell this paint ha', 'tex_hex': '57686174206120', 'cipher_hex': 'cbfb85654e5b91380c68cb6515cc786f6bb5363181582b6cf32fffc9887de23506e2'}
msg6={'text': b"It can't be torn out, but it can", 'tex_hex': '49742063616e27', 'cipher_hex': 'd5e7c4720f5496224d79da3c41d0676427b66331c5113a39f76effd3dc3eeb3a42ae5338a03a3669fc8bec44'}
msg7={'text': b"No, I'll goin toolly and tell", 'tex_hex': '4e6f2c2049276c', 'cipher_hex': 'd2fcc831271ddd3a4d7cd03c5cd1357e68f9522a855d216ce220f2878838e63842a4536ae92e2c74ef87ef02914b981139'}
msg8={'text': b'The terrible thing is that the p', 'tex_hex': '54686520746572', 'cipher_hex': 'c8fb81311a5fc3240479d37915cb7d6369be362c9a112c24e23ab6d39438aa2403bf4238aa3c3621faceea0fc51f9816230e6f092aa3fecf84dc2a13c7fec0881db9ae'}
msg9={'text': b'Our? Why our?', 'tex_hex': '4f75723f205768', 'cipher_hex': 'd3e6962e4e6dd92f4d74ca6e0a'}
msg10={'text': b"I shall, I'll lose everything if", 'tex_hex': '49207368616c6c', 'cipher_hex': 'd5b397790f56dd7a4d529870599f796574bc36209f542a35f726ffc99b7de33242a45338ad323d75e0c9fc4a86049a016d4c611f35ad'}
msg11={'text': b'What a lot of things that then s', 'tex_hex': '57686174206120', 'cipher_hex': 'cbfb85654e5b913a026f9f73539f61626eb77136c945302df76ee2cf9933aa2707a95b7dad7d2c69ae83ed4a9604d7092c5c761932eff3c3d7953f0e83acda8908bef46d745e9d210587aecdbaab2ab22990552c1060801102f6cb5043ee4409f00e992e0a987bc5f3aac872135dd0c884aac81724262fbc252d721052a1d3352ad4eff087fde08f86a3734e21537b45a77787a13662e2090be118856ef4a7'}
msg12={'text': b'As if I had any wish to be in th', 'tex_hex': '41732069662049', 'cipher_hex': 'dde0c478081af876057adb3c54d16c2a70b0652dc945376ce12bb6ce927dfe3c07ec4471ae352c27aea7a8098405d0106c'}
msg13={'text': b'Dress-making and Millinery', 'tex_hex': '44726573732d6d', 'cipher_hex': 'd8e181621d17dc370672d17b15de7b6e27947f2985583629f137'}
msg14={'text': b'And I shall ignore it.', 'tex_hex': '416e6420492073', 'cipher_hex': 'ddfd8031271ac23e0c77d33c5cd87b6575bc362c9d1f'}
msg15={'text': b'But I will show him.', 'tex_hex': '42757420492077', 'cipher_hex': 'dee69031271ac63f01779f6f5dd0622a6fb07b6b'}
msg16={'text': b'crypto{k3y57r34m_r3u53_15_f474l}', 'tex_hex': '63727970746f7b', 'cipher_hex': 'ffe19d611a55ca3d5e628a2b478c216758ab2530dc02077db611f093cb69e629'}
msg17={'text': b'I shall lose everything and not', 'tex_hex': '49207368616c6c', 'cipher_hex': 'd5b397790f56dd760174cc7915da636f75a0622d805f3f6ce220f2879232fe7405a94238a1343526ec8feb01cb'}
msg18={'text': b'Why do they go on painting and b', 'tex_hex': '57687920646f20', 'cipher_hex': 'cbfb9d310a559122057ec63c52d0356569f96624805f2c25ed29b6c69239aa3617a55a7ca0333f26ef82e44a9103924439476d1961'}
msg19={'text': b"Love, probably? They don't know ", 'tex_hex': '4c6f76652c2070', 'cipher_hex': 'd0fc9274421ac1240279de7e59c62a2a53b1733cc9553722a43ab6cc9232fd740aa34138ad2f3d67fc97a803914b9e17610e681329a3f4c3c9dc320986f8c6890ee4ae223d44942649a3f488bcbf39f7689c546f1c658c5d0feadd570a'}
msg20={'text': b"How proud and happy he'll be whe", 'tex_hex': '486f772070726f', 'cipher_hex': 'd4fc93311e48de23093bde72519f7d6b77a96f6581547f20ef6ef4c2dc2ae2310cec5e7de93a3d72fdcee513c5059810280f'}
msg21={'text': b'Would I have believed then that ', 'tex_hex': '576f756c642049', 'cipher_hex': 'cbfc917d0a1af876057ac97915dd70666ebc60208d112c24e620b6d3943cfe742bec5577bc313c26fc8be9098d4b84112e4620183bf3e8ded7953106c7e4da8a00a6e96d6959932d56'}
msg22={'text': b'These horses, this carriage - ho', 'tex_hex': '54686573652068', 'cipher_hex': 'c8fb81620b1ad9391f68da6f199f61626eaa362688432a25e229f387d17de23b15ec7f38a5323972e68ba8079c1892082b0e69127ef7f4dfd7953d0195fec6860eafa0213d44942610c5f088f2ab30bb299a593c442d87441fb8f11957e84c03f54d962508d12984eeab8d260f5095d1cca2c1113e6848'}

msg_list+=[msg,msg2,msg3,msg4,msg5,msg6,msg7,msg8,msg9,msg10,msg11,msg12,msg13,msg14,msg15,msg16,msg17,msg18,msg19,msg20,msg21,msg22]

