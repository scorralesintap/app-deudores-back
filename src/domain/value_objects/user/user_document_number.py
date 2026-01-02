class UserDocumentNumber:

    def __init__(self, document_number: str):
        self._validate(document_number)
        self._document_number = document_number.strip()

    def _validate(self, document_number: str):
        if not document_number or document_number.strip() == "":
            raise ValueError("El número de documento del usuario es obligatorio")
        if len(document_number) < 6 or len(document_number) > 20:
            raise ValueError("El documento debe tener entre 6 y 20 caracteres")

    @property
    def value(self) -> str:
        return self._document_number

    def __eq__(self, other):
        return isinstance(other, UserDocumentNumber) and self._document_number == other._document_number

    def __str__(self):
        return self._document_number