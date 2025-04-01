const plot = echarts.init(document.getElementById('plot'));
var pie_chart = echarts.init(document.getElementById('pie_chart'));

const plot_options = {
    tooltip: {
        trigger: 'item',
        backgroundColor: "rgba(20, 20, 20, 0.7)",
        textStyle: {
            color: '#fff'
        },
        formatter: function (params) {
            return `
                <strong>Post title</strong><br/>
                Subreddit: r/politics<br/>
                Upvotes: 1009<br/>
                Comments: 93<br/>
                Posted on 11.10.23<br/>
                <span style="font-size:0.7rem">Click to see on Reddit</span>
            `;
        }
    },
    xAxis: {
        type: 'category',
        data: Array.from({ length: 30 }, (_, i) => `October ${i + 1}`),
        axisLine: {
            lineStyle: {
                color: 'rgb(196, 196, 196)'
            }
        },
        axisLabel: {
            color: 'rgb(196, 196, 196)'
        }
    },
    yAxis: {
        type: 'value',
        axisLine: {
            lineStyle: {
                color: 'rgb(196, 196, 196)'
            }
        },
        axisLabel: {
            color: 'rgb(196, 196, 196)'
        }
    },
    series: [{
        data: Array.from({ length: 50 }, () => Math.floor(Math.random() * 100)),
        type: 'scatter',
        symbolSize: 10,
        itemStyle: {
            color: 'rgb(255, 102, 0)'
        }
    }],
    dataZoom: [{
        type: 'slider',
        xAxisIndex: [0],
        start: 0,
        end: 100,
        handleStyle: {
            color: 'rgb(255, 255, 255)',
            borderColor: 'white',
            borderWidth: 1
        },
        backgroundColor: 'rgba(0, 0, 0, 0.1)',
        fillerColor: 'rgba(255, 94, 0, 0.13)',
        borderColor: 'rgb(255, 196, 172)'
    }],
    grid: {
        left: 30,
        right: 15,
        top: 20,
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        borderColor: 'rgba(161, 0, 0, 0.8)'
    },
};

const pie_options = {
    title: {
        text: 'ECharts Pie Chart',
        left: 'center', 
        textStyle: {
            color: '#ffffff'
        }
    },
    tooltip: {
        trigger: 'item'
    },
    legend: [
        {
            data: ['Search Engine', 'Direct', 'Union Ads', 'Email', 'Search Engine1', 'Direct1', 'Video Ads33333333333 333333333333333', 'Union Ads1', 'Email1','Search Engine2', 'Direct2', 'Union Ads2', 'Email2', 'Search Engine3', 'Direct3', 'Union Ads3', 'Email3'],
            left: 'left',
            orient: 'vertical',
            textStyle: {
                color: '#ffffff'
            }
        },
        {
            data: ['Union Ads', 'Email', 'Video Ads33333333333 333333333333333'],
            right: 'right',
            orient: 'vertical',
            textStyle: {
                color: '#ffffff'
            }
        }
    ],
    series: [
        {
            name: 'Main Categories',
            type: 'pie',
            radius: ['0%', '40%'],
            center: ['50%', '50%'],
            label: { show: false },
            data: [
                { value: 1048, name: 'Search Engine', itemStyle: {color: 'green'} },
                { value: 735, name: 'Direct', itemStyle: {color: 'red'} },
            ]
        },
        {
            name: 'Main Categories',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            label: { show: false },
            data: [
                { value: 1048, name: 'Search Engine', itemStyle: {color: 'white'} },
                { value: 735, name: 'Direct', itemStyle: {color: 'white'} },
                { value: 580, name: 'Email', itemStyle: {color: 'white'} },
                { value: 484, name: 'Union Ads', itemStyle: {color: 'white'} },
                { value: 300, name: 'Video Ads', itemStyle: {color: 'white'} },
                { value: 1048, name: 'Search Engine1' },
                { value: 735, name: 'Direct1' },
                { value: 580, name: 'Email1' },
                { value: 484, name: 'Union Ads1' },
                { value: 300, name: 'Video Ads1' },
                { value: 1048, name: 'Search Engine2' },
                { value: 735, name: 'Direct2' },
                { value: 580, name: 'Email2' },
                { value: 484, name: 'Union Ads2' },
                { value: 300, name: 'Video Ads2' },
                { value: 1048, name: 'Search Engine3' },
                { value: 735, name: 'Direct3' },
                { value: 580, name: 'Email3' },
                { value: 484, name: 'Union Ads3' },
                { value: 300, name: 'Video Ads33333333333 333333333333333' }
            ]
        }
    ],
    grid: {
        left: 0,
        right: 0,
        top: 0
    }
};

window.addEventListener('resize', () => {
    plot.resize();
});

plot.setOption(plot_options);
pie_chart.setOption(pie_options);

plot.on('click', function (params) {
    window.open("https://www.youtube.com/watch?v=xvFZjo5PgG0");
});