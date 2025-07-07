
from cryptography.hazmat.primitives.asymmetric import dilithium
from cryptography.hazmat.primitives import serialization

def generate_quantum_resistant_keys():
    """
    Gera um par de chaves pós-quânticas (Dilithium).
    """
    private_key = dilithium.generate_private_key()
    public_key = private_key.public_key()

    # Serializa as chaves para o formato PEM
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        "private_key": private_pem.decode('utf-8'),
        "public_key": public_pem.decode('utf-8')
    }

def create_quantum_resistant_signature(private_key_pem: str, data: bytes):
    """
    Cria uma assinatura digital usando uma chave privada Dilithium.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None
    )
    
    signature = private_key.sign(data)
    
    return signature

def verify_quantum_resistant_signature(public_key_pem: str, signature: bytes, data: bytes):
    """
    Verifica uma assinatura digital usando uma chave pública Dilithium.
    """
    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8')
        )
        public_key.verify(signature, data)
        return True
    except Exception:
        return False
