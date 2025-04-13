// Charts
const plot = echarts.init(document.getElementById('plot'));
const pie_chart = echarts.init(document.getElementById('pie_chart'));

// Django data
const django_data = JSON.parse(document.getElementById('django_data').textContent);

const subreddits = django_data['subreddit_activity'];
const posts = django_data['posts'];
const comments = django_data['comments'];

// Functions
function limit_text_width (text, max_width) {
    let words = text.split(" ");
    let result = words[0];
    
    for (let i = 1; i < words.length; i += 1) {
        if (words[i-1].length + words[i].length > max_width) {
            result += '\n' + words[i]
        }
        else {
            result += " " + words[i]
        }
    }

    return result
}

function fill_subreddits_table(sort_criteria) {
    const table = document.getElementById('table-body')
    function clear_criterias() {
        document.getElementById('table-head').children[0].textContent = "Name"
        document.getElementById('table-head').children[1].textContent = "Posts"
        document.getElementById('table-head').children[2].textContent = "Comments"
        document.getElementById('table-head').children[3].textContent = "Upvotes"
    }
    while (table.firstChild) {
        table.removeChild(table.firstChild);
      }
    if (sort_criteria == "name") {
        subreddits.sort((a, b) => a.name.localeCompare(b.name));
        clear_criterias();
        document.getElementById('table-head').children[0].innerHTML = "Name&nbsp;↓"
    }
    else if (sort_criteria == "posts") {
        subreddits.sort((a, b) => b.posts - a.posts);
        clear_criterias();
        document.getElementById('table-head').children[1].innerHTML = "Posts&nbsp;↓"
    }
    else if (sort_criteria == "comments") {
        subreddits.sort((a, b) => b.comments - a.comments);
        clear_criterias();
        document.getElementById('table-head').children[2].innerHTML = "Comments&nbsp;↓"
    }
    else if (sort_criteria == "upvotes") {
        subreddits.sort((a, b) => b.upvotes - a.upvotes);
        clear_criterias();
        document.getElementById('table-head').children[3].innerHTML = "Upvotes&nbsp;↓"
    }
    for (let i = 0; i < subreddits.length; i += 1) {
        var sub = document.createElement('tr')
        sub.innerHTML = `
            <td>${subreddits[i].name}</td>
            <td>${subreddits[i].posts}</td>
            <td>${subreddits[i].comments}</td>
            <td>${subreddits[i].upvotes}</td>
        `;
        table.appendChild(sub)
    }
}

function scroll_to_analysis() {
    document.getElementById('behaviour-analysis').scrollIntoView({ behavior: 'smooth' });
}

function scroll_to_monitor() {
    document.getElementById('activity-monitor').scrollIntoView({ behavior: 'smooth' });
}

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
        zoomLock: false,
        xAxisIndex: [0],
        start: 0,
        end: 100,
        handleStyle: {
            color: 'rgb(255, 255, 255)',
            borderColor: '#8ad184',
            borderWidth: 1
        },
        handleLabel: {
            show: false
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
    tooltip: {
        trigger: 'item',
        confine: true,
        // rich: {
        //     a: {
        //         lineHeight: 20,
        //         width: 100
        //     }
        // },
        // formatter: function (params) {
        //     return `
        //         <strong>${params.name}</strong><br/>
        //         Value: ${params.value}<br/>
        //         Upvotes: 1009<br/>
        //         Comments: 93<br/>
        //         Posted on 11.10.23<br/>
        //         <span style="font-size:0.7rem">Click to see on Reddit</span>
        //     `;
        // }
    },
    // legend: [
    //     {
    //         type: "scroll",
    //         pageButtonItemGap: 20,
    //         pageIconColor: '#ccc',
    //         pageIconInactiveColor: '#878787',
    //         pageTextStyle: {
    //             color: 'rgb(196, 196, 196)'
    //           },
    //         data: ['No profile picture', 'User is active in too many subreddits', 'Generic username'],
    //         left: 'left',
    //         orient: 'vertical',
    //         textStyle: {
    //             color: '#ffffff'
    //         }, 
    //         formatter: function (text) {
    //             return limit_text_width(text, 10)
    //         }
    //     },
    //     {
    //         type: "scroll",
    //         pageButtonItemGap: 20,
    //         pageIconColor: '#ccc',
    //         pageIconInactiveColor: '#878787',
    //         pageTextStyle: {
    //             color: 'rgb(196, 196, 196)'
    //           },
    //         data: ['User is a moderator', 'Many upvotes on posts', 'Many upvotes on comments', 'Each post is unique', 'Account is 4 years old', 'Account has 22 trophies'],
    //         left: 'right',
    //         orient: 'vertical',
    //         textStyle: {
    //             color: '#ffffff'
    //         },
    //         formatter: function (text) {
    //             return limit_text_width(text, 10)
    //         }
    //     }
    // ],
    series: [
        {
            selectedMode: 'single',
            type: 'pie',
            radius: ['50%', '90%'],
            center: ['50%', '50%'],
            label: { show: false },
            padAngle: 3,
            itemStyle: {
                borderRadius: 5
            },
            data: [
                { value: 1048, name: 'User is a moderator', itemStyle: {color: '#8ad184'} },
                { value: 735, name: 'Many upvotes on posts', itemStyle: {color: '#8ad184'} },
                { value: 580, name: 'Many upvotes on comments', itemStyle: {color: '#8ad184'} },
                { value: 484, name: 'Each post is unique', itemStyle: {color: '#8ad184'} },
                { value: 300, name: 'Account is 4 years old', itemStyle: {color: '#8ad184'} },
                { value: 1048, name: 'Account has 22 trophies', itemStyle: {color: '#8ad184'} },
                { value: 300, name: 'No profile picture', itemStyle: {color: '#ffa8a8'} },
                { value: 1048, name: 'User is active in too many subreddits', itemStyle: {color: '#ffa8a8'} },
                { value: 735, name: 'Generic username', itemStyle: {color: '#ffa8a8'} }
            ]
        }
    ],
    graphic: [{
        type: 'text',
        left: 'center',
        top: '40%',
        style: {
            text: '18%',
            textAlign: 'center',
            fontSize: 48,
            fontWeight: 'bold',
            fill: '#fff'
        }
    }, 
    {
        type: 'text',
        left: 'center',
        top: '55%',
        style: {
            text: 'Very likely not a bot',
            textAlign: 'center',
            fontSize: 12,
            fill: '#fff'
        }
    }],
};

window.addEventListener('resize', () => {
    plot.resize();
    pie_chart.resize();
});

plot.setOption(plot_options);
pie_chart.setOption(pie_options);

plot.on('click', function (params) {
    window.open("https://www.youtube.com/watch?v=xvFZjo5PgG0");
});



// function adjustPiePosition() {
//     const chartWidth = document.getElementById('pie_chart').clientWidth;
//     const chartHeight = document.getElementById('pie_chart').clientHeight;
//     const pieRadius = 0.9 * chartHeight; // Calculate radius based on width

//     // Update the center position
//     pie_chart.setOption({
//         series: [{
//             center: [pieRadius, '50%'] // Set center based on calculated offset
//         }]
//     });
// }

// // Call the function to adjust position initially
// adjustPiePosition();

// // Adjust position on window resize
// window.addEventListener('resize', adjustPiePosition);

document.querySelectorAll('.factor').forEach(factor => {
    const itemName = factor.textContent.trim();
    
    factor.addEventListener('mouseenter', function () {
        pie_chart.dispatchAction({
          type: 'select',
          name: itemName
        });
      });
    
      factor.addEventListener('mouseleave', function () {
        pie_chart.dispatchAction({
          type: 'unselect',
          name: itemName
        });
      });
});

document.addEventListener('DOMContentLoaded', function() {
    fill_subreddits_table("upvotes")
    plot.resize();
});