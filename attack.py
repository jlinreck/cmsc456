import sys
import random
def check_byte(num, name):
    """
    Checks if the input is a byte. Name is used to report where the error is.
    """
    if type(num) != int or num < 0 or num > 255:
        raise Exception(name + ' is not a byte.')
        check_result = False
    else:
        check_result = True
    return check_result
def check_byte_list(list_to_check, length, name):
    """
    Checks if the provided list (list_to_check) is actually a list of bytes of the
    specified length. If length is 0 then the list can be any length except *not*
    empty. Name is used to report where the error is.
    """
    check_result = True
    if type(list_to_check) != list:
        raise TypeError(name + ' is not a list.')
        check_result = False
    elif length != 0 and len(list_to_check) != length:
        raise Exception(name + ' has ' + str(len(name)) + ' entries instead of ' + str(length))
        check_result = False
    elif length == 0 and len(list_to_check) == 0:
        raise Exception(name + ' is empty.')
        check_result = False
    else:
        entry_name = 'entry of ' + name
        for j in list_to_check:
            if not check_byte(j, entry_name):
                check_result = False
    return check_result
def init(IV, k):
    """
    Initializes the stream cipher with input IV (the initial value), which is a list
    of
    256 entries, each of which is an integer from 0 to 255, and k, which is a list of
    some number of integers from 0 to 255. Init returns a tuple (i, state), with i
    an
    integer from 0 to 255 and state a list of 256 entries, each of which is itself a
    number from 0 to 255. These will comprise the internal state of the stream
    cipher.
    """
    # Look for errors in input format:
    check_byte_list(IV, 256, 'IV')
    check_byte_list(k, 0, 'key')
    # Initialize output variables:
    i = 0
    state = list(IV)
    # Apply key transformations to state:
    for j in k:
        if j > 0:
            for t in range(j):
                shift = state.pop(0)
                state.append(shift)
    return (i, state)
def next(i, state):
    """
    Produces a single byte from the stream cipher. Takes as input a single number i
    between 0 and 255 and a state of 256 bytes. It returns j, an updated value of i
    and
    state following an x which is the product of the stream cipher.
    """
    # Look for errors in input format:
    check_byte_list(state, 256, 'state')
    check_byte(i, 'i')
    # Run next:
    x = state[i]
    j = (i + state[(i + 1) % 256]) % 256
    return (x, j, state)
def enc(IV, k, m):
    """
    Given input IV, the initial value (which should be a list of 256 random numbers
    between 0 and 255), k, the key (a list of any length of numbers between 0 and
    255),
    and m, the message to be encrypted (given as a list of any length of numbers
    between
    0 and 255), returns a ciphertext c in the form of a list of numbers between 0 and
    255.
    Note that IV is supposed to be random; in principle, the enc function should be
    generating it randomly itself, but I have put IV as an input for more
    flexibility.
    The default length for k is 16 bytes, but the algorithm doesn't check or make use
    of
    that. The encrypt a text message, it should be first converted to a list of
    bytes,
    e.g., the ASCII encoding of the characters.
    """
    # Look for errors in input format:
    check_byte_list(IV, 256, 'IV')
    check_byte_list(k, 0, 'key')
    check_byte_list(m, 0, 'message')
    # Initialize stream cipher and ciphertext. The ciphertext begins with the IV:
    (i, state) = init(IV, k)
    c = list(IV)
    # Get one byte from the stream cipher and use it to encode one byte of the message:
    for b in m:
        (x, i, state) = next(i, state)
        c.append((x + b) % 256)
    return c
def dec(k, c):
    """
    Takes as input k, the key (a list of any length of numbers between 0 and 255),
    and c,
    the ciphertext (a list of any length of numbers between 0 and 255). Returns a
    message m (a list of numbers between 0 and 255) decrypted from the ciphertext
    with
    that k.
    """
    # Look for errors in input format:
    check_byte_list(k, 0, 'key')
    check_byte_list(c, 0, 'ciphertext')
    if len(c) <= 256:
        print('Error: ciphertext is too short.')
    # Determine IV, which is the first 256 bytes of the ciphertext:
    IV = c[0:256]
    # Initialize stream cipher and message list:
    (i, state) = init(IV, k)
    m = []
    # Decrypt by getting one byte at a time from the stream cipher:
    # We can start in the ciphertext at spot 256, after the IV is done
    for b in c[256:]:
        (x, i, state) = next(i, state)
        m.append((b - x) % 256)
    return m

def PRG_attack(IV, x):
    """ Complete this function! given an Initial Value [list of 256 bytes] to the
    Cipher `IV` and a byte stream `x` [list of bytes of variable length], return 1 if
    the `x` is random, and 0 if pseudorandom (generated by the stream cipher)."""
    for key_byte in range(256):
        key = [key_byte]
        (i, state) = init(IV, key)
        generated_bytes = []
        currI = i
        currentState = state[:]
        for _ in range(len(x)):
            (output_byte, currI, currentState) = next(currI, currentState)
            generated_bytes.append(output_byte)
        if generated_bytes == x:
            return 0
    return 1

def EAV_choose(length):
    """ Complete this function! Given a length, return two different messages
    (lists of bytes) of the given length."""
    m0 = [0 for i in range(length)]
    m1 = [255 for i in range(length)]
    return (m0, m1)

def EAV_attack(m0, m1, c):
    """ Complete this function! Given the two messages selected by you, and the
    ciphertext c, return 0 if the ciphertext is an encryption of the message m0, and 1
    if the ciphertext is an encryption of the message m1 """
    IV = c[0:256]
    encrypted_message = c[256:]
    for key_byte in range(256):
        key = [key_byte]
        try:
            (i, state) = init(IV, key)
            generated_stream = []
            current_i = i
            current_state = state[:]
            for _ in range(len(encrypted_message)):
                (x, current_i, current_state) = next(current_i, current_state)
                generated_stream.append(x)
            if generated_stream == encrypted_message:
                return 0
        except:
            continue
    return 1

def decrypt(m_list,c):
    """ Complete this function! Given a list m_list of possible messages and the
    ciphertext c, return i if the ciphertext is an encryption of m_list[i]."""
    IV = c[0:256]
    encrypted_message = c[256:]
    for message in range(len(m_list)):
        currMessage = m_list[message]
        if len(currMessage) != len(encrypted_message):
            continue
        pseudorandom = []
        for i in range(len(currMessage)):
            pseudorandom_byte = (encrypted_message[i] - currMessage[i]) % 256
            pseudorandom.append(pseudorandom_byte)
        stream_found = False
        for key_byte in range(256):
            key = [key_byte]
            try:
                (i, state) = init(IV, key)
                generated_stream = []
                current_i = i
                current_state = state[:]
                for _ in range(len(pseudorandom)):
                    (x, current_i, current_state) = next(current_i, current_state)
                    generated_stream.append(x)
                if generated_stream == pseudorandom:
                    stream_found = True
                    break
            except:
                continue
        if not stream_found and len(pseudorandom) > 10:
            for byte1 in range(0, 256, 16): 
                for byte2 in range(0, 256, 16):
                    key = [byte1, byte2]
                    try:
                        (i, state) = init(IV, key)
                        generated_stream = []
                        current_i = i
                        current_state = state[:]
                        for _ in range(len(pseudorandom)):
                            (x, current_i, current_state) = next(current_i, current_state)
                            generated_stream.append(x)
                        if generated_stream == pseudorandom:
                            stream_found = True
                            break  
                    except:
                        continue
                if stream_found:
                    break
        if stream_found:
            return message
    return 0
