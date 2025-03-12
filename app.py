from dash import Dash
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import html, dcc
from callbacks import register_callbacks  # 导入注册回调函数的函数
from pages.layout import layout

# 首页
from api.home import register_callbacks_home
# 新建对话
from api.newChat import register_callbacks_newChat
# 对话历史
from api.historyChat import register_callbacks_historyChat
# acebergAis
from api.acebergAis import register_callbacks_acebergAis
# train
from api.train import register_callbacks_train
# api
from api.api import register_callbacks_api
# down
from api.todown import register_callbacks_todown


# 系统管理
from api.userManage import register_callbacks_userManage


import random


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_scripts=[
        'assets/materials/echarts.min.js'   # 'https://cdn.jsdelivr.net/npm/echarts@5.3.0/dist/echarts.min.js',
    ],
    index_string='''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
    )


app.layout = html.Div([
    # 存储到localstorage
    dcc.Store(id='loginStatus', storage_type='local'),
    
    dcc.Location(id='mainurl', refresh=False),
    html.Div(
        id='maincontainer',
        style={
            'width': '100%',
            'height': '100%'
        }
    ), 
    ],
    style={
        'width': '100vw',
        'height': '100vh'
    }
)

# 注册应用内的回调函数
register_callbacks(app)

# 注册各个menu的回调函数
register_callbacks_home(app)
register_callbacks_newChat(app)
register_callbacks_historyChat(app)
register_callbacks_acebergAis(app)
register_callbacks_train(app)
register_callbacks_api(app)
register_callbacks_todown(app)


register_callbacks_userManage(app)



    
if __name__ == '__main__':
    app.run_server(host="127.0.0.1", debug=True, port=8888)