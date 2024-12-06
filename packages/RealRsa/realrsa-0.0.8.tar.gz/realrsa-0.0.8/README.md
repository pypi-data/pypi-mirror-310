# Python RSA加解密封装

解除只能用公钥加密的限制



## 示例

```python
from RealRsa import Rsa


pyrsa = Rsa()

pub_key = """
-----BEGIN RSA PUBLIC KEY-----
xxxxxxxxxxxxxxxxxxxxxxxxxxxx
-----END RSA PUBLIC KEY-----
"""

data = "1bff1dfb66a599777dfe4d5edad268d41866e8f82d9604d6b750e2106b292cf2e11690420f515c3fe06d5fe851dc977e1eb3f0f610881659cb8fbf78e3e0dbc260dd7876146fc2b0e24a059fdf4d9540e8b1f9f755006085f491980248c345da03ff50edb77561bc5a304dc9ab658540cfbed4ebf828a351058abe7af508d5a19fa8dce65955d4f535618cba8fa115454fac166bf53784d51f319a56e3de071d766bda8c1683a74f10c9ee873daa710d233b53bcf8cbf7e0f9e48c13d9a1096ee3971c7c35b1b4bf4a4c6cdb4518c75147d5a21ed17fe161075baad4512ab3d4cf994f1bd5ca983fbf255f65b6a5d321ed68999cbff9b7e1b5dc9fc358d7a247"

ret = pyrsa.pub_decrypt(bytes.fromhex(data), pub_key)
print(ret)

ret = pyrsa.pub_encrypt("23342321",pub_key)
print(ret)
```