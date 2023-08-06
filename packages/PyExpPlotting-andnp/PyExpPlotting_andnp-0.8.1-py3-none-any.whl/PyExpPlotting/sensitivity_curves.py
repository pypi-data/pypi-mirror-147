import numpy as np
from itertools import tee
from typing import Any, Dict, Optional
from PyExpUtils.results.backends.backend import ResultList
from PyExpUtils.results.results import getBest, splitOverParameter, sliceOverParameter
from PyExpPlotting.tools import getCurveReducer

def confidenceInterval(mean, stderr, mult):
    return (mean - mult * stderr, mean + mult * stderr)

def buildOptions(options: Optional[Dict[str, Any]]):
    options = options if options is not None else {}
    out_options = {}

    if options.get('dashed'):
        out_options['style'] = '--'
    elif options.get('dotted'):
        out_options['style'] = ':'
    else:
        out_options['style'] = None

    out_options['alpha_main'] = options.get('alpha_main', 1.0)
    out_options['alpha'] = options.get('alpha', 0.4) * out_options['alpha_main']
    out_options['color'] = options.get('color')
    out_options['label'] = options.get('label')
    out_options['width'] = options.get('width', 1.25)
    out_options['legend'] = options.get('legend', True)
    out_options['stderr'] = options.get('stderr', 2.0)
    out_options['prefer'] = options.get('prefer', 'big')
    out_options['log_x'] = options.get('log_x', None)
    out_options['x_label'] = options.get('x_label')
    out_options['y_label'] = options.get('y_label')
    out_options['curve_reducer'] = options.get('curve_reducer', 'auc')
    out_options['param_reducer'] = options.get('param_reducer', 'best')

    return out_options

def getSensitivityData(results: ResultList, param: str, options: Optional[Dict[str, Any]] = None):
    o = buildOptions(options)

    if o['param_reducer'] == 'best':
        split = splitOverParameter(results, param)
        bestStream = {}
        for k in split:
            bestStream[k] = getBest(split[k], prefer=o['prefer'])

    elif o['param_reducer'] == 'slice':
        l, r = tee(results)
        best = getBest(l, prefer=o['prefer'])

        bestStream = sliceOverParameter(r, best, param)

    else:
        raise NotImplementedError()

    x = sorted(list(bestStream))
    best = bestStream

    metric = getCurveReducer(o['curve_reducer'])

    y = np.array([metric(best[k].mean()) for k in x])
    e = np.array([metric(best[k].stderr()) for k in x])

    e[np.isnan(y)] = 0.000001
    y[np.isnan(y)] = 100000

    return x, y, e

def plot(results: ResultList, ax, param: str, options: Optional[Dict[str, Any]] = None):
    o = buildOptions(options)
    x, y, e = getSensitivityData(results, param, o)

    pl = ax.plot(x, y, label=o['label'], linestyle=o['style'], color=o['color'], linewidth=o['width'])
    if o['stderr']:
        color = pl[0].get_color()
        low_ci, high_ci = confidenceInterval(np.array(y), np.array(e), o['stderr'])
        ax.fill_between(x, low_ci, high_ci, color=color, alpha=o['alpha'])

    if o['log_x'] is not None:
        ax.set_xscale('log', base=o['log_x'])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if o['legend']:
        ax.legend(frameon=False)

    if o['x_label'] is None:
        x_label = param.split('.')[-1]
        if o['log_x'] is not None:
            scale = o['log_x']
            x_label += f' (log-{scale} scale)'

        ax.set_xlabel(x_label)
    elif o['x_label']:
        ax.set_xlabel(o['x_label'])
