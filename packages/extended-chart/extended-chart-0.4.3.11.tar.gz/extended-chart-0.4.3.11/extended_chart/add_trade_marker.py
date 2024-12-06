import pandas as pd
import numpy as np
from typing import Literal

trade_colors = {'WIN': 'rgba(0,114,54,255)', 'LOSS': 'rgba(201,29,35,255)', 'SIGNAL': 'rgba(255,170,51,1)'}

direction_shape = {
    'LONG': {'entry': 'arrow_up', 'exit': 'arrow_down', 'entry_position': 'below', 'exit_position': 'above'},
    'SHORT': {'entry': 'arrow_down', 'exit': 'arrow_up', 'entry_position': 'above', 'exit_position': 'below'},
}

# TODO: if signal line for LMT and STP exceeds the chart datetime start and end, it freezes the chart

# TODO: Not important to start strategy development so park for now:
#   I would like to be able to customize label entries per trade
#   I would like to be able to show and hide based trades on labels and all labels


def add_trade_marker(chart, data: pd.DataFrame(), label='',
                     marking_style: Literal['show_trades', 'show_markers', None] = 'show_trades', show_signal_marker=False):
    if not marking_style:
        return [], []

    assert {'direction', 'entry_price', 'entry_time', 'exit_price', 'exit_time', 'pnl_with_commission'}. \
        issubset(set(data.columns)), 'Missing required pnl columns to render trade trade markers'

    data['trade_category'] = np.where(data.pnl_with_commission > 0, 'WIN', 'LOSS')

    pnl_lines = []
    pnl_arrows = []

    try:
        signal_data = data[(~data.signal_time.isnull()) & (~data.signal_timeout.isnull())][
            ['signal_time', 'signal_timeout', 'entry_price']]

        if show_signal_marker:
            for t in signal_data.itertuples():
                marker_line = chart.trend_line(t.signal_time, t.entry_price, t.signal_timeout, t.entry_price,
                                               color=trade_colors.get('SIGNAL'), width=1, style='solid', round=True)
                pnl_lines.append(marker_line)

                signal_circle = chart.marker(time=t.signal_time, position='below', shape='circle',
                                             color=trade_colors.get('SIGNAL'), text='')
                pnl_arrows.append(signal_circle)
    except AttributeError:  # TODO: Handle backward compatibility when signal_time data is not available, remove on cleanup
        ...

    try:
        markers_entry = data[['entry_time', 'direction', 'trade_category', 'pnl_with_commission']]
        markers_exit = data[['exit_time', 'direction', 'trade_category', 'pnl_with_commission']]

        markers_entry['datetime'] = markers_entry.entry_time
        markers_exit['datetime'] = markers_exit.exit_time
        markers_entry['shape'] = markers_entry.direction.apply(lambda x: direction_shape.get(x).get('entry'))
        markers_exit['shape'] = markers_exit.direction.apply(lambda x: direction_shape.get(x).get('exit'))
        markers_entry['position'] = markers_entry.direction.apply(lambda x: direction_shape.get(x).get('entry_position'))
        markers_exit['position'] = markers_exit.direction.apply(lambda x: direction_shape.get(x).get('exit_position'))
        markers_entry['color'] = markers_entry.trade_category.apply(lambda x: trade_colors.get(x))
        markers_exit['color'] = markers_exit.trade_category.apply(lambda x: trade_colors.get(x))
        markers_entry['text'] = label
        markers_exit['text'] = markers_exit.pnl_with_commission.apply(lambda x: f'{x:,.2f}')

        markers = pd.concat([markers_entry, markers_exit], ignore_index=True)
        markers = markers.sort_values('datetime', ascending=True)

        if marking_style == 'show_trades':
            for t in data.itertuples():
                marker_line = chart.trend_line(t.entry_time, t.entry_price, t.exit_time, t.exit_price,
                                               color=trade_colors.get(t.trade_category),
                                               width=2, style='dotted', round=True)
                pnl_lines.append(marker_line)

        if marking_style in ('show_trades', 'show_markers'):
            for m in markers.itertuples():
                marker_arrow = chart.marker(time=m.datetime, position=m.position, shape=m.shape, color=m.color, text=m.text)
                pnl_arrows.append(marker_arrow)

        return pnl_lines, pnl_arrows

    except:
        return pnl_lines, pnl_arrows
