import json

from bson.objectid import ObjectId

from clean.clean_service.src.encoder.mongo_serializer import JSONEncoder
from clean.clean_service.src.controller.base import BaseHandler


class CleaningProcessHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    async def get(self, cleaning_process_id):
        db = self.settings['db']
        cleaning_process = None

        if cleaning_process_id:
            try:
                cleaning_process_id = ObjectId(cleaning_process_id)
                cleaning_process = await db.cleaningProcess.find_one(
                    {"_id": cleaning_process_id}
                )
            except TypeError:
                cleaning_process = None

        if cleaning_process:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(JSONEncoder().encode(cleaning_process))
            return

        self.send_error(status_code=404)

    async def post(self, *args, **kwargs):
        inc_body = self.request.body.decode('utf-8')

        db = self.settings['db']
        cleaning_process = json.loads(inc_body)

        msg_failed = {
            "created": False,
            "msg": "Could not create questionary."
        }
        msg_success = {
            "created": True,
            "msg": "Successfully created questionary."
        }
        self.set_header("Access-Control-Allow-Origin", "*")
        try:
            created_cleaning_process = await db.cleaningProcess.insert_one(
                cleaning_process
            )
            if created_cleaning_process:
                self.write(msg_success)
            else:
                self.write(msg_failed)
        except Exception:
            self.write(msg_failed)


