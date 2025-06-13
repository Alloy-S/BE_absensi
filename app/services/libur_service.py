from app.repositories.libur_repository import LiburRepository

class LiburService:

    @staticmethod
    def get_libur_pagination(page, size, search):
        return LiburRepository.get_libur_pagination(page, size, search)

    @staticmethod
    def get_libur_by_id(libur_id):
        return LiburRepository.get_libur_by_id(libur_id)

    @staticmethod
    def update_libur(libur_id, data):
        libur = LiburRepository.get_libur_by_id(libur_id)

        return LiburRepository.update_libur(libur, data)

    @staticmethod
    def delete_libur(libur_id):
        libur = LiburRepository.get_libur_by_id(libur_id)
        LiburRepository.delete_libur(libur)

    @staticmethod
    def create_libur(data):
        return LiburRepository.create_libur(data)


