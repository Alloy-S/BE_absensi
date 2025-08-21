from app.services.encryption_service import EncryptionServiceAES256



result = EncryptionServiceAES256.encrypt("2025-05-07")

# result = EncryptionServiceAES256.decrypt("l+A+BHG6FV0t0L8DDno1wbX0aPbDW4wkhmMXVEkw1B1rD0CaH3imgoz3MFy1WSINGq4aiPH/KVTgoSfshv4utA==")

print(result)

