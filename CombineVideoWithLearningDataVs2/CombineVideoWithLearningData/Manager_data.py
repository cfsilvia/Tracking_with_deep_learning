# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:01:28 2024

@author: Administrator
"""
from auxiliary_functions import auxiliary_functions
import cv2
from Frame_treatment import CreatePlot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from dataclasses import dataclass


@dataclass
class Config:
    middle_tube_y: int
    middle_tube_x: int
    input_excel: str
    input_video: str
    sheet_name: str
    column_name: str
    output_video: str
    upper_tube: int
    lower_tube: int
    fps: float
    if_cropped: bool
    if_plot_left: bool
    input_excel_left: str = ""
    title: str = ""
    xstart: int = 0
    ystart: int = 0
    xend: int = 0
    yend: int = 0


class ManagerData:

    def __init__(self, config: Config):
        self.config = config

    def process(self):
        if not self.config.if_plot_left:
            # Get data to plot for right side
            data_to_plot = auxiliary_functions.read_excel(
                self.config.middle_tube_y, self.config.middle_tube_x,
                self.config.input_excel, self.config.sheet_name,
                self.config.column_name, self.config.upper_tube,
                self.config.lower_tube
            )
            # Save data
            data_to_save = pd.DataFrame({'Right_side': data_to_plot})
            self._save_data(data_to_save)
            # Create new movie
            up_line = self.config.middle_tube_y - self.config.upper_tube
            down_line = self.config.middle_tube_y - self.config.lower_tube
            self._create_new_movie(data_to_plot, up_line, down_line)
        else:
            # Get data for both sides
            data_to_plot_right = auxiliary_functions.read_excel(
                self.config.middle_tube_y, self.config.middle_tube_x,
                self.config.input_excel, self.config.sheet_name,
                self.config.column_name, self.config.upper_tube,
                self.config.lower_tube
            )
            data_to_plot_left = auxiliary_functions.read_excel(
                self.config.middle_tube_y, self.config.middle_tube_x,
                self.config.input_excel_left, self.config.sheet_name,
                self.config.column_name, self.config.upper_tube,
                self.config.lower_tube
            )
            # Save data
            data_to_save = pd.DataFrame({
                'Left_side': data_to_plot_left,
                'Right_side': data_to_plot_right
            })
            self._save_data(data_to_save)
            # Create new movie
            up_line = self.config.middle_tube_y - self.config.upper_tube
            down_line = self.config.middle_tube_y - self.config.lower_tube
            self._create_new_movie(
                data_to_plot_right, up_line, down_line,
                data_to_plot_left
            )

    def _save_data(self, data_to_save):
        directory = os.path.dirname(self.config.input_excel)
        file_name_without_extension = os.path.splitext(
            os.path.basename(self.config.input_excel)
        )[0]
        output_path = os.path.join(
            directory,
            f"{file_name_without_extension}_ToPlot.xlsx"
        )
        with pd.ExcelWriter(output_path) as writer:
            data_to_save.to_excel(
                writer, sheet_name=self.config.column_name, index=False
            )

    def _create_new_movie(self, data_to_plot, up_line, down_line,
                          data_to_plot_left=None):
        plt.ioff()
        counter_frame = 0
        cap = cv2.VideoCapture(self.config.input_video)

        if not cap.isOpened():
            raise ValueError("Error: Could not open video.")

        fps = cap.get(cv2.CAP_PROP_FPS)
        writer = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Reached end of video or failed to read frame.")
                break

            # Crop the image if needed
            if self.config.if_cropped:
                frame = frame[
                    self.config.ystart:self.config.yend,
                    self.config.xstart:self.config.xend
                ]

            # Create plot
            plot_instance = CreatePlot(
                frame, data_to_plot, counter_frame, up_line, down_line,
                data_to_plot_left, self.config.title
            )
            plot_instance.SelectDataToPlot()
            img, fig = plot_instance.FillSubplot()

            # Initialize writer on first frame
            if counter_frame == 0:
                height, width = img.shape[:2]
                writer = cv2.VideoWriter(
                    self.config.output_video,
                    cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                    fps, (width, height)
                )

            writer.write(img)
            plt.close(fig)
            print(counter_frame)
            counter_frame += 1

            # Optional: break on 'q' key (though headless)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()