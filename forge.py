# This is the framework file for your programming assignment. Complete the three functions selective_forge, universal_forge and md_forge towards the bottom of the file and upload to Gradescope.

#------------------CODE FOR MAC------------------------------------
KEY_ROWS = KEY_COLS = 16

def MAC_check(msg):  
    if (type(msg) != tuple or len(msg) != 2): 
        raise Exception("Input msg must be a tuple of length 2") 
    if (type(msg[0])!=int or type(msg[1])!=int):
        raise Exception("Elements of the tuple must be integers")
    if (not(0<=msg[0]<KEY_ROWS and 0<=msg[1]<KEY_COLS)): 
        raise Exception(f"The msg must be of the form (m, n) where 0<=m<{KEY_ROWS} and 0<=n<{KEY_COLS}") 
    

def sample_MAC(msg):
    MAC_check(msg)
    key = [[(i+(10*j))%101 for i in range(KEY_COLS)] for j in range(KEY_ROWS)]

    m, n = msg 
    s, t = (0, 0)

    for row in key[:m+1]:
        s+=row[n]

    for element in key[m][:n+1]:
        t+= element 

    return (s, t)
#---------------------------------------------------------------------
#---------------------CODE FOR HASH-AND-MAC---------------------------

def MD_check(msg):
    if (type(msg) != list or len(msg) > 2**16 or len(msg) == 0): 
        raise Exception("Input msg must be a list of length greater than 0 and less than 2**16")
    for i in msg:
        if (type(i) != int or not(0<=i<256)):
            raise Exception("Elements must be integers between 0 and 255, both inclusive")
   

def MD_pad(msg):
    ln = len(msg)
    num_zeros = (6 - ((ln+3)%6))%6
    pad = msg + [1] + [0 for i in range(num_zeros)] + [ln//256, ln%256]
    return pad

def MD_hash(pad):
    def h(x, z):
        new_z = [0] * 6
        for i in range(6):
            new_z[i] = ((z[i]*x[i])%256 + x[(i+1)%6])%256
        return new_z
    
    z = [17 for i in range(6)]

    for i in range(len(pad)//6):
        z = h(pad[i*6:i*6+6], z)
    
    return z


def MD_tag(hash):
    tag = [0] * 6
    for i in range(6):
        tag[i] = sample_MAC((hash[i]//16, hash[i]%16))
    return tag

def sample_MD(msg):
    MD_check(msg)

    pad = MD_pad(msg)
    hash = MD_hash(pad)
    hashtag = MD_tag(hash)
    return hashtag

#-----------------------------------------------------------------------
#------------COMPLETE THE FOLLOWING FUNCTIONS----------------------------
     
def selective_forge(MAC): 
    # In this task, you must return a msg of your choice with a valid tag that would be produced by running the MAC protocol specified by sample_MAC
    # You may query MAC for any message different from the one you return. 
    # Completion of the task with fewer queries is worth more points!
    # Below is an example that does not work!
    tag1 = MAC((1, 0))
    tag2 = MAC((0, 1)) 
    # s1, t1 = tag1
    s2, t2 = tag2
    forged_msg = (0, 0)
    forged_s = t2 - s2 
    forged_t = t2 - s2 
    return (forged_msg, (forged_s, forged_t))

def universal_forge(MAC, msg):
    # In this task, you must return the valid tag for the input message that would be produced by running the MAC protocol specified by sample_MAC
    # You may query MAC for any message different from the input. 
    # Completion of the task with fewer queries is worth more points!
    # Below is an example that does not work!
    m, n = msg
    if m == 15 and n == 15:
        return None
    if m < 15 and n < 15:
        if m > 0 and n > 0:
            s4, t4 = MAC((m - 1, n - 1))
            s5, t5 = MAC((m, n - 1))  
            s6, t6 = MAC((m - 1, n))
            return (s6 + t5 - t4, t6 + s5 - s4)
        else:
            if m == 0 and n == 0:
                s1, t1 = MAC((0, 1))
                s2, t2 = MAC((1, 0))
                return (t1 - s1, t1 - s1)
            elif m == 0:
                s1, t1 = MAC((0, n - 1))
                s3, t3 = MAC((0, n + 1))
                return (t3 - s3 - t1, t3 - s3)
            else:  # n == 0
                s1, t1 = MAC((m - 1, 0))
                s3, t3 = MAC((m + 1, 0))
                return (s3 - t3, s3 - t3 - s1)
    elif m == 15:
        if n > 0:
            s4, t4 = MAC((14, n - 1))
            s5, t5 = MAC((15, n - 1))
            s6, t6 = MAC((14, n))
            return (s6 + t5 - t4, t6 + s5 - s4)
        else:  # n == 0, m == 15
            s1, t1 = MAC((14, 0))
            s2, t2 = MAC((15, 1))
            return (2*s1 - s2 + t2, t2 + s1 - s2)
    
    else:  # n == 15
        if m > 0:
            s4, t4 = MAC((m - 1, 14))
            s5, t5 = MAC((m, 14))
            s6, t6 = MAC((m - 1, 15))
            return (s6 + t5 - t4, t6 + s5 - s4)
        else:  # m == 0, n == 15
            s1, t1 = MAC((0, 14))
            s2, t2 = MAC((1, 15))
            s3, t3 = MAC((1, 14))
            return (s1 + t2 - t3, t1 + s2 - s3)

def md_forge(MD):
    # In this task, you must return a msg of your choice with a valid tag that would be produced by running the Hash-and-MAC protocol specified by sample_MD
    # You may query MD for any message different from the one you return. 
    # Completion of the task with fewer queries is worth more points!
    # Below is an example that does not work!
    msg1 = [1, 1, 0, 0, 0, 1]
    tag1 = MD(msg1)
    msg2 = [1] 
    return (msg2, tag1)  

#-----------------------------------------------------------------------

def main():
    select_msg, select_tag = selective_forge(sample_MAC)
    print("The selected msg for MAC is: ", select_msg)
    print("The selected tag for MAC is", select_tag)
    print("The actual tag for the selected msg for MAC is", sample_MAC(select_msg))

    forged_tag = universal_forge(sample_MAC, (5,6))
    print("The forged tag for MAC is:", forged_tag)
    print("The actual tag for MAC is:", sample_MAC((5,6)))

    md_select_msg, md_select_tag = md_forge(sample_MD)
    print("The selected msg for MD is: ", md_select_msg)
    print("The selected tag for MD is", md_select_tag)
    print("The actual tag for the selected message for MD is", sample_MD(md_select_msg))



if (__name__ == "__main__"):
    main()