import sys

from rich.prompt import Prompt, Confirm
from rich import print

from audit_tools.core.errors import SessionException
from audit_tools.core.functions import clear
from audit_tools.core.session import Session


class Scanner:
    def __init__(self, session: Session):
        self.session = session

    # Create run event
    def start_count(self):
        clear()

        scanning = True
        while scanning:
            self.session.logger.info("Scanner: Scanning...")

            sku = Prompt.ask("> Enter [bold green]SKU")

            if sku == "" or sku == " " or not sku:
                self.session.logger.info("Scanner: Stopped")
                break

            try:
                _ = self.session.get_product(sku)
            except SessionException as e:
                print(f"> [bold red]{e}")
                continue

            else:
                while True:
                    try:
                        count = int(Prompt.ask("\t> Enter product count [yellow]check all boxes"))

                        if count >= 0:

                            # Extra check incase user somehow enters a sku that passed a false positive
                            try:
                                self.session.count_product(sku, count)
                            except SessionException as e:
                                self.session.logger.error(e)
                                print(f"\t> [bold red]{e}")
                            break

                    except ValueError:
                        self.session.logger.error("Scanner: Invalid count")
                        continue

    def shutdown(self):
        self.session.logger.info("Scanner is shutting down...")

        self.session.parse_session_data()

        while self.session.missed_counter > 0:
            self.session.logger.warning(f"[bold orange] {self.session.missed_counter} missed products...")
            print(f"> [bold orange]You may have missed items!")
            print(self.session.get_table_data(self.session.missed_items))
            answer = Confirm.ask("> [bold orange]Would you like to count them?", default=True)
            if answer:
                self.start_count()
            else:
                break

        if self.session.variance_counter > 0:
            print(self.session.get_table_data(self.session.variance_items))

            _ = Prompt.ask("Press enter to exit...")

