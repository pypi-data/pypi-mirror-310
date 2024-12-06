from RealRsa import Rsa
import unittest


class TestCryto(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.rsa = Rsa()
        cls.pubkey = """
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAsbVa8N3Fv6GDACU4UCBvEsFRJ4PcL6RR6L53j4cvkccrxK572sTG
CWTCKkgt08Op/somc6SgbnzL5HwnuKb5uoPqAVkPG796yKTvSADju/NJUEhWxya2
qOOL6hWcmYmREnpiJVxdKy+0WyXaQ2j7aDnUQk6J5MtgOuRgzaR4uezS31YNFIqo
QubEzPowjwEvv2A6DPsHYqrBHBUOpBeJCEG1BaQ4GS49U2mT3WCNsnj+7nPGs6io
Hz9hJ0suJasCor91URLG2TGWFs4z0joXHXUh+Cbw79tRaByHgywWKvJlVzwjiR2L
ezpE77O8cGWm5DmSseLsaekmvOoqWIoK0wIDAQAB
-----END RSA PUBLIC KEY-----"""

        cls.prikey="""
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAsbVa8N3Fv6GDACU4UCBvEsFRJ4PcL6RR6L53j4cvkccrxK57
2sTGCWTCKkgt08Op/somc6SgbnzL5HwnuKb5uoPqAVkPG796yKTvSADju/NJUEhW
xya2qOOL6hWcmYmREnpiJVxdKy+0WyXaQ2j7aDnUQk6J5MtgOuRgzaR4uezS31YN
FIqoQubEzPowjwEvv2A6DPsHYqrBHBUOpBeJCEG1BaQ4GS49U2mT3WCNsnj+7nPG
s6ioHz9hJ0suJasCor91URLG2TGWFs4z0joXHXUh+Cbw79tRaByHgywWKvJlVzwj
iR2LezpE77O8cGWm5DmSseLsaekmvOoqWIoK0wIDAQABAoIBAC47ek9TwxCZ2lT9
WesupPcCKDTZjz0tyMl+U+iZSPzqDi77HenKa6Mh/Ym2gYWoT9+jg+FuIPbdrMXi
rwrRFgM6MnTrUIztgeoVTtMyuAy7vIUQbNMe9UJ3AH2D5dvj+EQQZtxFbU/A93EH
JgOHmnCBKwGdIS7O4lgv9idJ9MaZsT49lY4j6JYsGoBeLXi5daDnAPw7hAEX4tF2
BlZ1aRGeFsxRW6SEwTQ+MLpfzRgQbtw9Cf2zHFFNvkoP1UMJ5HA4JKbSFtefgNo6
X1UsToDBGhettxnh+RRtLri23hHM6ym7amQ2YUc8+QeR5XZUoDvCZYG+o7aV9PUS
IHntsfECgYEA0zPqiz/ma0HJpacyJqGfkV5y9Kv3srMA1SwOIS8unAIjvUW7RHHe
29esI9HKW/Xp/QzykU5UTblTYLwNYu1fsIbtl5uwUkw1mQrdXtFKdUloHO9RZfvh
HMYUHbRaEkEQyPaGNdNMX8RcknjiCF/leAUegsFql3aXjaHIxSrqGXcCgYEA12a6
/3KLNoRNMEHZP3xtUyZUg3YGqRbn/lr6lqon2CsJJrWbiWliNp3VFhGlCWjA/gbs
Oso91LOL+VW9EXm19nUeRxEkoUTJ5HTnplCb+a2eh3CtrqJIDqPM99FwaIB2qXX2
dbBHtENt9Dhf0RHCuDhIiaVlAEeGowAOyKofsIUCgYB4tFAUe1Wl8Phcuxx3ZaF7
hD4wxWOP9qvAKSh+IKgDs1lXn9Wx/V4/yJfx9MExI28yF0c+ckTOEt+rBm6kHkO0
8LgzEGCJ+FIdgE8aFIT4WRauiru7jGOQfUgb3eooSpVcNUBo3LTmeqPpdjrATIYp
vMs+MWpI3Bcrc835mVgnawKBgG+nJZlSE41fyO8Rwv3gjn7CaJ54KH2vjPPQzwIY
E20+6ZByJLx2rt0mtRSqcsTM0vUaO4tB2AkQRKcq5UVQtJybGuW1oioiERDl9EnG
kQM8FueX5b+XCQjlqVJv8veIV3oB1o4soQ50wWMNccVakneRXTBUVmVtrgGB/yfO
33xNAoGAeHbozOqdP3KDsC0fY4FFfQTfWw5FyMOkO1g7jklsZjIgR1gcDxn9u/7y
q/e52HBJ8T48uvIaWQqWzkx5uNAPGHkux1+HXbdGeocLMqF53XufeucrBFjweAUB
c6KUpqKdAjotmACEpjUFIGqHXAiMKJnEGHaaEdmlrLXgRfODaCk=
-----END RSA PRIVATE KEY-----"""

        cls.plaintext = "just a test"

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_genkey(self):
        ret = self.rsa.genkey()
        self.assertTrue(len(ret) == 2)
        
    
    def test_rsa_pri_en_pub_de(self):
        ret = self.rsa.pri_encrypt(self.plaintext,self.prikey)
        ret = self.rsa.pub_decrypt(ret, self.pubkey)
        self.assertTrue(self.plaintext == ret.decode("utf-8"))

    def test_rsa_pub_en_pri_de(self):
        ret = self.rsa.pub_encrypt(self.plaintext,self.pubkey)
        ret = self.rsa.pri_decrypt(ret, self.prikey)
        self.assertTrue(self.plaintext == ret.decode("utf-8"))