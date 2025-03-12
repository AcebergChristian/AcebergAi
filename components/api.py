import dash
from dash import html
import feffery_antd_components as fac

api_layout = html.Div(
    [   
        html.Div(id='api-message'),
        
        html.Div(
            [
                html.Div(
                    [
                        fac.AntdButton(
                            '创建',
                            id="api-create",
                            icon=fac.AntdIcon(icon='md-add-box'),
                            type='primary',
                            style={
                                "marginLeft": 20
                            },
                        ),
                    ],
                    id="api-bar",
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "flex-start",
                        "width": "100%",
                        "height": 60,
                        "backgroundColor": "#f3f5fa",
                    },
                ),
                html.Div(
                    [],
                    id="api-items",
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "flexWrap": "wrap",
                        "justifyContent": "flex-start",
                        "alignItems": "flex-start",
                        "alignContent": "flex-start",
                        "gap": 10,
                        "width": "100%",
                        "height": "calc(100% - 120px)",
                        # "backgroundColor": "#5525f1",
                        "overflowY": "auto",
                    },
                ),
            ],
            id="api-content",
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center",
                "gap": 10,
                "width": "84%",
                "height": "100%",
            },
        ),
        
        
        # 新增modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='api-create-title',
                                name = 'title'
                            ),
                            label='title'
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='api-create-desc',
                                name = 'desc'
                            ),
                            label='desc'
                            
                        ),
                        fac.AntdFormItem(
                            fac.AntdRadioGroup(
                                id='api-create-apitype',
                                options=[
                                    {'label': 'model', 'value': 'model'},
                                    {'label': 'vector', 'value': 'vector'}
                                ],
                                defaultValue='model',
                                optionType='button',
                                buttonStyle='solid',
                                name = 'apitype'
                            ),
                            label='apitype'
                        ),
                        fac.AntdFormItem(
                            fac.AntdSelect(
                                id='api-create-content',
                                name = 'content'
                            ),
                            label='content'
                        ),
                        
                        
                    ],
                    id='api-create-form',
                    labelCol={'span': 4},
                    wrapperCol={'span': 20},
                    labelAlign='left',
                    style={'width': 300},
                )
            ],
            id='api-modal-create',
            title='创建API',
            renderFooter=True,
        ),
        
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='api-edit-title',
                                name = 'title'
                            ),
                            label='title'
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='api-edit-desc',
                                name = 'desc'
                            ),
                            label='desc'
                            
                        ),
                        fac.AntdFormItem(
                            fac.AntdRadioGroup(
                                id='api-edit-apitype',
                                options=[
                                    {'label': 'model', 'value': 'model'},
                                    {'label': 'vector', 'value': 'vector'}
                                ],
                                defaultValue='model',
                                optionType='button',
                                buttonStyle='solid',
                                name = 'apitype'
                            ),
                            label='apitype'
                        ),
                        fac.AntdFormItem(
                            fac.AntdSelect(
                                id='api-edit-content',
                                name = 'content'
                            ),
                            label='content'
                        ),
                        fac.AntdFormItem(
                                fac.AntdInput(
                                    id='api-edit-path',
                                    name = 'path',
                                    disabled=True
                                ),
                                label='path'
                        ),
                        
                        
                        
                    ],
                    id='api-edit-form',
                    labelCol={'span': 4},
                    wrapperCol={'span': 20},
                    labelAlign='left',
                    style={'width': 300},
                )
            ],
            id='api-modal-edit',
            title='更新API',
            renderFooter=True,
        ),
        
        fac.AntdModal(
            '确认删除该API？',
            id='api-modal-del',
            title='删除API',
            renderFooter=True,
        ),
    ],
    id="api-container",
    style={
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "width": "100%",
        "height": "100%",
        "backgroundColor": "#ffffff",
    },
    
    
)
