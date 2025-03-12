import dash
from dash import html, dcc, Input, Output, callback, State, callback_context
from dash.dependencies import ClientsideFunction, ALL
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac

from common.sql import SQLiteClass
import json
import datetime
import uuid


# 新增API
def api_create_def(*kwargs):
    
    title = kwargs[0]['title']
    desc = kwargs[0]['desc']
    apitype = kwargs[0]['apitype']
    content = kwargs[0]['content']
    creator = kwargs[0]['creator']

    key = str(uuid.uuid4())
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "key": f"api_{key}",
        "title": title,
        "desc": desc,
        "path": f"path_{key}",
        "apitype": apitype,
        "content": content,
        "status": '0',
        "isdel": '0',
        "creator": creator,
        "createtime": nowtime,
        "updatetime": nowtime,
    }
    with SQLiteClass("./acebergAi.db") as cursor:
        affected_rows = cursor.insert_data("api", data)
    
    return affected_rows


# api查询 all
def api_queryAll_def(creator):
    with SQLiteClass("./acebergAi.db") as cursor:
        res = cursor.select_data("api", "*", condition=f"isdel='0' and creator='{creator}' order by createtime desc")
    return res


# status修改
def api_status_def(key, status):
    with SQLiteClass("./acebergAi.db") as cursor:
        res = cursor.update_data("api", {"status": '1' if status else '0'}, condition=f"isdel='0' and key='{key}'")
    return res

# isdel修改
def api_del_def(key):
    with SQLiteClass("./acebergAi.db") as cursor:
        res = cursor.update_data("api", {"isdel": '1'}, condition=f"key='{key}'")
    return res

# update 单条回显
def api_queryOne_def(key):
    with SQLiteClass("./acebergAi.db") as cursor:
        res = cursor.select_data("api", "*", condition=f"key='{key}'")
    return res
def api_updateOne_def(key, data):
    with SQLiteClass("./acebergAi.db") as cursor:
        res = cursor.update_data("api", data, condition=f"key='{key}'")
    return res

# data=[
#     {'key': '1', 'title': 'John Brown', 'desc': 'asasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdaasdasdasdasdasdadasdasdasdasda', 'path': 'New York No. 1 Lake Park','status': '1', 'isdel': '0'},
#     {'key': '2', 'title': 'Jim Green', 'desc': '42', 'path': 'London No. 1 Lake Park','status': '1', 'isdel': '0'},
#     {'key': '3', 'title': 'Joe Black', 'desc': '32', 'path': 'Sidney No. 1 Lake Park','status': '0', 'isdel': '0'},
# ]

# 数据变成卡片 
def apitohtml(data):
    res = []
    for item in data:
        card = html.Div(
            className='api-card',
            key=item['key'],    # key是唯一标识
            children=[
                html.Div(
                    className='api-card-header',
                    children=[
                        html.Div(
                            [
                                item['title']
                            ],
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-between',
                                'alignItems': 'center',
                                'width': '120px',
                                'height': '26px',
                                'font-size': '14px',
                                'font-weight': 'bold',
                                'overflow': 'hidden',
                            })
                        ,
                        html.Div(
                            children=[
                                fac.AntdButton(
                                    icon=fac.AntdIcon(icon='antd-edit'),
                                    type='text',
                                    color='default',
                                    variant='filled',
                                    size='small',
                                    id={'type': 'edit', 'index': f"edit@{item['key']}"},
                                ),
                                fac.AntdSwitch(
                                    size='small',
                                    checked=True if item['status'] == '1' else False,
                                    style={
                                        'marginLeft': 8
                                    },
                                    # id=f"switch@{item['key']}"
                                    id={'type': 'switch', 'index': f"switch@{item['key']}"}, 
                                    
                                ),
                                fac.AntdButton(
                                    icon=fac.AntdIcon(icon='antd-delete'),
                                    type='text',
                                    color='default',
                                    variant='filled',
                                    size='small',
                                    style={
                                        'marginLeft': 8
                                    },
                                    id={'type': 'del', 'index': f"del@{item['key']}"},
                                    # key=f"{item['key']}"
                                ),
                            ],
                            # style={
                            #     'width': 'calc(100% - 120px)'
                            # }
                        )
                    ],
                    style={
                        'width': '100%',
                        'height': '30px',
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'alignItems': 'center',
                    },
                ),
                html.Div(
                    item['desc'],
                    className='api-card-body',
                    style={
                        'marginTop': 8,
                        'width': '100%',
                        'height': '100px',
                        'color': '#5e6671',
                        'fontSize': '10px',
                        'overflow': 'hidden',  # 或 'scroll' 按需显示滚动条
                        'whiteSpace': 'pre-line',  # 保留换行符并自动换行
                        'wordWrap': 'break-word',  # 强制长单词/URL换行
                        'textOverflow': 'ellipsis'  # 可选：溢出时显示省略号（需配合 overflow:hidden）
                    },
                )
            ],
            style={
                'border': '1px solid #f1f1f1',
                'padding': '10px',
                'width': 'calc(calc(100% / 4) - 30px)',
                'height': '140px',
                'borderRadius': '6px'
            },
        )
        res.append(card)
    return res
    



# 注册 api 的回调
def register_callbacks_api(app):
    global apidata
    apidata = []
    
    # 页面初始化时候调用
    @app.callback(
        Output('api-items', 'children'),
        Input('url', 'pathname'),
        State('loginStatus', 'data'),
        prevent_initial_call=False,
    )
    def api_init(pathname, loginStatus):
        creator = loginStatus['username']
        if pathname:
            apidata = api_queryAll_def(creator)
            
            dom = apitohtml(apidata)
                
            return dom
        else:
            return dash.no_update
        
    
    # 点击创建
    @app.callback(
        Output('api-create-title', 'value'),
        Output('api-create-desc', 'value'),
        Output('api-create-apitype', 'value'),
        Output('api-create-content', 'value'),
        Output('api-modal-create', 'visible'),
        
        Input('api-create', 'nClicks'),
        prevent_initial_call=True,
    )
    def api_create(nClicks):
        if nClicks:
            return '', '', 'model', '', True
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        
    # 点击radio
    @app.callback(
        Output('api-create-content', 'options'),
        Input('api-create-apitype', 'value'),
        prevent_initial_call=True,
    )
    def api_create_apitype(radio):
        modellist = [
            {'label': 'qwen-7B', 'value': 'qwen-7B'},
            {'label': 'deepseek-R1', 'value': 'deepseek-R1'},
            {'label': 'deepseek-V3', 'value': 'deepseek-V3'},
            {'label': 'gpt-3.5-turbo', 'value': 'gpt-3.5-turbo'},
        ]
        
        vectorlist = [
            {'label': 'fassi-1', 'value': 'fassi-1'},
            {'label': 'fassi-2', 'value': 'fassi-2'},
            {'label': 'fassi-3', 'value': 'fassi-3'},
            {'label': 'chroma-1', 'value': 'chroma-1'},
        ]
        
        if radio == 'model':
            return modellist
        else:
            return vectorlist


    # 点击确认新增
    @app.callback(
        Output('api-items', 'children', allow_duplicate=True),
        
        Input('api-modal-create', 'okCounts'),
        State('api-create-title', 'value'),
        State('api-create-desc', 'value'),
        State('api-create-apitype', 'value'),
        State('api-create-content', 'value'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    def api_create_confirm(okCounts, title, desc, apitype, content, loginStatus):
        if okCounts:
            creator = loginStatus['username']
            args = {
                'title': title,
                'desc': desc,
                'apitype': apitype,
                'content': content,
                'creator': creator,
            }
            isadd = api_create_def(args)
            if isadd:
                apidata = api_queryAll_def(creator)
                  
                res = apitohtml(apidata)
                
                return res
            else:
                return dash.no_update
        else:
            return dash.no_update
    
    
    
    # 每一个卡片的switch按钮@
    @app.callback(
        Output('api-message', 'children'),
        Input({'type': 'switch', 'index': ALL}, 'checked'),    # 获取组件的完整 ID
        prevent_initial_call=True
    )
    def api_item_switch(checked_list):
        ctx = callback_context
        
        # 1. 排除初始加载或非用户交互触发
        if not ctx.triggered or ctx.triggered[0]['value'] is None:
            raise PreventUpdate
        
        # 2. 获取触发组件的 ID
        trigger_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        try:
            trigger_id = json.loads(trigger_id_str)
        except json.JSONDecodeError:
            raise PreventUpdate
        
        # 3. 验证是否为合法触发源
        if trigger_id.get('type') != 'switch':
            raise PreventUpdate
        
        # 4. 提取 item_id 和状态
        item_key = trigger_id['index'].split('@')[1]  # 假设 ID 格式为 "类型@唯一ID"
        status = ctx.triggered[0]['value']
        
        # 5. 执行更新逻辑
        issuccess = api_status_def(item_key, status)
        
        return dash.no_update





    # 每一个卡片的del按钮 显示Modal
    @app.callback(
        Output('api-modal-del', 'key', allow_duplicate=True),
        Output('api-modal-del', 'visible', allow_duplicate=True),
        Input({'type': 'del', 'index': ALL}, 'nClicks'),
        prevent_initial_call=True
    )
    def api_item_del(nClicks):
        if nClicks:
            ctx = callback_context
            
            # 1. 排除初始加载或非用户交互触发
            if not ctx.triggered or ctx.triggered[0]['value'] is None:
                raise PreventUpdate
            
            # 2. 获取触发组件的 ID
            item_key = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index'].split('@')[1]
            
            return item_key, True
        else:
            return dash.no_update, dash.no_update
    
    
    
    @app.callback(
        Output('api-message', 'children', allow_duplicate=True),
        Output('api-items', 'children', allow_duplicate=True),
        Input('api-modal-del', 'okCounts'),
        State('api-modal-del', 'key'),
        State('loginStatus', 'data'),
        prevent_initial_call=True
    )
    def api_item_del(okCounts, key, loginStatus):
        if okCounts:
            issuccess = api_del_def(key)
            message = fac.AntdMessage(
                content="删除成功" if issuccess else "删除失败",
                type="success" if issuccess else "error"
            )
            
            creator = loginStatus['username']
            alldata = api_queryAll_def(creator)
            dom = apitohtml(alldata)
            
            return message, dom
        else:
            return None, None
        
        
        
    # 每一个卡片的edit按钮 显示Modal
    @app.callback(
        Output('api-modal-edit', 'key', allow_duplicate=True),
        Output('api-modal-edit', 'visible', allow_duplicate=True),
        Output('api-edit-title', 'value', allow_duplicate=True),
        Output('api-edit-desc', 'value', allow_duplicate=True),
        Output('api-edit-apitype', 'value', allow_duplicate=True),
        Output('api-edit-content', 'value', allow_duplicate=True),
        Output('api-edit-path', 'value', allow_duplicate=True),
        
        
        Input({'type': 'edit', 'index': ALL}, 'nClicks'),
        prevent_initial_call=True
    )
    def api_item_del(nClicks):
        if nClicks:
            ctx = callback_context
            # 1. 排除初始加载或非用户交互触发
            if not ctx.triggered or ctx.triggered[0]['value'] is None:
                raise PreventUpdate
            # 2. 获取触发组件的 ID
            item_key = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index'].split('@')[1]
            
            apidataone = api_queryOne_def(item_key)[0]
            return (
                item_key, 
                True, 
                apidataone['title'], 
                apidataone['desc'], 
                apidataone['apitype'],
                apidataone['content'], 
                apidataone['path']
            )
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    
    # 编辑 API 更新后
    @app.callback(
        Output('api-message', 'children', allow_duplicate=True),
        Output('api-items', 'children', allow_duplicate=True),
        
        Input('api-modal-edit', 'okCounts'),
        State('api-modal-edit', 'key'),
        State('api-edit-title', 'value'),
        State('api-edit-desc', 'value'),
        State('api-edit-apitype', 'value'),
        State('api-edit-content', 'value'),
        State('loginStatus', 'data'),
        prevent_initial_call=True
    )
    def api_item_edit(okCounts, key, title, desc, apitype, content,  loginStatus):
        if okCounts:
            data = {
                'title': title,
                'desc': desc,
                'apitype': apitype,
                'content': content
            }
            issuccess = api_updateOne_def(key, data)
            message = fac.AntdMessage(
                content="更新成功" if issuccess else "更新失败",
                type="success" if issuccess else "error"
            )
            
            creator = loginStatus['username']
            alldata = api_queryAll_def(creator)
            dom = apitohtml(alldata)
            
            return message, dom
        else:
            return None, None
        




# 提供resful api方法 通过统一接口方法启服务，根据key去做不通任务
# rag 或者 通用chat
# 入参
