const chart = echarts.init(document.getElementById('chart'));

const options = {
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
window.addEventListener('resize', () => {
    chart.resize();
});

chart.setOption(options);

chart.on('click', function (params) {
    window.open("https://www.youtube.com/watch?v=xvFZjo5PgG0");
});