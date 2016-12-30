def answer(s):
    # your code here
    input1="wrw blf hvv ozhg mrtsg'h vkrhlwv?"
    output1="did you see last night's episode?"
    input2="Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"
    output2="Yeah! I can't believe Lance lost his job at the colony!!"
    input3="ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-="
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dic={}
    for i in range(len(input1)):
        dic[input1[i]]=output1[i]
        dic[output1[i]]=input1[i]

    for i in range(len(input2)):
        dic[input2[i]]=output2[i]
        dic[output2[i]]=input2[i]

    for i in range(len(input3)):
        dic[input3[i]]=input3[i]
    
    for i in alphabet:
        print(i,dic[i])

    out=[]
    
    for i in s:
        out.append(dic[i])

    return ''.join(out)
    
print(answer("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"))
print(answer("wrw blf hvv ozhg mrtsg'h vkrhlwv?"))
