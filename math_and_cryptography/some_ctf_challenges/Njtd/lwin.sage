s="00101101100100011101101110000000101100001110110001011110110011011011011011001111111101111101011111010000001011000011111010110011010111000100110010101100101000011000111010110011110011001001000101010010011100001011100101010000111100001010101001100010101110110110111000111010000011000000000010110101011011011111100100010100101100110000111010001101010111010010011110000110110010100010011101111111101001111101001100110110111110100101000010000000000010000000100100001110001110100001100111111010110010010110000000001110101101011001011011001101001010000000100010011001000100111000110100101011101001100110010110010011100010011101010000010101010001111110101010111001111000111111011011101011100011010101011010110001101110110101111001101110010100010110100100000000100000111000110010101100111111101001100111110000101011100111110010001111100000110110110110010101101110111100101010011000100110001000110011111110011110111001100110001011111111111011010010010110010011101011001010010101011001010100110001001111111000110011010101011011010110000101011011001100100000000000011111110101001100011001110000101110001101011011110000100111100010111110101101101010100110100010011001000110010100000001110010011001111110010001110110110100000001110110111011010100100111011011100001110100001110101111010100110101110100111111101100011010110011111111100011101110001111011100000000100110010111100100110100011000110110001001011111110000111001110010010111101000100011100101001111101011011011111011100011000001011011101111101111011011101011101110011011111001011101101100111111000000100000100011111101110100110100000111010001101100011000100000100010010111101111011000001011110101001010001000001001000111101110101001010110101101101010001110000001000001011110001011100011011010010110011011111111110010111101011111111101111110001100101001011010110001000001000111000101010100001000000101000100011100111001100111010010100101100100101001010100001100111001011111110011000000110000110101101000001110100101110011110001111000001111000100111000111011010100101000001101111100011011000111010001110110"
arr=[int(i) for i in s]
l=384
M=Matrix(GF(2),l,l)
for i in range(0,l):
    M[i]=arr[i:i+l]
v=vector(GF(2),arr[l:2*l])
SECRET=[0,6,15,16]
arr.reverse()
arr+=[0]*(16*48)
for i in range(2048,2048+16*48):
    arr[i]=(arr[i-6]+arr[i-15]+arr[i-16]+arr[i-384])%2
arr.reverse()
arr=arr[:384]
bi=""
for i in arr:
    bi+=str(i)
dec=int(bi,2)
he=hex(dec)[2:]
flag=bytes.fromhex(he)
print(flag)