let radarChart = echarts.init(document.getElementById('radarChart'), 'dark');
var scoreHistory = [[0,0,0,0,0,0]];
let indexList = [0,0,0,0,0,0]
function updateRadarPlot() {
    let seriesRadarData = [];
    // Create a separate series for each historical score
    for (let i = 0; i < scoreHistory.length; i++) {
        let colorList = [
            'rgba(255, 255, 0, 0.0)',  // 黄色，透明度0.1
            'rgba(255, 255, 0, 0.1)',  // 浅黄色，透明度0.3
            'rgba(255, 255, 0, 0.2)',  // 橙黄色，透明度0.4
            'rgba(255, 223, 0, 0.3)',  // 橙色，透明度0.5
            'rgba(255, 191, 0, 0.4)',  // 深橙色，透明度0.6
            'rgba(255, 159, 0, 0.5)',   // 红橙色，透明度0.7
            'rgba(255, 128, 0, 0.6)',   // 橙红色，透明度0.8
            'rgba(255, 96, 0, 0.7)',   // 浅红色，透明度0.9
            'rgba(255, 32, 0, 0.8)',   // 红色，透明度0.95
            'rgba(255, 0, 0, 0.9)'       // 红色，透明度1
        ];
        seriesRadarData.push({
            type: 'radar',
            symbol: 'none',
            lineStyle: {
            width: 1,
            color: colorList[Math.floor(i/scoreHistory.length*colorList.length)]
            },
            emphasis: {
            areaStyle: {
                color: 'rgba(0,250,0,0.3)'
            }
            },
            data: [
                {
                value: scoreHistory[i],
                name: 'Step_ ' + (i + 1)
                }
            ]
        });
    }

    let radarOption = {
        title: {
            text: 'Performance',
            // top: '82%',
            // left: 'center',
            textStyle: {
                color: '#ffffff'
            }
        },
        tooltip: {
            trigger: 'item',
        },
        radar: {
            name: {
                textStyle: {
                    fontSize: 10,
                }
            },
            indicator: [
                { name: 'AESTHETICS', max: 100 },
                { name: 'AFFORD\nABILITY', max: 100 },
                { name: 'TAX\nREVENUE', max: 100 },
                { name: 'PROFIT', max: 100 },
                { name: 'SVF', max: 100 },
                { name: 'SHAPE', max: 100 },
            ]
        },
        series: seriesRadarData,
        graphic: [
            {
                type: 'text',
                left: 'center',
                top: '95%', // Adjust the top value to position the total score
                style: {
                    text: 'Total Score: ' + calculateTotalScore(),
                    fill: '#ffffff',
                    fontSize: 14
                }
            }
        ]
    };
    if (radarOption && typeof radarOption === 'object') {
        radarChart.setOption(radarOption);
    };
}

function calculateTotalScore() {
    if (scoreHistory.length == 0) {
        return 0;
    }
    return Math.floor(scoreHistory[scoreHistory.length-1].reduce((total, score) => total + score, 0));
    };
    

// ECharts 柱状图
let barChart = echarts.init(document.getElementById('barChart'), 'dark');
function updateBarChart() {
    let barOption = {
        title: {
            text: 'Urban Form Indexes'
        },
        // backgroundColor: 'rgba(50, 50, 100, 0.5)',
        tooltip: {},
        xAxis: {
            data: ["BCR","FAR","OSR","Max_l","O_ratio","F_ratio"],
            axisLabel: {
                rotate: 45 // or any other angle
            }
        },
        yAxis: {},
        series: [{
            name: 'Index',
            type: 'bar',
            data: indexList,
        }]
    };
    barChart.setOption(barOption);
}

window.addEventListener( 'resize', onWindowResize );
function onWindowResize() {
    radarChart.resize();
    barChart.resize();
}

updateRadarPlot();
updateBarChart();