import json
import logging
import pathlib as pl
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

POLLING_INTERVAL = 1  # second
PRINT_POLLING_INTERVAL = 10  # number of polls before print


class FileHandshaker:
    def __init__(
        self,
        self_uuid: str,
        input_dir_path: pl.Path,
        output_dir_path: pl.Path,
        is_initiator: bool = False,
        handshake_filename: str = "handshake.json",
        polling_interval=POLLING_INTERVAL,
        print_polling_interval=PRINT_POLLING_INTERVAL,
        verbose_level=logging.ERROR,
    ):
        self.verbose_level = verbose_level
        logger.setLevel(self.verbose_level)

        self.self_uuid = str(self_uuid)
        self.other_uuid = None

        self.last_write = None
        self.is_initiator = is_initiator

        self.input_dir_path = input_dir_path
        self.output_dir_path = output_dir_path
        self.handshake_filename = handshake_filename
        self.polling_interval = polling_interval
        self.print_polling_interval = print_polling_interval

        self.handshake_output_path = (
            self.output_dir_path / self.handshake_filename
        )
        self.handshake_input_path = (
            self.input_dir_path / self.handshake_filename
        )

    def shake(self):
        """Perform handshake with other service"""

        if self.handshake_output_path.exists():
            self.handshake_output_path.unlink()

        if self.is_initiator:
            return self.shake_initiator()
        else:
            return self.shake_receiver()

    def write_filecontent(self, path: pl.Path, content: str):
        path.write_text(content)

        self.last_write = path, content

    def retry_last_write(self):
        if self.last_write is not None:
            path, content = self.last_write
            self.write_filecontent(path, content)
            logger.info(f"Retried writing file content to {path}")

    def write_register_handshake(self):
        handshake_out = {
            "command": "register",
            "uuid": self.self_uuid,
        }
        if self.handshake_output_path.exists():
            self.handshake_output_path.unlink()
        self.write_filecontent(
            self.handshake_output_path, json.dumps(handshake_out)
        )
        logger.info(f"Wrote handshake file to {self.handshake_output_path}")

    def try_handshake(self):
        handshake_input_content = self.read_until_path_exists(
            self.handshake_input_path,
            wait_message="Waiting for handshake confirmation at "
            f"{self.handshake_input_path}...",
        )

        return json.loads(handshake_input_content)

    def wait_for_confirmation(self):
        waiter_confirm = 0
        while True:
            handshake_in = self.try_handshake()
            if (
                handshake_in["command"] == "confirm_registration"
                and handshake_in["confirmed_uuid"] == self.self_uuid
            ):
                break
            else:
                if waiter_confirm % self.print_polling_interval == 0:
                    logger.info(
                        "Waiting for correct handshake registration "
                        "confirmation ..."
                    )
                    self.retry_last_write()

                waiter_confirm += 1
            time.sleep(self.polling_interval)

        other_uuid = handshake_in["uuid"]

        return other_uuid

    def write_confirmation(self, other_uuid):
        if self.handshake_output_path.exists():
            self.handshake_output_path.unlink()

        handshake_out = {
            "command": "confirm_registration",
            "uuid": self.self_uuid,
            "confirmed_uuid": other_uuid,
        }
        self.write_filecontent(
            self.handshake_output_path, json.dumps(handshake_out)
        )

        assert other_uuid is not None

        logger.info(
            f"Wrote handshake confirmation for {other_uuid} to "
            f"{self.handshake_output_path}"
        )

    def shake_initiator(self):
        """Shake hand by initiator"""

        # Write a file to register with other side
        self.write_register_handshake()

        # Wait for a file confirming the registration
        tmp_other_uuid = self.wait_for_confirmation()

        # Write a file confirming our registration
        self.write_confirmation(tmp_other_uuid)

        # We are now sure about the other uuid
        self.other_uuid = tmp_other_uuid

        return self.other_uuid

    def shake_receiver(self):
        """Perform handshake by receiver"""

        other_uuid = None
        last_written_other_uuid = None
        task_waiter = 0
        while True:
            handshake_in = json.loads(
                self.read_until_path_exists(
                    self.handshake_input_path,
                    wait_message="Waiting for handshake file at "
                    f"{self.handshake_input_path} ...",
                )
            )

            command = handshake_in["command"]
            if command == "register":
                other_uuid = handshake_in["uuid"]
                if other_uuid != last_written_other_uuid:
                    logger.info(
                        "Received handshake registration from "
                        f"{other_uuid} for the first time ..."
                    )

                    self.write_confirmation(other_uuid)

                    last_written_other_uuid = other_uuid
            elif command == "confirm_registration":
                if (
                    other_uuid is not None
                    and handshake_in["uuid"] == other_uuid
                    and handshake_in["confirmed_uuid"] == self.self_uuid
                ):
                    logger.info(
                        "Received valid handshake confirmation from "
                        f"{other_uuid}, handshake finished."
                    )
                    break
            else:
                raise ValueError(f"Invalid handshake command: {command}")

            if task_waiter % self.print_polling_interval == 0:
                logger.info("Waiting for handshake command ...")
                self.retry_last_write()

            time.sleep(self.polling_interval)
            task_waiter += 1

        assert other_uuid is not None

        self.other_uuid = other_uuid

        return self.other_uuid

    def read_until_path_exists(self, path, wait_message="Waiting..."):
        waiter = 0
        while True:
            if path.exists():
                try:
                    file_content = path.read_text()
                except FileNotFoundError:
                    pass
                else:
                    return file_content

            if waiter % self.print_polling_interval == 0:
                logger.debug(wait_message)
                self.retry_last_write()
            time.sleep(self.polling_interval)
            waiter += 1
