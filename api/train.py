import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac

from common.sql import SQLiteClass
from common.utils import fintuning_layout, distillation_layout




# 注册 train 的回调
def register_callbacks_train(app):

    # 页面初始化时候调用
    @callback(
        Output('train-radio', 'value'),
        Input('train-container', 'children'),
        prevent_initial_call=False,
    )
    def train_radio(children):
        if children:
            return 'fintuning'
        else:
            return dash.no_update
    
    # radio变化事件
    @callback(
        Output('train-main', 'children'),
        Input('train-radio', 'value'),
        prevent_initial_call=False,
    )
    def train_radio_change(value):
        if value == 'fintuning':
            return fintuning_layout
        else:
            return distillation_layout
        
        
    
    # lossplot
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_lossplot'
            ),
            Output('lossplot', 'children'),
            Input('lossplot', 'data')
    )
    @app.callback(
        Output('lossplot', 'data'),
        Input('train-main', 'children'),
        prevent_initial_call=True,
    )
    def lossplot(children):
        res = {
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "y": [200, 180, 160, 140, 120, 100, 80, 60, 40, 30, 20, 15, 12, 10, 10]
        }
        return res
        
        
        


    # # 点击详情按钮事件
    # @callback(
    #     Output('url', 'pathname', allow_duplicate=True),
    #     Input({'type': 'train—infobtn', 'index': dash.dependencies.ALL}, 'nClicks'),
    #     prevent_initial_call=True
    # )
    # def train_info_callback(nClicks):
    #     ctx = dash.callback_context
    #     if not ctx.triggered:
    #         raise PreventUpdate

    #     # 获取触发按钮的 ID
    #     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #     button_id = eval(button_id)  # 将字符串转换为字典
    #     key = button_id['index']

    #     # 检查 n_clicks 的值
    #     if not any(nClicks):  # 如果所有按钮的 n_clicks 都为 None 或 0
    #         raise PreventUpdate

    #     return f'/newChat/{key}'
    
    
    # # 点击删除按钮事件
    # @callback(
    #     Output('url', 'pathname', allow_duplicate=True),
    #     Input({'type': 'train—delbtn', 'index': dash.dependencies.ALL}, 'nClicks'),
    #     prevent_initial_call=True
    # )
    # def train_info_callback(nClicks):
    #     ctx = dash.callback_context
    #     if not ctx.triggered:
    #         raise PreventUpdate

    #     # 获取触发按钮的 ID
    #     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #     button_id = eval(button_id)  # 将字符串转换为字典
    #     key = button_id['index']

    #     # 检查 n_clicks 的值
    #     if not any(nClicks):  # 如果所有按钮的 n_clicks 都为 None 或 0
    #         raise PreventUpdate
        
    #     isdel = train_delone(key)
    #     if isdel:
    #         return f'/train'
    #     else:
    #         return dash.no_update        
        
        
    # # 点击删除全部
    # @callback(
    #     Output('url', 'pathname', allow_duplicate=True),
    #     Input('train—delAllbtn', 'nClicks'),
    #     prevent_initial_call=True
    # )
    # def train_info_callback(nClicks):
    #     if nClicks:
    #         isdelAll = train_delAll()
    #         if isdelAll:
    #             return f'/train'
    #         else:
    #             return dash.no_update
    #     else:
    #         return dash.no_update


    # # 点击查询 title or content
    # @callback(
    #     Output('train-content', 'children', allow_duplicate=True),
    #     Input('train—search', 'nClicksSearch'),
    #     State('train—search', 'value'),
    #     State('loginStatus', 'data'),
    #     prevent_initial_call=True,
    # )
    # def train_likesearch(nClicksSearch, value, loginStatus):
    #     try:
    #         if nClicksSearch:
                
    #             usr = loginStatus['username']
    #             train_data = train(usr, input=value)
    #             res = traindatatohtml(train_data)
                
    #             return res
    #         else:
    #             return dash.no_update
            
    #     except Exception as e:
    #         return dash.no_update