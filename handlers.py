from PyQt5 import QtCore, QtSerialPort
import numpy as np

num_channels = 96
chart_height = 6
chart_width = num_channels // chart_height

data_buffer = b''
recent_data = []


def handle_ready_read(self):
    global data_buffer, recent_data, shared_data_buffer
    while self.serialInst.in_waiting > 0:
        data_buffer += self.serialInst.read(self.serialInst.in_waiting)

        start_marker = b'<START>'
        end_marker = b'<END>'

        while start_marker in data_buffer and end_marker in data_buffer:
            start_index = data_buffer.find(start_marker)
            end_index = data_buffer.find(end_marker) + len(end_marker)

            complete_message = data_buffer[start_index:end_index]
            data_buffer = data_buffer[end_index:]

            main_data = complete_message[len(start_marker):-len(end_marker)]
            data_bytes = main_data
            complete_data = []

            for i in range(0, len(data_bytes), 2):
                if i + 1 < len(data_bytes):
                    value = int.from_bytes(
                        data_bytes[i:i+2], byteorder='little', signed=True)
                    complete_data.append(value)

            if len(complete_data) == num_channels:
                complete_data[34] = 2000
                complete_data[49] = 2000
                complete_data[13] = 2000
                complete_data[40] = 2000
                self.record_data(complete_data)
                recent_data.append(complete_data)
                if len(recent_data) > 5:
                    recent_data.pop(0)

                avg_data = np.mean(recent_data, axis=0).astype(int).tolist()
                self.update_plot(avg_data)
                for avg_canvas in self.avg_canvases:
                    avg_canvas.update_plot(complete_data)
                self.graph1_canvas.update_plot(complete_data)
                self.graph2_canvas.update_plot(complete_data)

                # Вывод данных в com_textedit
                self.com_textedit.appendPlainText(str(complete_data))
            else:
                print(f"Incorrect data length: {len(complete_data)}")


def handle_error(self, error):
    if error == QtSerialPort.QSerialPort.NoError:
        return
    print(error, self.serialInst.errorString())


def convert_input_data(self, data):
    display_input_data(self, data, self.cur_step)
    return data


def display_input_data(self, data, cur_step):
    l = len(data) if len(data) <= num_channels else num_channels
    for i in range(l):
        try:
            self.Z[cur_step % chart_height][i] = data[i]
        except ValueError:
            continue
    self.draw()
    self.flush_events()
    self.cur_step += 1


def process_data(data):
    return data
