

// 在独立js脚本中定义比较长的回调函数
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
    
        // loss
        func_lossplot: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('lossplot'));

            const option = {
                title: {
                    text: 'LOSS',
                    left: 'center',
                    itemStyle: {
                        fontSize: 10,
                    }
                },
                grid: {
                    top: '2%',
                    left: '2%',
                    right: '2%',
                    bottom: '2%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                color: ['#1f63fb'],
                xAxis: {
                    data: data['x'],
                    axisLine: {
                        show: true
                    },
                    axisTick: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'value',
                    axisLine: {
                        show: true
                    },
                    splitLine: {
                        show: false
                    }
                },
                series: [
                    {
                        data: data['y'],
                        type: 'line',
                        smooth: true,
                        label: {
                            show: false // 不显示每个数据点的标签
                        },
                        itemStyle: {
                            opacity: 0 // 隐藏数据点的点
                        }
                    }
                ]
            };

            // 渲染
            myChart.setOption(option);
        },


    }
})