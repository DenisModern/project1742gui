import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# Создаем пользовательскую colormap с 50 цветами для плавного градиента
colors = [
    "#0c77be", "#0c78bb", "#0d79b9", "#0d7bb7", "#0e7cb5", "#0f7db3", "#0f7fb1", "#1080af",
    "#1081ad", "#1183ab", "#1284a9", "#1285a7", "#1387a5", "#1488a3", "#1489a1", "#158b9f",
    "#158c9d", "#168d9b", "#178f99", "#179097", "#189195", "#199393", "#199491", "#1a968f",
    "#1a978d", "#1b988b", "#1c9a89", "#1c9b87", "#1d9c85", "#1e9e83", "#1e9f81", "#1fa07f",
    "#1fa27d", "#20a37b", "#21a479", "#21a677", "#22a775", "#22a873", "#23aa71", "#24ab6f",
    "#24ac6d", "#25ae6b", "#26af69", "#26b067", "#27b265", "#27b363", "#28b561", "#29b65f",
    "#29b75d", "#2ab95b", "#2bba59", "#2bbb57", "#2cbd55", "#2cbe53", "#2dbf51", "#2ec14f",
    "#2ec24d", "#2fc34b", "#30c549", "#30c647", "#31c745", "#31c943", "#32ca41", "#33cb3f",
    "#33cd3d", "#34ce3b", "#35d039", "#37cc38", "#39c937", "#3cc636", "#3ec335", "#40c034",
    "#43bd33", "#45b932", "#47b632", "#4ab331", "#4cb030", "#4ead2f", "#51aa2e", "#53a72d",
    "#55a32c", "#58a02c", "#5a9d2b", "#5c9a2a", "#5f9729", "#619428", "#639027", "#668d26",
    "#688a26", "#6b8725", "#6d8424", "#6f8123", "#727e22", "#747a21", "#767720", "#79741f",
    "#7b711f", "#7d6e1e", "#806b1d", "#82681c", "#84641b", "#87611a", "#895e19", "#8b5b19",
    "#8e5818", "#905517", "#925116", "#954e15", "#974b14", "#994813", "#9c4513", "#9e4212",
    "#a13f11", "#a33b10", "#a5380f", "#a8350e", "#aa320d", "#ac2f0c", "#af2c0c", "#b1280b",
    "#b3250a", "#b62209", "#b81f08", "#ba1c07", "#bd1906", "#bf1606", "#c11205", "#c40f04",
    "#c60c03", "#c80902", "#cb0601", "#cd0300", "#d00000", "#ce0000", "#cd0000", "#cc0000",
    "#cb0000", "#ca0000", "#c80000", "#c70000", "#c60000", "#c50000", "#c40000", "#c20100",
    "#c10100", "#c00100", "#bf0100", "#be0100", "#bc0100", "#bb0100", "#ba0100", "#b90100",
    "#b80100", "#b60100", "#b50201", "#b40201", "#b30201", "#b20201", "#b00201", "#af0201",
    "#ae0201", "#ad0201", "#ac0201", "#aa0201", "#a90201", "#a80301", "#a70301", "#a60301",
    "#a40301", "#a30301", "#a20301", "#a10301", "#a00301", "#9e0301", "#9d0301", "#9c0301",
    "#9b0402", "#9a0402", "#980402", "#970402", "#960402", "#950402", "#940402", "#920402",
    "#910402", "#900402", "#8f0402", "#8e0502", "#8c0502", "#8b0502", "#8a0502", "#890502",
    "#880502", "#860502", "#850502", "#840502", "#830502", "#820502", "#810603"
]
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)


class Canvas(FigureCanvas):
    def __init__(self, parent=None, chart_height=8, chart_width=12, min_value=-32768, max_value=32767):
        self.chart_height = chart_height
        self.chart_width = chart_width
        self.min_value = min_value
        self.max_value = max_value
        fig, self.ax = plt.subplots(figsize=(4, 2), dpi=190)
        super().__init__(fig)
        self.setParent(parent)
        self.Z = np.zeros((self.chart_height, self.chart_width))
        self.cax = self.ax.pcolormesh(
            np.arange(self.chart_width + 1),
            np.arange(self.chart_height + 1),
            self.Z,
            shading='flat',
            cmap=cmap,
            vmin=self.min_value,
            vmax=self.max_value
        )
        self.ani = FuncAnimation(fig, self.animate, interval=100)
        self.cur_step = 0

        # Настройка фона и цвета текста
        self.ax.set_facecolor("#2E2E2E")  # Темный фон графика
        self.ax.figure.patch.set_facecolor('#2E2E2E')  # Темный фон фигуры
        self.ax.tick_params(colors="#E0E0E0")  # Цвет меток осей
        self.ax.spines['bottom'].set_color('#E0E0E0')
        self.ax.spines['top'].set_color('#E0E0E0')
        self.ax.spines['right'].set_color('#E0E0E0')
        self.ax.spines['left'].set_color('#E0E0E0')
        self.ax.title.set_color('#E0E0E0')  # Цвет заголовка графика
        self.ax.xaxis.label.set_color('#E0E0E0')  # Цвет подписи оси X
        self.ax.yaxis.label.set_color('#E0E0E0')  # Цвет подписи оси Y

    def set_min_value(self, min_value):
        self.min_value = min_value
        self.cax.set_clim(vmin=self.min_value, vmax=self.max_value)
        self.draw()

    def set_max_value(self, max_value):
        self.max_value = max_value
        self.cax.set_clim(vmin=self.min_value, vmax=self.max_value)
        self.draw()

    def update_plot(self, data):
        reshaped_data = np.array(data).reshape(
            (self.chart_height, self.chart_width))
        self.Z[self.cur_step %
               self.chart_height] = reshaped_data[self.cur_step % self.chart_height]
        self.cur_step += 1

    def animate(self, i):
        self.cax.set_array(self.Z.flatten())
        return self.cax,


class AnimatedCanvas(FigureCanvas):
    def __init__(self, parent=None, channel=0, maxlen=100):
        self.channel = channel
        self.maxlen = maxlen
        self.data = [0] * maxlen

        fig, self.ax = plt.subplots(figsize=(4, 2), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

        self.line, = self.ax.plot(self.data)
        self.ax.set_ylim(-32768, 32767)
        self.ax.set_xlim(0, maxlen)

        self.ani = FuncAnimation(fig, self.animate, interval=100)

    def update_channel(self, channel):
        self.channel = channel

    def animate(self, i):
        self.line.set_ydata(self.data)
        self.draw()
        return self.line,

    def update_plot(self, new_data):
        self.data = self.data[1:] + [new_data[self.channel]]


class AverageCanvas(FigureCanvas):
    def __init__(self, parent=None, channels=range(16), maxlen=100):
        self.channels = channels
        self.maxlen = maxlen
        self.data = np.zeros((maxlen, len(channels)))

        fig, self.ax = plt.subplots(figsize=(4, 2), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

        self.lines = []
        for i in range(len(channels)):
            line, = self.ax.plot(self.data[:, i])
            self.lines.append(line)
        self.ax.set_ylim(-32768, 32767)
        self.ax.set_xlim(0, maxlen)

        self.ani = FuncAnimation(fig, self.animate, interval=100)

    def animate(self, i):
        for i, line in enumerate(self.lines):
            line.set_ydata(self.data[:, i])
        self.draw()
        return self.lines

    def update_plot(self, new_data):
        avg_data = [np.mean(new_data[ch:ch + 16]) for ch in self.channels]
        self.data = np.roll(self.data, -1, axis=0)
        self.data[-1, :] = avg_data
