from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from propeller_design_tools.settings import VALID_OPER_PLOT_PARAMS
from propeller_design_tools.funcs import get_all_propeller_dirs
from propeller_design_tools.propeller import Propeller
try:
    from PyQt5 import QtWidgets, QtCore
    from propeller_design_tools.helper_ui_subclasses import PDT_Label, PDT_GroupBox, PDT_ComboBox, PDT_PushButton
    from propeller_design_tools.helper_ui_classes import SingleAxCanvas, PropellerCreationPanelCanvas, \
        CheckColumnWidget, AxesComboBoxWidget
except:
    pass


class PropellerSweepWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        super(PropellerSweepWidget, self).__init__()
        main_lay = QtWidgets.QHBoxLayout()
        self.setLayout(main_lay)

        center_lay = QtWidgets.QVBoxLayout()
        left_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(left_lay)
        main_lay.addLayout(center_lay)

        # left
        self.select_prop_widg = select_prop_widg = PropellerSweepSelectPropWidget(main_win=main_win)
        left_lay.addWidget(select_prop_widg)

        # center layout
        center_lay.addStretch()
        self.exist_data_widg = exist_data_widg = CheckColumnWidget(title='Existing Data (plot controls)', title_font_size=14,
                                                                   title_bold=True)
        center_lay.addWidget(exist_data_widg)
        center_lay.addStretch()
        add_data_grp = PDT_GroupBox('Add Data Points By Range')
        add_data_grp.setMinimumSize(400, 250)
        add_data_grp.setLayout(QtWidgets.QVBoxLayout())
        center_lay.addWidget(add_data_grp)
        center_lay.addStretch()

        # right layout
        self.metric_plot_widget = PropellerSweepMetricPlotWidget(main_win=main_win)
        main_lay.addWidget(self.metric_plot_widget)

        # connecting those signals
        self.exist_data_widg.checkboxClicked.connect(self.metric_plot_widget.update_data)

    @property
    def prop(self):
        return self.select_prop_widg.prop


class PropellerSweepSelectPropWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        super(PropellerSweepSelectPropWidget, self).__init__()
        self.main_win = main_win
        self.prop = None

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.select_prop_cb = select_prop_cb = PDT_ComboBox(width=200)
        self.pop_select_prop_cb()
        select_prop_cb.currentTextChanged.connect(self.select_prop_cb_changed)
        layout.addStretch()
        top_lay = QtWidgets.QHBoxLayout()
        top_lay.addStretch()
        top_lay.addWidget(PDT_Label('Select Propeller:', font_size=14, bold=True))
        top_lay.addWidget(select_prop_cb)
        top_lay.addStretch()
        layout.addLayout(top_lay)

        layout.addStretch()
        bot_lay = QtWidgets.QHBoxLayout()
        bot_lay.addStretch()
        self.wvel_3d_view = wvel_3d_view = gl.GLViewWidget()
        wvel_3d_view.setFixedSize(450, 450)
        bot_lay.addWidget(wvel_3d_view)
        bot_lay.addStretch()
        layout.addLayout(bot_lay)
        layout.addStretch()

    def pop_select_prop_cb(self):
        item_txts = ['None'] + get_all_propeller_dirs()
        self.select_prop_cb.addItems(item_txts)

    def select_prop_cb_changed(self):
        self.main_win.prop_sweep_widg.exist_data_widg.clear()
        if self.select_prop_cb.currentText() == 'None':
            self.prop = None
            self.wvel_3d_view.clear()
            self.metric_plot_widget.axes.clear()
            self.metric_plot_widget.plot_canvas.draw()
        else:
            self.prop = Propeller(self.select_prop_cb.currentText())
            self.plot_prop_wvel()
            self.main_win.prop_sweep_widg.metric_plot_widget.update_data()

            if len(self.prop.oper_data) == 0:
                return

            params = self.prop.oper_data.get_swept_params()
            if len(params) == 0:
                return

            self.main_win.prop_sweep_widg.exist_data_widg.col_groups = params
            for param in params:
                uniq_vals = self.prop.oper_data.get_unique_param(param=param)
                for val in uniq_vals:
                    self.main_win.prop_sweep_widg.exist_data_widg.add_checkbox(lbl='{}'.format(val), colname=param, chkd=True)

    def plot_prop_wvel(self):
        self.wvel_3d_view.clear()
        self.prop.plot_gl3d_wvel_data(view=self.wvel_3d_view)


class PropellerSweepMetricPlotWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        self.main_win = main_win
        super(PropellerSweepMetricPlotWidget, self).__init__()
        main_lay = QtWidgets.QVBoxLayout()
        self.setLayout(main_lay)
        self.creation_panel_canvas = None

        axes_cb_lay = QtWidgets.QHBoxLayout()
        main_lay.addLayout(axes_cb_lay)
        x_txts = ['x-axis'] + VALID_OPER_PLOT_PARAMS
        y_txts = ['y-axis'] + VALID_OPER_PLOT_PARAMS
        self.axes_cb_widg = AxesComboBoxWidget(x_txts=x_txts, y_txts=y_txts, init_xtxt='rpm',
                                               init_ytxt='Efficiency')
        self.xax_cb = self.axes_cb_widg.xax_cb
        self.yax_cb = self.axes_cb_widg.yax_cb
        self.xax_cb.setFixedWidth(130)
        self.yax_cb.setFixedWidth(130)
        self.xax_cb.currentTextChanged.connect(self.update_data)
        self.yax_cb.currentTextChanged.connect(self.update_data)

        axes_cb_lay.addStretch()
        axes_cb_lay.addWidget(PDT_Label('Plot Metric:', font_size=14, bold=True))
        axes_cb_lay.addWidget(self.axes_cb_widg)
        axes_cb_lay.addStretch()

        lay1 = QtWidgets.QHBoxLayout()
        lay1.addStretch()
        lay1.addWidget(PDT_Label('families of:', font_size=12))
        self.fam_cb = fam_cb = PDT_ComboBox(width=130)
        fam_cb.addItems(['None'] + VALID_OPER_PLOT_PARAMS)
        fam_cb.currentTextChanged.connect(self.update_data)
        lay1.addWidget(fam_cb)
        lay1.addWidget(PDT_Label('iso metric:', font_size=12))
        self.iso_cb = iso_cb = PDT_ComboBox(width=130)
        iso_cb.addItems(['None'] + VALID_OPER_PLOT_PARAMS)
        iso_cb.currentTextChanged.connect(self.update_data)
        lay1.addWidget(iso_cb)
        lay1.addStretch()
        main_lay.addLayout(lay1)

        self.plot_canvas = SingleAxCanvas(self, width=4.5, height=5)
        self.axes = self.plot_canvas.axes
        main_lay.addWidget(self.plot_canvas)
        toolbar = NavigationToolbar(self.plot_canvas, self)
        main_lay.addWidget(toolbar)
        main_lay.setAlignment(toolbar, QtCore.Qt.AlignHCenter)
        main_lay.addStretch()

    def update_data(self, *args):
        self.plot_canvas.clear_axes()

        yax_txt = self.yax_cb.currentText()
        xax_txt = self.xax_cb.currentText()
        if yax_txt == 'y-axis' or xax_txt == 'x-axis':
            return
        prop = self.main_win.prop_sweep_widg.prop
        if prop is None:
            return

        fam_txt = self.fam_cb.currentText()
        if fam_txt.lower() == 'none':
            fam_txt = None

        iso_txt = self.iso_cb.currentText()
        if iso_txt.lower() == 'none':
            iso_txt = None

        # need to filter out the unchecked boxes and not plot that data
        if len(args) > 0:
            print(isinstance(args[0], dict))
            print(args[0])

        prop.oper_data.plot(x_param=xax_txt, y_param=yax_txt, family_param=fam_txt, iso_param=iso_txt,
                            fig=self.plot_canvas.figure)

        self.plot_canvas.draw()
