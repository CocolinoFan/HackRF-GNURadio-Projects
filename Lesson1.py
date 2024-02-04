#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM reaciver
# Author: CocolinoFan
# Description: Change "chanel_freq" to the FM station frequency you want to listen to
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip



class Lesson1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM reaciver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM reaciver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Lesson1")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.chanel_width = chanel_width = 200e3
        self.chanel_freq_2 = chanel_freq_2 = 100.1e6
        self.chanel_freq_1 = chanel_freq_1 = 100.1e6
        self.center_freq = center_freq = 97.9e6
        self.audio_gain_2 = audio_gain_2 = 0.01
        self.audio_gain_1 = audio_gain_1 = 0.01

        ##################################################
        # Blocks
        ##################################################

        self._chanel_freq_2_range = qtgui.Range(87.6e6, 107.9e6, 100, 100.1e6, 200)
        self._chanel_freq_2_win = qtgui.RangeWidget(self._chanel_freq_2_range, self.set_chanel_freq_2, "'chanel_freq_2'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._chanel_freq_2_win)
        self._chanel_freq_1_range = qtgui.Range(87.6e6, 107.9e6, 100, 100.1e6, 200)
        self._chanel_freq_1_win = qtgui.RangeWidget(self._chanel_freq_1_range, self.set_chanel_freq_1, "'chanel_freq_1'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._chanel_freq_1_win)
        self._audio_gain_2_range = qtgui.Range(0, 2, 0.01, 0.01, 200)
        self._audio_gain_2_win = qtgui.RangeWidget(self._audio_gain_2_range, self.set_audio_gain_2, "audio_gain_channel_2", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._audio_gain_2_win)
        self._audio_gain_1_range = qtgui.Range(0, 2, 0.01, 0.01, 200)
        self._audio_gain_1_win = qtgui.RangeWidget(self._audio_gain_1_range, self.set_audio_gain_1, "audio_gain_channel_1", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._audio_gain_1_win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Raw", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            (int(samp_rate/chanel_width)),
            firdes.low_pass(
                1,
                samp_rate,
                75e3,
                25e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            (int(samp_rate/chanel_width)),
            firdes.low_pass(
                1,
                samp_rate,
                75e3,
                25e3,
                window.WIN_HAMMING,
                6.76))
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(audio_gain_2)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(audio_gain_1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0_0 = analog.wfm_rcv(
        	quad_rate=480e3,
        	audio_decimation=10,
        )
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=480e3,
        	audio_decimation=10,
        )
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (center_freq - chanel_freq_2), 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (center_freq - chanel_freq_1), 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_wfm_rcv_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_wfm_rcv_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Lesson1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 75e3, 25e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 75e3, 25e3, window.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_chanel_width(self):
        return self.chanel_width

    def set_chanel_width(self, chanel_width):
        self.chanel_width = chanel_width

    def get_chanel_freq_2(self):
        return self.chanel_freq_2

    def set_chanel_freq_2(self, chanel_freq_2):
        self.chanel_freq_2 = chanel_freq_2
        self.analog_sig_source_x_0_0.set_frequency((self.center_freq - self.chanel_freq_2))

    def get_chanel_freq_1(self):
        return self.chanel_freq_1

    def set_chanel_freq_1(self, chanel_freq_1):
        self.chanel_freq_1 = chanel_freq_1
        self.analog_sig_source_x_0.set_frequency((self.center_freq - self.chanel_freq_1))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.analog_sig_source_x_0.set_frequency((self.center_freq - self.chanel_freq_1))
        self.analog_sig_source_x_0_0.set_frequency((self.center_freq - self.chanel_freq_2))
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_audio_gain_2(self):
        return self.audio_gain_2

    def set_audio_gain_2(self, audio_gain_2):
        self.audio_gain_2 = audio_gain_2
        self.blocks_multiply_const_vxx_0_0.set_k(self.audio_gain_2)

    def get_audio_gain_1(self):
        return self.audio_gain_1

    def set_audio_gain_1(self, audio_gain_1):
        self.audio_gain_1 = audio_gain_1
        self.blocks_multiply_const_vxx_0.set_k(self.audio_gain_1)




def main(top_block_cls=Lesson1, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
