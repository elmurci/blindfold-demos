from blindfold import ClusterKey, SecretKey, encrypt, decrypt

def encrypt_secret(
        secret: str,
        threshold: int,
        cluster_size: int,
        key_type: str = 'cluster',
        key_hex: str = '',
        key_seed: str = ''
    ):
    """Encrypt a secret using Blindfold"""
    if not secret or threshold is None or cluster_size is None or key_type not in ['cluster', 'secret_key'] or (key_type == 'cluster' and not key_hex) or (key_type == 'secret_key' and not key_seed):
        raise ValueError("Missing required parameters: secret, threshold, cluster_size, key_type, key_hex")
    
    # Create cluster
    cluster_obj = {'nodes': [{} for _ in range(cluster_size)]}
    
    # Generate key and encrypt
    if key_type == 'cluster' and key_hex:
        key = ClusterKey.generate(cluster_obj, {"store": True}, threshold)
    elif key_type == 'secret_key' and key_seed:
        key = SecretKey.generate(cluster_obj, {"store": True}, threshold)
    else:
        raise ValueError("Invalid key_type or missing required key parameters")
    
    # key = SecretKey.generate(
    #         cluster,
    #         op,
    #         threshold,
    #         options.seed,
    #     )

    shares = encrypt(key, secret)
    
    return {
        "shares": shares,
        "runtime": "python"
    }

def decrypt_secret(
        shares: list,
        threshold: int,
        cluster_size: int,
        key_type: str = 'cluster',
        key_hex: str = '',
        key_seed: str = ''
    ):
    """Decrypt shares using Blindfold"""
    # Add your decrypt logic here
    cluster_obj = {'nodes': [{} for _ in range(cluster_size)]}
    
    if key_type == 'cluster' and key_hex:
        key = ClusterKey.generate(cluster_obj, {"store": True}, threshold)
    elif key_type == 'secret_key' and key_seed:
        key = SecretKey.fromkeys(cluster_obj, {"store": True}, threshold)
    else:
        raise ValueError("Invalid key_type or missing required key parameters")
    
    result = decrypt(key, shares)
    
    return {
        "result": result,
        "runtime": "python"
    }