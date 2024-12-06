import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QTableWidgetItem

import ok.gui
from ok.gui.tasks.TooltipTableWidget import TooltipTableWidget
from ok.gui.widget.Tab import Tab
from ok.gui.widget.UpdateConfigWidgetItem import value_to_string
from ok.logging.Logger import get_logger

logger = get_logger(__name__)


class TaskTab(Tab):
    def __init__(self):
        super().__init__()

        self.task_info_table = TooltipTableWidget()
        self.task_info_table.setFixedHeight(300)
        self.task_info_container = self.addCard(self.tr("Choose Window"), self.task_info_table)
        self.addWidget(self.task_info_container)

        self.task_info_labels = [self.tr('Info'), self.tr('Value')]
        self.task_info_table.setColumnCount(len(self.task_info_labels))  # Name and Value
        self.task_info_table.setHorizontalHeaderLabels(self.task_info_labels)
        self.update_info_table()

        # Create a QTimer object
        self.timer = QTimer()
        self.task_info_container.hide()

        # Connect the timer's timeout signal to the update function
        self.timer.timeout.connect(self.update_info_table)

        # Start the timer with a timeout of 1000 milliseconds (1 second)
        self.timer.start(1000)
        self.keep_info_when_done = False
        self.current_task = None
        self.current_task_name = ""

    def in_current_list(self, task):
        return True

    @staticmethod
    def time_elapsed(start_time):
        if start_time > 0:
            # Calculate the difference between the current time and the start time
            elapsed_time = time.time() - start_time

            # Calculate the number of hours, minutes, and seconds
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Return the elapsed time in the format "1h 12m 5s"
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        else:
            return ""

    def update_info_table(self):
        task = ok.gui.executor.current_task
        if task is not None and self.current_task is not task:
            self.current_task = task
        if task is None or not self.in_current_list(task):
            if self.task_info_table.isVisible():
                if not self.keep_info_when_done or self.task_info_table.rowCount() == 0:
                    self.task_info_container.hide()
                else:
                    self.task_info_container.titleLabel.setText(
                        self.tr(
                            'Completed') + self.current_task_name)
                    self.update_task_info(self.current_task)
        else:
            self.update_task_info(task)

    def update_task_info(self, task):
        if not self.task_info_table.isVisible():
            self.task_info_container.show()
        info = task.info
        self.current_task_name = f": {ok.gui.app.tr(task.name)} {self.time_elapsed(task.start_time)} {ok.gui.app.tr(task.description)}"
        self.task_info_container.titleLabel.setText(
            self.tr(
                'Running') + self.current_task_name)
        self.task_info_table.setRowCount(len(info))
        for row, (key, value) in enumerate(info.items()):
            if not self.task_info_table.item(row, 0):
                item0 = self.uneditable_item()
                self.task_info_table.setItem(row, 0, item0)
            self.task_info_table.item(row, 0).setText(ok.gui.app.tr(key))
            if not self.task_info_table.item(row, 1):
                item1 = self.uneditable_item()
                self.task_info_table.setItem(row, 1, item1)
            self.task_info_table.item(row, 1).setText(ok.gui.app.tr(value_to_string(value)))

    def uneditable_item(self):
        item = QTableWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item
