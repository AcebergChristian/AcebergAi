import dash
from dash import html, dcc, Input, Output, callback, State

from common.utils import getchatData, chatdatatohtml, newchat_update_content, get_ai_answer

import json
import time





fakedata = [
    {
        "key": "bot_00001",
        "role": "bot",
        "content": "你好，我是你的智能助手，有什么可以帮助你的吗？",
    },
    {"key": "usr_00002", "role": "usr", "content": "我想请问一下，最近有什么新闻吗？"},
    {
        "key": "bot_00003",
        "role": "bot",
        "content": """最近有一个关于人工智能的新闻，你感兴趣吗？最近有一个关于人工智能的新闻，你感兴趣吗？
                                 最近有一个关于人工智能的新闻，你感兴趣吗？最近有一个关于人工智能的新闻，你感兴趣吗？
                                 最近有一个关于人工智能的新闻，你感兴趣吗？""",
    },
    {"key": "usr_00004", "role": "usr", "content": "是的，我非常感兴趣。"},
    {
        "key": "bot_00005",
        "role": "bot",
        "content": "好的，我会尽快为你提供最新的新闻资讯。",
    },
]



import datetime




# def chatdatatohtml(data):
#     # 初始化容器
#     res = []
#     # 遍历对话数据
#     for idx, item in enumerate(data):
#         # 历史记录中的其他消息（静态）
#         if item['role'] != 'bot' or idx != len(data)-1:
#             if item['role'] == 'bot':
#                 res.append(
#                     html.Div(
#                         [
#                             html.Div(item['role'], className="newChat_avator"),
#                             html.Div(item['content'], className=f"newChat_text newChat_text_{item['role']}", id=f"content@{item['key']}"),
#                             fac.AntdCopyText(
#                                 id=f"copy@{item['key']}",
#                                 text=item['content'],
#                                 beforeIcon=fac.AntdButton(
#                                     icon=fac.AntdIcon(icon="antd-copy", style={"color": "#5e6671"}),
#                                     color="default",
#                                     variant="filled",
#                                     id=f"copy@{item['key']}"
#                                 )
#                             ),
#                         ],
#                         className=f"newChat_{item['role']}"
#                     )
#                 )
#             else:
#                 res.append(
#                     html.Div(
#                         [
#                             fac.AntdCopyText(
#                                 id=f"copy@{item['key']}",
#                                 text=item['content'],
#                                 beforeIcon=fac.AntdButton(
#                                     icon=fac.AntdIcon(icon="antd-copy", style={"color": "#5e6671"}),
#                                     color="default",
#                                     variant="filled",
#                                     id=f"copy@{item['key']}"
#                                 )
#                             ),
#                             html.Div(item['content'], className=f"newChat_text newChat_text_{item['role']}", id=f"content@{item['key']}"),
#                             html.Div(item['role'], className="newChat_avator")
#                         ],
#                         className=f"newChat_{item['role']}"
#                     )
#                 )
#         # 最后一条AI消息（流式）
#         else:
#             res.append(
#                 html.Div(
#                     id=f"streaming-div-{item['key']}",
#                     className=f"newChat_{item['role']}"
#                 )
#             )
#     return res


global newChat_current_chatlist
newChat_current_chatlist = []

# 注册 newChat 的回调
def register_callbacks_newChat(app):
    
    # 页面初始化时候调用
    @callback(
        Output("newChat-content", "children"),
        Output("newChat-input", "value", allow_duplicate=True),
        
        Input("layout-mainContent", "children"), 
        Input('url', 'pathname'),
        prevent_initial_call='initial_duplicate'
    )
    def newChat_chatContent(children, pathname):
        if children:
            
            # 清空当前聊天列表
            newChat_current_chatlist.clear()
        
            key = pathname.split('/')[-1]
            title, content = getchatData(key)  # 获取新的聊天数据
            newChat_current_chatlist.extend(content)  # 将新数据追加到现有列表中
            
            
            res = chatdatatohtml(newChat_current_chatlist)
            
            # 复制功能
            for item in newChat_current_chatlist:
                newChat_copy_callback(item)
                
            return res, title
        
        else:
            return dash.no_update, dash.no_update


    # 点击复制按钮
    def newChat_copy_callback(item):
        @callback(
            Output(f"copy@{item['key']}", "text"),
            Input(f"copy@{item['key']}", "nClicks"),
            State(f"content@{item['key']}", "children"),
            prevent_initial_call=True,
        )
        def newChat_content_copy(nClicks, children):
            if nClicks:
                return children
            return dash.no_update

    

    # 点击发送按钮
    @callback(
        Output("newChat-content", "children", allow_duplicate=True),
        Output("newChat-input", "value", allow_duplicate=True),
        Output("newChat-timeout", "delay"),
        
        Input('url', 'pathname'),
        Input(f"newChat-inputarea-send", "nClicks"),
        State(f"newChat-model", "value"),
        State(f"newChat-input", "value"),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    def newChat_content_sendinput(pathname, nClicks, model, value, loginStatus):
        if nClicks and value:
            
            # 添加用户输入到历史记录
            newChat_current_chatlist.append(
                {"key": f"usr_{len(newChat_current_chatlist)}", "role": "usr", "content": value}
            )
            newChat_current_chatlist.append(
                {"key": f"bot_{len(newChat_current_chatlist)}", "role": "bot", "content": 'loading'}
            )

            # [] 渲染成dom
            res = chatdatatohtml(newChat_current_chatlist)
            html.Script("document.getElementById('newChat-content').scrollTop = document.getElementById('newChat-content').scrollHeight;")
            
            key = pathname.split('/')[-1]
            # 更新数据库的用户对话字段
            newchat_update_content(key, json.dumps(newChat_current_chatlist, ensure_ascii=False)) 


            
            return res, "", 300
        else:
            return dash.no_update, dash.no_update, dash.no_update


    # 调API callback 方法
    @callback(
        Output("newChat-content", "children", allow_duplicate=True),
        
        Input('url', 'pathname'),
        Input('newChat-timeout', 'timeoutCount'),
        State(f"newChat-model", "value"),
        prevent_initial_call=True,
    )
    def get_ai_answerdef_callback(pathname, timeoutCount, model):
        if timeoutCount:
            usr_input = newChat_current_chatlist[-2]["content"]
            res = get_ai_answer(model, usr_input)
            if res:
                newChat_current_chatlist[-1]["content"] = res
                
                
                # 更新数据库的用户对话字段
                key = pathname.split('/')[-1]
                newchat_update_content(key, json.dumps(newChat_current_chatlist, ensure_ascii=False)) 
                resdom = chatdatatohtml(newChat_current_chatlist)
                    
                return resdom
                
            else:
                return dash.no_update
        return dash.no_update
        
        
        
    # interval 开启
    # @callback(
    #     Output("newChat-content", "children", allow_duplicate=True),
    #     Output("newChat-streaminterval", "disabled", allow_duplicate=True),
    #     Output("newChat-streaminterval", "n_intervals", allow_duplicate=True),
        
    #     Input("newChat-streaminterval", "n_intervals"),
    #     Input('url', 'pathname'),
    #     prevent_initial_call=True,
    # )
    # def update_ai_response(n_intervals, pathname):
    #     pass
        
        # response_text = get_ai_answer(model, user_input)
        # full_text = response_text.split('\n')  # 将返回的文本按行分割成列表
        # print('full_text==========>', full_text)
        
        # return dash.no_update, dash.no_update, dash.no_update
        
        # if n_intervals == 5:  # 3秒后开始流式输出（假设interval为500ms）
        #     last_bot_msg = newChat_current_chatlist[-1]
        #     if last_bot_msg["role"] == "bot" and last_bot_msg["content"] == 'loading':
        #         last_bot_msg["content"] = ""  # 移除"loading"
        #         res = chatdatatohtml(newChat_current_chatlist)
        #         return res, False, dash.no_update  # 更新内容并继续流式输出

        # if n_intervals > 5:
        #     last_bot_msg = newChat_current_chatlist[-1]
        #     if last_bot_msg["role"] == "bot":
                
        #         response_text = get_ai_answer(model, user_input)
        #         full_text = response_text.split('\n')  # 将返回的文本按行分割成列表
                
                
        #         if n_intervals < len(full_text) + 6:
        #             next_segment = full_text[n_intervals - 6]
        #             last_bot_msg["content"] += next_segment
        #             res = chatdatatohtml(newChat_current_chatlist)
        #             return res, False, dash.no_update  # 继续流式输出
        #         else:
        #             # 结束后，更新数据库的content字段
        #             key = pathname.split('/')[-1]
        #             newchat_update_content(key, json.dumps(newChat_current_chatlist, ensure_ascii=False))
                    
        #             return dash.no_update, True, None  # 停止定时器
        #     else:
        #         return dash.no_update, dash.no_update, dash.no_update
        
        # else:
        #     return dash.no_update, dash.no_update, dash.no_update

