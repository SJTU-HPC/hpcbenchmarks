import math
import json
import copy
import time
from setting import CLUSTER_SCALE, CLUSTER_NAME
from utils.tool import Tool, dict_to_obj
import pyecharts.options as opts
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from pyecharts.charts import Radar
from utils.result import get_result

test_result_file = "result/test_result.json"
standard_file = "utils/standard_score.json"
test_score_file = "result/test_score.json"

tool = Tool()

def read_file(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def get_evaluate(result):
    issue_map = {'AI':'AI计算', 'compute':'计算', 'storage':'存储', 'network':'网络', 'system':'能效', 'balance':'系统平衡性'}
    good = []
    better = []
    for k in issue_map:
        score = result[k].issue_score
        if score < 70:
            better.append(issue_map[k])
        else:
            good.append(issue_map[k])
    return good, better

def get_score():
    test_result = get_result() # read_file(test_result_file)
    CLUSTER_SCALE = tool.get_scale(test_result['compute']['HPL'])
    standard = read_file(standard_file)
    sum_score = 0
    for issue, sub_issue in standard.items():
        issue_score = 1
        for norm, value in sub_issue.items():
            try:
                norm_score = test_result[issue][norm] / (value[CLUSTER_SCALE] * 0.8) * 100
            except Exception:
                norm_score = eval(test_result[issue][norm]) / ((eval(value[CLUSTER_SCALE])) * 0.8) * 100
            if norm_score > 100:
                norm_score = 100
            standard[issue][norm]["score"] = norm_score
            issue_score *= math.pow(norm_score, value["weights"])
        standard[issue]["issue_score"] = issue_score
        sum_score += issue_score / 6
    standard["sum_score"] = sum_score

    tool.write_file(test_score_file, json.dumps(standard, ensure_ascii=False))

    res = dict_to_obj(standard)
    good, better = get_evaluate(res)

    data = [[round(res.compute.issue_score, 2),
            round(res.AI.issue_score, 2),
            round(res.storage.issue_score, 2),
            round(res.network.issue_score, 2),
            round(res.system.issue_score, 2),
            round(res.balance.issue_score, 2)]]
    c = (
        Radar(init_opts=opts.InitOpts())
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="计算", max_=100),
                opts.RadarIndicatorItem(name="AI", max_=100),
                opts.RadarIndicatorItem(name="存储", max_=100),
                opts.RadarIndicatorItem(name="网络", max_=100),
                opts.RadarIndicatorItem(name="能效", max_=100),
                opts.RadarIndicatorItem(name="平衡性", max_=100),
            ],
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            textstyle_opts=opts.TextStyleOpts(color="#000000"),
        )
        .add(
            series_name="Score",
            data=data,
            areastyle_opts=opts.AreaStyleOpts(color="#FF0000", opacity=0.2), 
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"综合分：{res.sum_score:.2f}", pos_right=True),
            legend_opts=opts.LegendOpts(selected_mode="single")
        )
        
    )

    logger.info(f"create RadarMap for {CLUSTER_SCALE} cluster")

    env = Environment(loader=FileSystemLoader("./utils"))
    template = env.get_template('report_tmp.html')

    data = copy.deepcopy(standard)
    data['radarmap'] = c.dump_options_with_quotes()
    data['scale'] = CLUSTER_SCALE
    data['scale_CN'] = {'small':'小', 'medium':'中', 'large':'大'}[CLUSTER_SCALE]
    data['test'] = test_result
    data['good'] = '、'.join(good)
    data['better'] = '、'.join(better)
    data['time'] = time.strftime("%Y.%m.%d", time.localtime())
    data['name'] = CLUSTER_NAME

    with open('Report.html', 'w') as f:
        f.write(template.render(data))

