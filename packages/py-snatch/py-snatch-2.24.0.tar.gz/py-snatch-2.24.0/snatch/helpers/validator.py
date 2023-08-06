from loguru import logger


class Validator:
    def __init__(self, data):
        self.instance = data["class"]
        self.data = data["data"]
        if "dataset" in data:
            self.dataset = data["dataset"] if data["dataset"] else []

    def receita_federal_validator(self):
        logger.info("Running Receita Federal validator")
        if "emails_extended" in self.dataset:
            if not self.data["mail"]:
                return False
        if "phones_extended" in self.dataset:
            if not self.data["phone"]:
                return False
        if "addresses_extended" in self.dataset:
            if not self.data["address"]:
                return False
        if "activity_indicators" in self.dataset:
            if not self.data["employees_range"]:
                return False
        return True

    def start(self):
        if self.instance == "receita_federal_pj":
            self.dataset = (
                self.enum_to_str(self.dataset)
                if isinstance(self.dataset, list)
                else self.dataset
            )
            return self.receita_federal_validator()
        else:
            return True

    def enum_to_str(self, arr):
        return [i.value for i in arr]
