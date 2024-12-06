import hashlib
# 动态生成包含所有汉字及常见符号的字符集
def generate_chars():
    # 包括所有常见可打印字符（ASCII 32-126）和汉字（\u4E00-\u9FFF）
    allowed_chars = ''.join(chr(i) for i in range(32, 127))  # 包括常见标点符号、数字、字母
    for codepoint in range(0x4E00, 0x9FFF + 1):  # 汉字范围
        allowed_chars += chr(codepoint)
    return allowed_chars

ALLOWED_CHARS = generate_chars()

def generate_shifts(key):
    """生成基于密钥的偏移序列。"""
    return [(ord(char) + index) for index, char in enumerate(key)]

def expandy_sha256(key, length):
    """使用 SHA-256 扩展密钥，截取指定长度。"""
    hash_object = hashlib.sha256(key.encode())
    return hash_object.hexdigest()[:length]

def expand_sha244(key, length):
    """使用 SHA-224 扩展密钥，截取指定长度。"""
    hash_object = hashlib.sha224(key.encode())
    return hash_object.hexdigest()[:length]

def complex_once(text, key_shifts, allowed_chars, encrypt=True):
    """单轮加密或解密操作。"""
    charset_len = len(allowed_chars)
    result = []
    
    for i, char in enumerate(text):
        if char not in allowed_chars:
            result.append(char)  # 非字符集字符直接保留
            continue
        shift = key_shifts[i % len(key_shifts)]
        shift = shift if encrypt else -shift
        idx = allowed_chars.index(char)
        new_idx = (idx + shift) % charset_len
        result.append(allowed_chars[new_idx])
    return ''.join(result)

def decrypt(text, key):
    """执行三轮加密。"""
    # 第一次加密
    key_shifts = generate_shifts(key)
    first_encryption = complex_once(text, key_shifts, ALLOWED_CHARS, encrypt=True)
    
    # 第二次加密（SHA-256扩展密钥）
    extended_key_sha256 = expandy_sha256(key, len(first_encryption))
    extended_shifts_sha256 = generate_shifts(extended_key_sha256)
    second_encryption = complex_once(first_encryption, extended_shifts_sha256, ALLOWED_CHARS, encrypt=True)
    
    # 第三次加密（SHA-224扩展密钥）
    extended_key_sha244 = expand_sha244(key, len(second_encryption))
    extended_shifts_sha244 = generate_shifts(extended_key_sha244)
    final_encryption = complex_once(second_encryption, extended_shifts_sha244, ALLOWED_CHARS, encrypt=True)
    
    return final_encryption

def encrypt(encrypted_text, key):
    """执行三轮解密，顺序与加密相反。"""
    # 第三次解密（SHA-224扩展密钥）
    extended_key_sha244 = expand_sha244(key, len(encrypted_text))
    extended_shifts_sha244 = generate_shifts(extended_key_sha244)
    second_decryption = complex_once(encrypted_text, extended_shifts_sha244, ALLOWED_CHARS, encrypt=False)
    
    # 第二次解密（SHA-256扩展密钥）
    extended_key_sha256 = expandy_sha256(key, len(second_decryption))
    extended_shifts_sha256 = generate_shifts(extended_key_sha256)
    first_decryption = complex_once(second_decryption, extended_shifts_sha256, ALLOWED_CHARS, encrypt=False)
    
    # 第一次解密
    key_shifts = generate_shifts(key)
    original_text = complex_once(first_decryption, key_shifts, ALLOWED_CHARS, encrypt=False)
    
    return original_text
