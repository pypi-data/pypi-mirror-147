"""
Analyze features.

Usage:
 ./classes/features.py

Author:
 Peter Rigali - 2022-03-19
"""
from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd
import statsmodels.api as sm
from pyjr.classes.model_data import ModelingData
from pyjr.classes.data import Data
from pyjr.utils.tools.math import _mean, _perc, _var, _sum, _std, _min
from pyjr.utils.tools.clean import _round, _mtype
from pyjr.utils.tools.general import _add_constant, _cent, _dis
from pyjr.utils.tools.array import _stack
import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqline
import matplotlib.pyplot as plt
from pyjr.plot.histogram import Histogram
from pyjr.plot.line import Line
from pyjr.plot.scatter import Scatter


@dataclass
class FeaturePerformance:

    __slots__ = ["modeling_data", "reg_results", "outlier_results"]

    def __init__(self, data: ModelingData):
        self.modeling_data = data
        self.reg_results = None
        self.outlier_results = None

    def __repr__(self):
        return "FeaturePerformance"

    def add_regression(self):
        """Return r2, pred to true correlation, and mean of residuals"""
        results = {}
        dic = dict(zip(range(len(self.modeling_data.x_data_names)), self.modeling_data.x_data_names))
        for i in range(len(self.modeling_data.x_data_names)):
            key = dic[i]
            results[key] = {}
            x = _add_constant(data=self.modeling_data.x_train[:, i])
            y = self.modeling_data.y_train
            lin_reg = sm.OLS(y, x).fit()
            pred = lin_reg.predict(_add_constant(data=self.modeling_data.x_test[:, i]))
            flat_ytest = self.modeling_data.y_test.reshape(1, pred.shape[0]).tolist()[0]
            results[key]["r2"] = _round(d=lin_reg.rsquared, v=100, r=True)
            results[key]['pred_true_coef'] = _round(d=np.corrcoef(pred, flat_ytest)[0, 1], v=100, r=True)
            results[key]['residuals_mean'] = _round(d=lin_reg.resid.mean(), v=100, r=True)
        self.reg_results = results
        return self

    def add_outlier_std(self, plus: bool = True, std_value: int = 2, return_ind: bool = True):
        per_dic = {-3: 0.001, -2: 0.023, -1: 0.159, 0: 0.50, 1: 0.841, 2: 0.977, 3: 0.999}
        dic = {val: self.modeling_data.x_data[:, ind] for ind, val in enumerate(self.modeling_data.x_data_names)}
        for key, val in dic.items():
            new_data = val.tolist()
            if _min(new_data) >= 0:
                if plus:
                    ind = np.where(val <= _perc(d=new_data, q=per_dic[std_value]))[0]
                else:
                    ind = np.where(val >= _perc(d=new_data, q=per_dic[-std_value]))[0]
            else:
                if plus:
                    ind = np.where(val <= _mean(d=new_data) + _std(d=new_data) * std_value)[0]
                else:
                    ind = np.where(val >= _mean(d=new_data) - _std(d=new_data) * std_value)[0]
            if return_ind:
                dic[key] = tuple(ind.tolist())
            else:
                dic[key] = tuple(val[ind].tolist())
        self.outlier_results = dic
        return self

    def add_outlier_var(self, plus: Optional[bool] = True, std_value: int = 2, return_ind: bool = True):
        per_dic = {-3: 0.001, -2: 0.023, -1: 0.159, 0: 0.50, 1: 0.841, 2: 0.977, 3: 0.999}
        dic = {val: self.modeling_data.x_data[:, ind] for ind, val in enumerate(self.modeling_data.x_data_names)}
        for key, val in dic.items():
            lst = val.tolist()
            temp_var = _var(d=lst)
            dev_based = np.array([temp_var - _var(np.delete(lst, i)) for i, j in enumerate(lst)])
            if plus:
                q = _perc(d=lst, q=per_dic[std_value])
                ind = np.where(dev_based <= q)[0]
            else:
                q = _perc(d=lst, q=per_dic[-std_value])
                ind = np.where(dev_based >= q)[0]

            if return_ind:
                dic[key] = tuple(ind.tolist())
            else:
                dic[key] = tuple(val[ind].tolist())
        self.outlier_results = dic
        return self

    def add_outlier_regression(self, plus: Optional[bool] = True, std_value: Optional[int] = 2, return_ind: bool = True):
        per_dic = {-3: 0.001, -2: 0.023, -1: 0.159, 0: 0.50, 1: 0.841, 2: 0.977, 3: 0.999}
        dic = {val: self.modeling_data.x_data[:, ind] for ind, val in enumerate(self.modeling_data.x_data_names)}
        for key, val in dic.items():
            arr = _stack(val, self.modeling_data.y_data, False)
            ran = np.array(range(self.modeling_data.len))
            mu_y = np.zeros(len(arr) - 1)
            line_ys = []
            for i, j in enumerate(arr):
                xx, yy = np.delete(arr[:, 0], i), np.delete(arr[:, 1], i)
                w1 = (np.cov(xx, yy, ddof=1) / _var(xx, dof=1))[0, 1]
                new_y = w1 * ran[:-1] + (-1 * _mean(xx) * w1 + _mean(yy))
                mu_y = (mu_y + new_y) / 2
                line_ys.append(new_y)

            reg_based = np.array([np.mean(np.square(mu_y - j)) for i, j in enumerate(line_ys)])
            if plus:
                threshold = _perc(d=reg_based, q=per_dic[std_value])
                ind = np.where(reg_based <= threshold)[0]
            else:
                threshold = _perc(d=reg_based, q=per_dic[-std_value])
                ind = np.where(reg_based >= threshold)[0]

            if return_ind:
                dic[key] = tuple(ind.tolist())
            else:
                dic[key] = tuple(val[ind].tolist())
        self.outlier_results = dic
        return self

    def add_outlier_distance(self, plus: Optional[bool] = True, std_value: int = 2, return_ind: bool = True):
        per_dic = {-3: 0.001, -2: 0.023, -1: 0.159, 0: 0.50, 1: 0.841, 2: 0.977, 3: 0.999}
        dic = {val: self.modeling_data.x_data[:, ind] for ind, val in enumerate(self.modeling_data.x_data_names)}
        for key, val in dic.items():
            arr = _stack(val, self.modeling_data.y_data, False)
            cent_other = _cent(arr[:, 0], arr[:, 1])
            ran = range(0, self.modeling_data.len)
            x_y_other_centers = np.array([_dis(_cent(x_lst=[arr[i][0]], y_lst=[arr[i][1]]), cent_other) for i in ran])

            if plus:
                x_y_other_centers_std = _perc(d=x_y_other_centers, q=per_dic[std_value])
                ind = np.where(x_y_other_centers <= x_y_other_centers_std)[0]
            else:
                x_y_other_centers_std = _perc(d=x_y_other_centers, q=per_dic[-std_value])
                ind = np.where(x_y_other_centers >= x_y_other_centers_std)[0]

            if return_ind:
                dic[key] = tuple(ind.tolist())
            else:
                dic[key] = tuple(val[ind].tolist())
        self.outlier_results = dic
        return self

    def add_outlier_hist(self, plus: Optional[bool] = True, std_value: int = 2, return_ind: bool = True):
        per_dic = {-3: 0.001, -2: 0.023, -1: 0.159, 0: 0.50, 1: 0.841, 2: 0.977, 3: 0.999}
        dic = {val: self.modeling_data.x_data[:, ind] for ind, val in enumerate(self.modeling_data.x_data_names)}
        for key, val in dic.items():
            n, b = np.histogram(val, bins='sturges')
            if plus:
                qn = _perc(d=val, q=per_dic[std_value])
                ind = np.where(n <= qn)[0]
                bin_edges = np.array([(b[i], b[i + 1]) for i in range(len(b) - 1)])[ind]
            else:
                qn = _perc(d=val, q=per_dic[-std_value])
                ind = np.where(n >= qn)[0]
                bin_edges = np.array([(b[i], b[i + 1]) for i in range(len(b) - 1)])[ind]

            z_selected_ind = []
            for i, j in enumerate(val):
                for k, l in bin_edges:
                    if k >= j <= l:
                        z_selected_ind.append(i)
                        break

            # select = np.in1d(arr, arr[z_selected_ind])
            # return np.array([np.where(arr == i)[0][0] for i in arr[np.in1d(arr, arr[~select])]])
            if return_ind:
                dic[key] = tuple(z_selected_ind)
            else:
                dic[key] = tuple(val[z_selected_ind].tolist())
        self.outlier_results = dic
        return self

    def add_outlier_knn(self, plus: Optional[bool] = True, std_value: int = 2, return_ind: bool = True):
        per_dic = {-3: 0.001, -2: 0.023, -1: 0.159, 0: 0.50, 1: 0.841, 2: 0.977, 3: 0.999}
        dic = {val: self.modeling_data.x_data[:, ind] for ind, val in enumerate(self.modeling_data.x_data_names)}
        for key, val in dic.items():
            arr = _stack(val, self.modeling_data.y_data, False)
            ran = range(0, self.modeling_data.len)
            test_centers = (_cent([arr[ind, 0]], [arr[ind, 1]]) for ind in ran)
            distances = [_dis(c1=i, c2=j) for i in test_centers for j in test_centers]
            if plus:
                threshold = _perc(d=distances, q=per_dic[std_value])
                count_dic = {}
                for i, j in enumerate(arr):
                    temp = arr[i, :] <= threshold
                    count_dic[i] = _sum([1 for i in temp if i == True])
            else:
                threshold = _perc(d=distances, q=per_dic[-std_value])
                count_dic = {}
                for i, j in enumerate(arr):
                    temp = arr[i, :] >= threshold
                    count_dic[i] = _sum([1 for i in temp if i == True])

            lst = []
            for i in _mtype(d=count_dic.values()):
                if isinstance(i, list):
                    for val1 in i:
                        lst.append(val1)
                else:
                    lst.append(i)
            if plus:
                val1 = _perc(d=lst, q=per_dic[std_value])
                ind = np.where(np.array(lst) <= np.floor(val1))[0]
            else:
                val1 = _perc(d=lst, q=per_dic[-std_value])
                ind = np.where(np.array(lst) >= np.floor(val1))[0]
            if return_ind:
                dic[key] = tuple(ind.tolist())
            else:
                dic[key] = tuple(val[ind].tolist())
        self.outlier_results = dic
        return self

    def add_outlier_cooks_distance(self, plus: bool = True, std_value: int = 2, return_ind: bool = True):
        per_dic = {-3: 0.001, -2: 0.023, -1: 0.159, 0: 0.50, 1: 0.841, 2: 0.977, 3: 0.999}
        dic = {val: self.modeling_data.x_data[:, ind] for ind, val in enumerate(self.modeling_data.x_data_names)}
        for key, val in dic.items():
            x = sm.add_constant(data=val)
            y = self.modeling_data.y_data
            model = sm.OLS(y, x).fit()
            np.set_printoptions(suppress=True)
            influence = model.get_influence()
            cooks = influence.cooks_distance
            if plus:
                val1 = _perc(d=cooks[0], q=per_dic[std_value])
                ind = np.where(cooks[0] <= val1)[0]
            else:
                val1 = _perc(d=cooks[0], q=per_dic[-std_value])
                ind = np.where(cooks[0] >= val1)[0]
            if return_ind:
                dic[key] = tuple(ind.tolist())
            else:
                dic[key] = tuple(val[ind].tolist())
        self.outlier_results = dic
        return self

    def get_outliers(self):
        ran = range(self.modeling_data.len)
        key_dic = dict(zip(self.modeling_data.x_data_names, range(len(self.modeling_data.x_data_names))))
        dic = self.outlier_results
        for key, val in dic.items():
            results = {i: True for i in val}
            temp = [i for i in ran if i not in results]
            dic[key] = tuple(self.modeling_data.x_data[:, key_dic[key]][temp].tolist())
        return dic

    def get_feature_plot(self):
        """Returns a series of plots describing the features."""
        data_lst = []
        for ind, val in enumerate(self.modeling_data.x_data_names):
            data_lst.append(Data(data=self.modeling_data.x_data[:, ind], name=val))

        # data_lst = [t, tt, tttt]
        h = 4 * data_lst.__len__()
        fig, axes = plt.subplots(nrows=data_lst.__len__(), ncols=4, figsize=(16, h))
        fig.suptitle('Feature Characteristics', fontsize='xx-large')
        count = 0
        for data in data_lst:
            Histogram(data=data, ax=axes[count, 0], title_size='large', ylabel=data.name, ylabel_size='x-large',
                      include_norm=data.name, norm_color="tab:blue", norm_lineweight=2)
            pp = sm.ProbPlot(data.array())
            qq = pp.qqplot(marker='.', markerfacecolor='tab:orange', markeredgecolor='tab:orange', alpha=0.3,
                           ax=axes[count, 1], markersize=15)
            qqline(ax=axes[count, 1], line='r', x=pp.theoretical_quantiles, y=pp.sample_quantiles, color='tab:blue',
                   linestyle='--', linewidth=2, alpha=1)
            axes[count, 1].set_title('Q-Q Plot', fontsize='large')
            axes[count, 1].set_xlabel('')
            axes[count, 1].set_ylabel('')
            axes[count, 1].grid(alpha=0.75, linestyle=(0, (3, 3)), linewidth=0.5)
            Line(data=data, ax=axes[count, 2], title_size='large', include_quant=data.name, quant_color='tab:blue',
                 quant_lineweight=[0.75, 1.0, 1.5, 2.0, 1.5, 1.0, 0.75])
            Scatter(data=data, ax=axes[count, 3], title_size='large', regression_line=data.name,
                    regression_line_color='tab:blue', regression_line_lineweight=2)
            count += 1
        ratio = 1.0
        cols = [0, 1, 2, 3]
        wid = list(range(data_lst.__len__()))
        for w in wid:
            for c in cols:
                x_left, x_right = axes[w, c].get_xlim()
                y_low, y_high = axes[w, c].get_ylim()
                axes[w, c].set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)
        plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
        plt.show()
        return
