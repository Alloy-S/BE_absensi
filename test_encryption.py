from app.services.encryption_service import EncryptionServiceAES256



result = EncryptionServiceAES256.encrypt("2007-08-27")

# result = EncryptionServiceAES256.decrypt("EdsGYruXsavhu9bzsLjp4G9G1yW8YRWfqj3yQm/0VlYK8Of0H3PPO6OVtqbBdLKnNMjtXR1RXPk+MdDSu462Gg==")

print(result)

