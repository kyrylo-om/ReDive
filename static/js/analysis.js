// Django data
const django_data = JSON.parse(document.getElementById('django_data').textContent);

// Constants
const subreddits = django_data['subreddit_activity'];
const posts = django_data['posts'];
const comments = django_data['comments'];
const posts_and_comments = posts.concat(comments);
const human_factors = django_data['human_points'];
const bot_factors = django_data['bot_points'];
const top_words = django_data['top_words'];
const themes = django_data['themes'];
const sentiment = django_data['sentiment'];

// Elements

const trophies_count = document.getElementById('trophies_count');
const trophies_button = document.getElementById('trophies_button');
const trophies_popup = document.getElementById('trophies_popup');
const analysis_date = document.getElementById('analysis_date');
const statistics_select = document.getElementById('statistics_select');
const browser = document.getElementById('browser');
const analysis_section = document.getElementById('behaviour-analysis');
const monitor_section = document.getElementById('activity-monitor');
const posts_switch = document.getElementById('posts_switch');
const comments_switch = document.getElementById('comments_switch');
const everything_switch = document.getElementById('everything_switch');
const submissions = document.getElementById('submissions');
const search_bar = document.getElementById('submissions-search')
const image_checkbox = document.getElementById('image_checkbox');
const spoiler_checkbox = document.getElementById('spoiler_checkbox');
const nsfw_checkbox = document.getElementById('nsfw_checkbox');
const oc_checkbox = document.getElementById('oc_checkbox');
const subreddit_select = document.getElementById('subreddit_select');
const sort_select = document.getElementById('sort_select');
const results_counter = document.getElementById('results_count');
const search_bar_button = document.getElementById("search-bar-button");
const comments_sort_option = document.getElementById("comments_sort_option");
const slider = document.getElementById('slider');
const sb_button = document.getElementById("search-bar-button");
const viewer_hint = document.getElementById("viewer_hint");
const viewer = document.getElementById('viewer');
const submission_container = document.getElementById('submission_container');
const submission_title = document.getElementById("submission_title");
const submission_body = document.getElementById("submission_body");
const submission_info = document.getElementById("submission_info");
const submission_subredit = submission_info.children[0];
const submission_meta = submission_info.children[1];
const submission_tags = submission_info.children[2];
const submission_image = document.getElementById("submission_image")
const submission_video = document.getElementById("submission_video");
const submission_link = document.getElementById("submission_link");
const factor_description = document.getElementById("factor_description");
const post_upvotes = document.getElementById("post_upvotes");
const post_count = document.getElementById("post_count");
const post_upvotes_title = document.getElementById("post_upvotes_title");
const comment_upvotes = document.getElementById("comment_upvotes");
const comment_count = document.getElementById("comment_count");
const comment_upvotes_title = document.getElementById("comment_upvotes_title");
const upvotes_switch_text = document.getElementById("upvotes_switch_text");
const bot_percent = document.getElementById('bot-likelihood-percentage');

// Variables

var show_karma = true;
var search_pool = posts;
var search_results = search_pool;
var search_target = "posts";
var browser_index = 0;
var browser_step = 10;
var viewed_url = "";

// Filter options
var search_query = ""
var include_body = false
var with_images = false
var spoiler_filter = false
var nsfw_filter = false
var oc_filter = false
var subreddit_filter = "All"

// Sorting
var sort_by = "Date"
var sort_direction = "down"

// Charts

const plot = echarts.init(document.getElementById('plot'));
const gauge = echarts.init(document.getElementById('gauge'));
const gauge2 = echarts.init(document.getElementById('gauge2'));
const pie_chart = echarts.init(document.getElementById('pie_chart'));

const plot_options = {
    tooltip: {
        trigger: 'item',
        backgroundColor: "rgba(20, 20, 20, 0.7)",
        textStyle: {
            color: '#fff',
            fontSize: rem_to_px(0.9)
        },
        formatter: function (params) {
            return `
                <strong>${text_newline(limit_text_width(params.data.title, 100), 30)}</strong><br/>
                Subreddit: r/${params.data.subreddit}<br/>
                Upvotes: ${params.value[1]}<br/>
                ${
                    params.data.is_post
                        ? `Comments: ${params.data.num_comments}<br/>`
                        : ''
                }
                Posted on ${convert_date(params.value[0])}<br/>
            `;
        }
    },
    xAxis: {
        type: 'time',
        axisLine: {
            lineStyle: {
                color: 'rgb(196, 196, 196)'
            }
        },
        axisLabel: {
            color: 'rgb(196, 196, 196)',
            fontSize: rem_to_px(0.9)
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
            color: 'rgb(196, 196, 196)',
            fontSize: rem_to_px(0.9),
            formatter: (value) => {
                const absValue = Math.abs(value);
                if (absValue >= 1_000_000) return (value / 1_000_000) + 'M';
                if (absValue >= 1_000) return (value / 1_000) + 'k';
                return value;
            }
        }
    },
    series: [],
    dataZoom: [
        {
            type: 'inside'
        },
        {
            type: 'slider',
            zoomLock: false,
            xAxisIndex: [0],
            start: 0,
            end: 100,
            height: rem_to_px(2),
            handleStyle: {
                color: 'rgb(255, 255, 255)',
                borderColor: 'rgb(197, 197, 197)',
                borderWidth: 1
            },
            labelFormatter: '',
            textStyle: {
                color: 'rgb(196, 196, 196)'
            },
            handleLabel: {
                show: true
            },
            backgroundColor: 'rgba(0, 0, 0, 0.1)',
            fillerColor: 'rgba(255, 94, 0, 0.13)',
            borderColor: 'rgb(255, 196, 172)'
        }
    ],
    grid: {
        left: 40,
        right: 35,
        top: 10,
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        borderColor: 'rgba(161, 0, 0, 0.8)'
    },
};

const gauge_options = {
    series: [
      {
        type: 'gauge',
        center: ['50%', '100%'],
        radius: '200%',
        startAngle: 180,
        endAngle: 0,
        min: -1,
        max: 1,
        itemStyle: {
          color: '#FFAB91'
        },
        progress: {
          show: true,
          width: rem_to_px(2.5)
        },
        pointer: {
            show: false
        },
        axisLine: {
          lineStyle: {
            width: rem_to_px(2.3)
          }
        },
        axisTick: {
          distance: -45,
          splitNumber: 5,
          lineStyle: {
            width: 2,
            color: '#999'
          }
        },
        splitLine: {
          show: false
        },
        axisLabel: {
          show: false
        },
        axisTick: {
            show: false
        },
        anchor: {
          show: false
        },
        title: {
          show: false
        },
        detail: {
          width: '60%',
          lineHeight: 40,
          borderRadius: 8,
          offsetCenter: [0, '-15%'],
          fontSize: rem_to_px(1.2),
          fontWeight: 'bolder',
          formatter: 'Polarity',
          color: 'inherit'
        },
        data: [
          {
            value: django_data.polarity
          }
        ]
        
      },
      {
        type: 'gauge',
        center: ['50%', '100%'],
        radius: '200%',
        startAngle: 180,
        endAngle: 0,
        min: -1,
        max: 1,
        itemStyle: {
          color: '#ff835c'
        },
        progress: {
          show: true,
          width: rem_to_px(0.5)
        },
        pointer: {
            show: false
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: false
        },
        axisLabel: {
          show: false
        },
        axisTick: {
            show: false
        },
        anchor: {
          show: false
        },
        title: {
          show: false
        },
        data: [
          {
            value: django_data.polarity
          }
        ]
        
      }]
  };

const pie_options = {
    tooltip: {
        trigger: 'item',
        confine: true,
        textStyle: {
            fontSize: rem_to_px(0.9)
        },
    },
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
            data: human_factors.map(item => ({
                ...item,
                itemStyle: {
                  color: '#8ad184'
                }
              })).concat(bot_factors.map(item => ({
                ...item,
                itemStyle: {
                  color: '#ffa8a8'
                }
              })))
        }
    ],
    graphic: [{
        type: 'text',
        left: 'center',
        top: '40%',
        style: {
            text: django_data.bot_likelihood_percentage + '%',
            textAlign: 'center',
            fontSize: rem_to_px(2.5),
            fontWeight: 'bold',
            fill: '#fff'
        }
    }, 
    {
        type: 'text',
        left: 'center',
        top: '55%',
        style: {
            text: (function () {
                let percent = django_data.bot_likelihood_percentage;
                if (percent < 20) {
                    return "Very likely not a bot"
                }
                else if (percent < 50) {
                    return "Likely not a bot"
                }
                else if (percent < 80) {
                    return "Could be a bot"
                }
                else {
                    return "Likely is a bot"
                }
            })(),
            textAlign: 'center',
            fontSize: rem_to_px(0.8),
            fill: '#fff'
        }
    }],
};

// Utility functions

function text_newline (text, max_width) {
    let words = text.split(" ");
    let result = words[0];
    let current_length = result.length;
    
    for (let i = 1; i < words.length; i += 1) {
        current_length += words[i].length;
        if (current_length > max_width) {
            result += '<br>' + words[i]
            current_length = 0;
        }
        else {
            result += " " + words[i]
        }
    }

    return result
}

function limit_text_width (text, max_length) {
    if (text.length > max_length) {
        return text.slice(0, max_length - 3) + '...';
      }
      return text;
}

function convert_date(value) {
    const date = new Date(value)
    return new Intl.DateTimeFormat("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      }).format(date);
}

function clamp(value, min, max) {
    if (value <= 0) {
        return 0
    }
    else {
        return Math.max(Math.min(value, max), min)
    }
}

function rem_to_px(rem) {
    const rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
    return rem * rootFontSize;
  }

// Core functions

function animateNumber(finalNumber, duration = 1000, startNumber = 0, callback) {
    const startTime = performance.now();
    
    function easeOutQuad(t) {
        return 1 - Math.pow(1 - t, 3);
    }
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easeOutQuad(progress);
        const currentNumber = Math.floor(easedProgress * (finalNumber - startNumber) + startNumber);
      
        callback(currentNumber);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    requestAnimationFrame(update);
}

function set_analysis_date() {
    if (django_data.analysis_date == "just now") {
        analysis_date.innerHTML = '<b>just now</b>';
    }
    else {
        const utc_date = new Date(django_data.analysis_date);

        const local_date = utc_date.toLocaleString(undefined, {
            year: "numeric", month: "long", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false
        }).split(' at ');
    
        const date = local_date[0];
        const time = local_date[1];
    
        analysis_date.innerHTML = '<b>' + date + '</b>, ' + time;
    }
}

function toggle_upvotes() {
    show_karma = !show_karma;

    if (show_karma) {
        post_upvotes_title.textContent = "Post karma";
        comment_upvotes_title.textContent = "Comment karma";
        animateNumber(django_data.post_karma, 300, django_data.post_upvotes, (n) => {
            post_upvotes.textContent = n;
        });
        animateNumber(django_data.comment_karma, 300, django_data.comment_upvotes, (n) => {
            comment_upvotes.textContent = n;
        });
        upvotes_switch_text.textContent = "Click to switch to sum of upvotes";
    }
    else {
        post_upvotes_title.textContent = "Post upvotes";
        comment_upvotes_title.textContent = "Comment upvotes";
        animateNumber(django_data.post_upvotes, 300, django_data.post_karma, (n) => {
            post_upvotes.textContent = n;
        });
        animateNumber(django_data.comment_upvotes, 300, django_data.comment_karma, (n) => {
            comment_upvotes.textContent = n;
        });
        upvotes_switch_text.textContent = "Click to switch to karma";
    }
}

function fill_statistics(criteria) {
    const max_post_frequency = 2;
    const max_comment_frequency = 4;
    const max_upvotes_post = 3000;
    const max_comments = 300;
    const max_own_comments = comments.length;
    const max_upvotes_comment = 500;
    const max_ratio = 1;
    const max_post_length = 500;
    const max_comment_length = 500;

    if (criteria == "Posts + comments") {
        document.getElementById("posting-frequency-title").innerHTML = "Activity frequency: <span class='orange bold'>" + django_data.total_frequency + "</span> per day";
        document.getElementById("average-upvotes-title").innerHTML = "Average upvotes per submission: <span class='orange bold'>" + django_data.overall_upvotes + "</span>";
        document.getElementById("average-comments-title").innerHTML = "Average submission length: <span class='orange bold'>" + django_data.avg_submission_length + "</span> chars";
        document.getElementById("upvotes-ratio-title").innerHTML = "Upvotes to downvotes ratio: <span class='orange bold'>" + django_data.avg_post_ratio + "</span>";

        document.getElementById("posting-frequency").style.width = clamp(django_data.total_frequency / max_post_frequency * 100, 4, 100) + "%";
        document.getElementById("average-upvotes").style.width = clamp(django_data.overall_upvotes / max_upvotes_post * 100, 4, 100) + "%";
        document.getElementById("average-comments").style.width = clamp(django_data.avg_submission_length / max_post_length * 100, 4, 100) + "%";
        document.getElementById("upvotes-ratio").style.width = clamp(django_data.avg_post_ratio / max_ratio * 100, 4, 100) + "%";
    }
    if (criteria == "Posts") {
        document.getElementById("posting-frequency-title").innerHTML = "Posting frequency: <span class='orange bold'>" + django_data.posting_frequency + "</span> per day";
        document.getElementById("average-upvotes-title").innerHTML = "Average upvotes per post: <span class='orange bold'>" + django_data.up + "</span>";
        document.getElementById("average-comments-title").innerHTML = "Average post length: <span class='orange bold'>" + django_data.avg_post_length + "</span> chars";
        document.getElementById("upvotes-ratio-title").innerHTML = "Average comments per post: <span class='orange bold'>" + django_data.comments_under_post_amount + "</span>";

        document.getElementById("posting-frequency").style.width = clamp(django_data.posting_frequency / max_post_frequency * 100, 4, 100) + "%";
        document.getElementById("average-upvotes").style.width = clamp(django_data.up / max_upvotes_post * 100, 4, 100) + "%";
        document.getElementById("average-comments").style.width = clamp(django_data.avg_post_length / max_post_length * 100, 4, 100) + "%";
        document.getElementById("upvotes-ratio").style.width = clamp(django_data.comments_under_post_amount / max_comments * 100, 4, 100) + "%";
    }
    if (criteria == "Comments") {
        document.getElementById("posting-frequency-title").innerHTML = "Commenting frequency: <span class='orange bold'>" + django_data.comment_frequency + "</span> per day";
        document.getElementById("average-upvotes-title").innerHTML = "Average upvotes per comment: <span class='orange bold'>" + django_data.up_comment + "</span>";
        document.getElementById("average-comments-title").innerHTML = "Average comment length: <span class='orange bold'>" + django_data.avg_comment_length + "</span> chars";
        document.getElementById("upvotes-ratio-title").innerHTML = "User's comments under own posts: <span class='orange bold'>" + django_data.own_comments + "</span>";

        document.getElementById("posting-frequency").style.width = clamp(django_data.comment_frequency / max_comment_frequency * 100, 4, 100) + "%";
        document.getElementById("average-upvotes").style.width = clamp(django_data.up_comment / max_upvotes_comment * 100, 4, 100) + "%";
        document.getElementById("average-comments").style.width = clamp(django_data.avg_comment_length / max_comment_length * 100, 4, 100) + "%";
        document.getElementById("upvotes-ratio").style.width = clamp(django_data.own_comments / max_own_comments * 100, 4, 100) + "%";
    }
}

function fill_subreddits_table(sort_criteria) {
    const table = document.getElementById('subreddits-body')
    function clear_criterias() {
        document.getElementById('subreddits-head').children[0].textContent = "Name"
        document.getElementById('subreddits-head').children[1].textContent = "Posts"
        document.getElementById('subreddits-head').children[2].textContent = "Comments"
        document.getElementById('subreddits-head').children[3].textContent = "Upvotes"
    }
    table.replaceChildren();

    if (sort_criteria == "name") {
        subreddits.sort((a, b) => a.name.localeCompare(b.name));
        clear_criterias();
        document.getElementById('subreddits-head').children[0].innerHTML = "Name&nbsp;↓"
    }
    else if (sort_criteria == "posts") {
        subreddits.sort((a, b) => b.posts - a.posts);
        clear_criterias();
        document.getElementById('subreddits-head').children[1].innerHTML = "Posts&nbsp;↓"
    }
    else if (sort_criteria == "comments") {
        subreddits.sort((a, b) => b.comments - a.comments);
        clear_criterias();
        document.getElementById('subreddits-head').children[2].innerHTML = "Comments&nbsp;↓"
    }
    else if (sort_criteria == "upvotes") {
        subreddits.sort((a, b) => b.upvotes - a.upvotes);
        clear_criterias();
        document.getElementById('subreddits-head').children[3].innerHTML = "Upvotes&nbsp;↓"
    }
    for (let i = 0; i < subreddits.length; i += 1) {
        var sub = document.createElement('tr')
        sub.innerHTML = `
            <td class="subreddit-cell subreddit-cell-name">${subreddits[i].name}</td>
            <td class="subreddit-cell number">${subreddits[i].posts}</td>
            <td class="subreddit-cell number">${subreddits[i].comments}</td>
            <td class="subreddit-cell orange number">${subreddits[i].upvotes}</td>
        `;
        sub.className = "subreddit";
        sub.onclick = () => view_subreddit(subreddits[i].name);
        table.appendChild(sub)
    }
}

function view_subreddit(name) {
    subreddit_filter = name.slice(2);
    filter_submissions();
    sort_submissions();
    reset_browser();
    scroll_to_submissions();
    subreddit_select.value = name;
}

function view_word(word) {
    search_query = word;
    include_body = false;
    toggle_body_search();
    if (search_target != "everything") {
        switch_to_everything();
    }
    filter_submissions();
    sort_submissions();
    reset_browser();
    scroll_to_submissions();
    search_bar.value = word;
}

function filter_submissions() {
    search_results = []
    for (let i = 0; i < search_pool.length; i += 1) {
        const submission = search_pool[i];

        if (subreddit_filter != "All") {
            if (submission.subreddit != subreddit_filter) {
                continue;
            }
        }

        if (submission.hasOwnProperty("title")) {
            if (with_images) {
                if (!submission.url.startsWith("https://i.redd.it") && !submission.url.startsWith("https://v.redd.it")) {
                    continue;
                }
            }
            if (spoiler_filter) {
                if (!submission.spoiler) {
                    continue;
                }
            }
            if (nsfw_filter) {
                if (!submission.over_18) {
                    continue;
                }
            }
            if (oc_filter) {
                if (!submission.oc) {
                    continue;
                }
            }

            if (include_body) {
                if (!submission.title.toLowerCase().includes(search_query) && !submission.body.toLowerCase().includes(search_query)) {
                    continue;
                }
            }
            else {
                if (!submission.title.toLowerCase().includes(search_query)) {
                    continue;
                }
            }
        }
        else {
            if (!submission.body.toLowerCase().includes(search_query)) {
                continue;
            }
        }

        search_results.push(submission);
    }

    update_plot();
    set_datazoom(0, 100);

    if (search_results.length == 1) {
        results_counter.textContent = "1 result"
    }
    else {
        results_counter.textContent = search_results.length + " results";
    }
}

function change_sort_direction(button) {
    if (sort_direction == "up") {
        sort_direction = "down";
        button.textContent = "▼"
    }
    else if (sort_direction == "down") {
        sort_direction = "up";
        button.textContent = "▲"
    }
    sort_submissions();
    reset_browser();
}

function sort_submissions() {
    if (sort_by == "Date") {
        if (sort_direction == "down") {
            search_results.sort((a, b) => new Date(b.created_date) - new Date(a.created_date));
        }
        else {
            search_results.sort((a, b) => new Date(a.created_date) - new Date(b.created_date));
        }
    }
    if (sort_by == "Upvotes") {
        if (sort_direction == "down") {
            search_results.sort((a, b) => b.score - a.score);
        }
        else {
            search_results.sort((a, b) => a.score - b.score);
        }
    }
    if (sort_by == "Comments") {
        if (sort_direction == "down") {
            search_results.sort((a, b) => b.num_comments - a.num_comments);
        }
        else {
            search_results.sort((a, b) => a.num_comments - b.num_comments);
        }
    }
}

function toggle_body_search() {
    if (search_target != "comments") {
        include_body = !include_body

        if (include_body) {
            search_bar_button.style.filter = "brightness(0) saturate(100%) invert(60%) sepia(93%) saturate(3248%) hue-rotate(1deg) brightness(107%) contrast(106%)";
            if (search_target == "posts") {
                search_bar.placeholder = "Search titles and body...";
            }
        }
        else {
            search_bar_button.style.filter = "";
            if (search_target == "posts") {
                search_bar.placeholder = "Search titles...";
            }
        }
        filter_submissions();
        sort_submissions();
        reset_browser();   
    }
}

function reset_browser() {
    browser.replaceChildren();
    browser.scrollTop = 0;

    browser_index = 0;
    fill_browser();
}

function fill_browser() {
    for (let i = browser_index; i < browser_index + browser_step && i < search_results.length; i += 1) {
        const component = document.createElement('div');
        const submission = search_results[i];

        component.onclick = function () {
            view_submission(submission)
        }

        const submissionContent = document.createElement('div');

        const meta = document.createElement('div');
        meta.className = 'subtext';

        const title = document.createElement('div');

        if (submission.hasOwnProperty("title")) {
            meta.textContent = 'r/' + submission.subreddit + ' • ' + convert_date(submission.created_date);

            component.className = 'browser-post';

            title.className = 'bold';
            title.textContent = limit_text_width(submission.title, 100);

            const stats = document.createElement('div');
            stats.className = 'subtext';

            const upvotes = document.createElement('span');
            upvotes.textContent = submission.score;
            if (submission.score == 1) {
                upvotes.textContent += ' upvote';
            }
            else {
                upvotes.textContent += ' upvotes';
            }

            stats.appendChild(upvotes);

            const separator = document.createTextNode(' • ');

            const comments = document.createElement('span');
            comments.textContent = submission.num_comments;
            if (submission.num_comments == 1) {
                comments.textContent += ' comment';
            }
            else {
                comments.textContent += ' comments';
            }

            stats.appendChild(separator);
            stats.appendChild(comments);

            submissionContent.appendChild(meta);
            submissionContent.appendChild(title);
            submissionContent.appendChild(stats);
        }
        else {
            meta.textContent = 'r/' + submission.subreddit + ' • ' + convert_date(submission.created_date) + ' • ' + submission.score;
            if (submission.score == 1) {
                meta.textContent += ' upvote';
            }
            else {
                meta.textContent += ' upvotes';
            }

            component.className = 'browser-comment';

            // title.className = 'browser-comment-text';
            title.textContent = limit_text_width(submission.body, 300);

            submissionContent.appendChild(meta);
            submissionContent.appendChild(title);
        }



        component.appendChild(submissionContent);

        browser.appendChild(component);
    }

    browser_index += browser_step;
}

function view_submission(submission) {
    if (search_target != "everything") {
        const series = plot.getOption().series[0];
        const max = new Date(series.data[0].value[0]).getTime();
        const min = new Date(series.data[series.data.length - 1].value[0]).getTime();

        const value = new Date(submission.created_date).getTime();

        const point = ((value - min) / (max - min)) * 100

        // const dataZoom = plot.getOption().dataZoom[1];
        // const zoom_length = dataZoom.end - dataZoom.start

        set_datazoom(point - 15, point + 15)
    }

    viewer_hint.style.display = "none";
    submission_image.style.display = "none";
    submission_video.style.display = "none";
    submission_link.style.display = "none";
    submission_container.style.display = "flex";

    submission_tags.textContent = "";

    if (submission.hasOwnProperty("title")) {
        submission_title.firstChild.textContent = submission.title;

        if (submission.url != submission.permalink) {
            if (submission.url.startsWith("https://i.redd.it")) {
                submission_image.style.display = "block";
                submission_image.src = submission.url;
            }
            else if (submission.url.startsWith("https://v.redd.it")) {
                submission_video.style.display = "block";
                submission_video.src = submission.url + "/DASH_360.mp4";
            }
            else {
                submission_link.style.display = "flex";
                submission_link.onclick = function () {
                    window.open(submission.url, '_blank');
                }
                submission_link.title = submission.url;
            }
        }
        if (submission.body == "") {
            submission_body.textContent = "This post has no body text.";
        }
        else {
            submission_body.innerHTML = submission.html;
        }
    }
    else {
        submission_title.firstChild.textContent = "View comment";
        submission_body.innerHTML = submission.html;
    }
    submission_subredit.textContent = 'r/' + submission.subreddit;
    submission_subredit.href = "https://www.reddit.com/r/" + submission.subreddit;
    submission_meta.textContent = ' • ' + convert_date(submission.created_date) + ' • ' + submission.score + ' upvotes';

    if (submission.hasOwnProperty("title")) {
        submission_meta.textContent += ' • ' + submission.num_comments + ' comments'

        if (submission.spoiler || submission.over_18 || submission.oc) {
            submission_tags.textContent += ' |'
            if (submission.spoiler) {
                submission_tags.textContent += ' SPOILER'
            }
            if (submission.over_18) {
                submission_tags.textContent += ' NSFW'
            }
            if (submission.oc) {
                submission_tags.textContent += ' OC'
            }
        }
    }

    viewed_url = submission.permalink;
}

function open_submission_link() {
    window.open(viewed_url, '_blank');
}

function set_datazoom(start, end) {
    plot.dispatchAction({
        type: 'dataZoom',
        start: start,
        end: end
      });
}

function update_plot() {
    plot.setOption({
        series: [{
            data: search_results.map(item => {
                const has_title = item.hasOwnProperty('title');

                return {
                    value: [item.created_date, item.score],
                    submission: item,
                    title: has_title ? item.title : item.body,
                    subreddit: item.subreddit,
                    body: item.body,
                    permalink: item.permalink,
                    num_comments: item.num_comments,
                    is_post: has_title
                }
              }),
            type: 'scatter',
            symbolSize: rem_to_px(0.7),
            itemStyle: {
                color: function(params) {
                    return params.data.is_post ? 'rgb(255, 102, 0)' : 'rgb(185, 227, 255)';
                }
            }
        }]
    });
}

function block_post_filters() {
    document.querySelectorAll('.posts-only').forEach(el => {
        el.disabled = true;
        el.parentElement.classList.add('gray');
    });
    comments_sort_option.style.display = "none";
    if (sort_by == "Comments") {
        sort_by = "Date";
        sort_select.value = "Date";
    }
}

function switch_to_posts() {
    document.querySelectorAll('.switch-option').forEach(opt => {
        opt.classList.remove('active');
        opt.style.color = "white";
        posts_switch.style.fontWeight = "normal"
    });
    posts_switch.classList.add('active');

    slider.style.transform = `translateX(0%)`;
    posts_switch.style.color = "orange";

    document.querySelectorAll('.posts-only').forEach(el => {
        el.disabled = false;
        el.parentElement.classList.remove('gray');
    });
    comments_sort_option.style.display = "block";
    
    sb_button.parentElement.className = "search-bar-button"
    if (search_target == "comments") {
        sb_button.style.filter = ""
    }
    if (include_body) {
        search_bar.placeholder = "Search titles and body...";
    }
    else {
        search_bar.placeholder = "Search titles...";
    }
    submission_container.style.display = "none";
    viewer_hint.style.display = "block";
    viewer_hint.textContent = "Select a post to view it here";

    search_target = "posts"
    search_pool = posts;
    filter_submissions();
    sort_submissions();
    reset_browser();
}

function switch_to_comments() {
    document.querySelectorAll('.switch-option').forEach(opt => {
        opt.classList.remove('active');
        opt.style.color = "white";
        comments_switch.style.fontWeight = "normal"
    });
    comments_switch.classList.add('active');

    slider.style.transform = `translateX(100%)`;
    comments_switch.style.color = "lightblue";

    block_post_filters();

    include_body = true;
    toggle_body_search();
    sb_button.parentElement.className = "search-bar-button-deactivated"
    sb_button.style.filter = "brightness(60%)"

    search_bar.placeholder = "Search comments...";

    submission_container.style.display = "none";
    viewer_hint.style.display = "block";
    viewer_hint.textContent = "Select a comment to view it here"

    search_target = "comments"
    search_pool = comments;
    filter_submissions();
    sort_submissions();
    reset_browser();
}

function switch_to_everything() {
    document.querySelectorAll('.switch-option').forEach(opt => {
        opt.classList.remove('active');
        opt.style.color = "white";
        everything_switch.style.fontWeight = "normal"
    });
    everything_switch.classList.add('active');

    slider.style.transform = `translateX(200%)`;
    everything_switch.style.color = "lightgreen";

    block_post_filters();

    sb_button.parentElement.className = "search-bar-button"
    if (search_target == "comments") {
        sb_button.style.filter = ""
    }

    search_bar.placeholder = "Search everything...";

    submission_container.style.display = "none";
    viewer_hint.style.display = "block";
    viewer_hint.textContent = "Select a post or a comment to view it here"

    search_target = "everything"
    search_pool = posts_and_comments;
    filter_submissions();
    sort_submissions();
    reset_browser();
}

function scroll_to_analysis() {
    analysis_section.scrollIntoView({ behavior: 'smooth' });
}

function scroll_to_monitor() {
    monitor_section.scrollIntoView({ behavior: 'smooth' });
}

function scroll_to_submissions() {
    submissions.scrollIntoView({ behavior: 'smooth' });
}

function change_factor_description(message) {
    factor_description.textContent = message;
}

// Event listeners

window.addEventListener('resize', () => {
    plot.resize();
    pie_chart.resize();
});

statistics_select.addEventListener('change', () => {
    fill_statistics(statistics_select.value);
});

plot.on('click', function (params) {
    view_submission(params.data.submission);
});

search_bar.addEventListener('input', () => {
    search_query = search_bar.value.toLowerCase();
    filter_submissions();
    sort_submissions();
    reset_browser();
});

image_checkbox.addEventListener('change', () => {
    with_images = image_checkbox.checked;
    filter_submissions();
    sort_submissions();
    reset_browser();
});

spoiler_checkbox.addEventListener('change', () => {
    spoiler_filter = spoiler_checkbox.checked;
    filter_submissions();
    sort_submissions();
    reset_browser();
});

nsfw_checkbox.addEventListener('change', () => {
    nsfw_filter = nsfw_checkbox.checked;
    filter_submissions();
    sort_submissions();
    reset_browser();
});

oc_checkbox.addEventListener('change', () => {
    oc_filter = oc_checkbox.checked;
    filter_submissions();
    sort_submissions();
    reset_browser();
});

subreddit_select.addEventListener('change', () => {
    if (subreddit_select.value == "All") {
        subreddit_filter = "All";
    }
    else {
        subreddit_filter = subreddit_select.value.slice(2);
    }
    filter_submissions();
    sort_submissions();
    reset_browser();
});

sort_select.addEventListener('change', () => {
    sort_by = sort_select.value;
    sort_submissions();
    reset_browser();
});

browser.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = browser;
  
    if (scrollTop + clientHeight >= scrollHeight - 10 && browser_index < search_results.length) {
        fill_browser();
    }
});

document.querySelectorAll('.factor').forEach(factor => {
    const itemName = factor.textContent.trim();
    
    factor.addEventListener('mouseenter', function () {
        pie_chart.dispatchAction({
            type: 'select',
            name: itemName
        });

        pie_chart.dispatchAction({
            type: 'showTip',
            seriesIndex: 0,
            dataIndex: pie_chart.getOption().series[0].data.findIndex(item => item.name === itemName)
        });
    });
    
    factor.addEventListener('mouseleave', function () {
        pie_chart.dispatchAction({
            type: 'unselect',
            name: itemName
        });

        pie_chart.dispatchAction({
            type: 'hideTip'
        });
    });
});

trophies_button.addEventListener('click', (e) => {
    e.stopPropagation();
    trophies_popup.classList.toggle('active');
});

trophies_popup.addEventListener('click', (e) => {
    if (e.target === trophies_popup) {
        trophies_popup.classList.remove('active');
    }
});

// On load

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('form').forEach(form => form.reset());

    set_analysis_date();

    plot.setOption(plot_options);
    update_plot();
    gauge.setOption(gauge_options);
    gauge2.setOption(gauge_options);
    gauge2.setOption({
        series: [{
            data: [{
                value: django_data.subjectivity
        }],
        detail: {
            formatter: 'Subjectivity',
        },
        itemStyle: {
            color: 'rgb(184, 182, 253)'
        }
        }, 
        {
            data: [{
                value: django_data.subjectivity
            }],
            itemStyle: {
                color: 'rgb(149, 146, 255)'
            },
        }]
    })
    pie_chart.setOption(pie_options);

    fill_subreddits_table("upvotes")
    reset_browser();
    plot.resize();

    fill_statistics("Posts");

    const percentage = django_data.bot_likelihood_percentage;
    if (percentage <= 25) {
        const r = Math.floor((255 * percentage) / 25);
        const g = 255;
        const b = 0;
        bot_percent.style.color = `rgb(${r},${g},${b})`;
    } else {
        const r = 255;
        const g = Math.floor(255 * (75 - percentage) / 50);
        const b = 0;
        bot_percent.style.color = `rgb(${r},${g},${b})`;
    }

    animateNumber(django_data.post_karma, 1000, 0, (n) => {
        post_upvotes.textContent = n;
    });
    animateNumber(django_data.comment_karma, 1000, 0, (n) => {
        comment_upvotes.textContent = n;
    });
    animateNumber(django_data.posts.length, 1000, 0, (n) => {
        post_count.textContent = n;
    });
    animateNumber(django_data.comments.length, 1000, 0, (n) => {
        comment_count.textContent = n;
    });
    animateNumber(django_data.trophies.length, 1000, 0, (n) => {
        trophies_count.textContent = n;
    });
})
