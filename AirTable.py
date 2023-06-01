from pyairtable import Table

from config import API_KEY, BASE_ID, TABLE_NAME


class AirTable():
    table = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE_NAME)

    def get_usernames(self):
        data = self.table.all()
        data = [{"id": dict_["id"], "username": dict_["fields"]["Account"]} for dict_ in data]
        return data

    def add_number(self, record_id: str, column_name: str, number: int):
        try:
            self.table.update(record_id=record_id, fields={column_name: number})
            print(f"the upload was successful")
        except Exception as ex:
            print(f"the upload was NOT successful: {ex}")