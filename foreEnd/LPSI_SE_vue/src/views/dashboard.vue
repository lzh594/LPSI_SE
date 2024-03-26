<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="10">
                <el-card shadow="hover" class="mgb20" style="height: 360px">
                    <div class="user-info">
                        <div class="user-info-icon">
                            <el-avatar v-if="identity==='1'" class="user-avator" :size="120" :src="userImg" style="background-color: white"/>
                            <el-avatar v-else class="user-avator" :size="120" :src="orgImg"/>
                        </div>
                        <div class="user-info-cont">
                            <div class="user-info-name" style="margin-bottom: 20px; font-size: 50px">{{ username }}</div>
                            <div style="font-size: 40px">{{ role }}</div>
                        </div>
                    </div>
                    <div class="user-info-list">
                        <span style="margin-right: 30px; font-size: 25px">日期：{{ currentTime }}</span>
                        <span style="margin-left: 30px; font-size: 25px">ip属地：{{ currentLocation }}</span>
                    </div>
                    <div class="user-welcome" style="font-size: 40px">
                        欢迎使用S.Encryption
                    </div>
                </el-card>
                <el-row :gutter="20" class="mgb20">
                    <el-col :span="12" style="height: 180px">
                        <el-card shadow="hover">
                            <div class="grid-content grid-con-1">
                                <el-icon class="grid-con-icon">
                                    <User/>
                                </el-icon>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ visitsTotal }}</div>
                                    <div class="message">访问量</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="12">
                        <el-card shadow="hover">
                            <div class="grid-content grid-con-2">
                                <el-icon class="grid-con-icon">
                                    <Message/>
                                </el-icon>
                                <div class="grid-cont-right">
                                    <div class="grid-num">21</div>
                                    <div class="message">系统消息</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="12">
                        <el-card shadow="hover">
                            <div class="grid-content grid-con-3">
                                <el-icon class="grid-con-icon">
                                    <Monitor/>
                                </el-icon>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ dbNums }}</div>
                                    <div class="message">数据库量</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="12">
                        <el-card shadow="hover">
                            <div class="grid-content grid-con-4">
                                <el-icon class="grid-con-icon">
                                    <Coin/>
                                </el-icon>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ serachTotal }}</div>
                                    <div class="message">搜索次数</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </el-col>
            <el-col :span="14">
                <el-card shadow="hover" style="height: 741px">
                    <div id="chart" style="height: 680px"></div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts" name="dashboard">
import {ref, onMounted} from 'vue';
import {Coin, Message, Monitor} from "@element-plus/icons-vue";
import userImg from "../assets/img/user.jpg";
import orgImg from "../assets/img/org.jpg";
import axios from "axios";
import * as echarts from 'echarts';

const identity = localStorage.getItem('ms_identity');
const username = localStorage.getItem('ms_username');
const role: string = '用户';

const visitsTotal = localStorage.getItem('visits') || "0"
const dbNums = localStorage.getItem('dbNums') || "0"
const serachTotal = localStorage.getItem('serachTotal') || "0"
const currentTime = ref('');
const currentLocation = ref('');


onMounted(async () => {
    // 获取当前时间
    const date = new Date();
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // 月份从0开始，所以需要+1
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear();
    currentTime.value = `${year}-${month}-${day}`;

    // 获取当前地理位置
    // 支持async/await用法
    const response = await axios.get('https://restapi.amap.com/v3/ip', {
        params: {
            output: "json",
            key: "1481cee1325f2cd0eab19ba643d87ba8"
        }
    });
    currentLocation.value = `${response.data.province} ${response.data.city}`;

    // 基于准备好的dom，初始化echarts实例
    const myChart = echarts.init(document.getElementById('chart'));
// 绘制图表
    myChart.setOption({
        title: {
            text: '实时搜索数据——最近1小时',
            left: 'center',
            textStyle: {
                fontSize: 30
            }
        },
        legend: {
            orient: 'horizontal',
            top: 'bottom',
            textStyle: {
                fontSize: 20
            }
        },
        xAxis: {
            data: ["60分前", "50分前", "40分前", "30分前", "20分前", "10分前"],
            axisLabel: {
                fontSize: 16
            }
        },
        yAxis: [
            {
                type: 'value',
                name: '访问量',
                min: 0,
                max: 200,
                position: 'right',
                axisLabel: {
                    formatter: '{value} 人次',
                    fontSize: 16
                },
            },
            {
                type: 'value',
                name: '搜索次数',
                min: 0,
                max: 30,
                position: 'left',
                axisLabel: {
                    formatter: '{value} 次',
                    fontSize: 16
                }
            }
        ],
        series: [
            {
                name: '系统访问量',
                type: 'bar',
                data: [20, 34, 36, 38, 47, 28],
                label: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        fontSize: 18
                    }
                },
                barWidth: '50%',
                itemStyle: {
                    color: '#ea7e53',
                    shadowColor: '#91cc75',
                    borderType: 'dashed',
                    opacity: 0.5,
                },
                smooth: true,
                yAxisIndex: 0
            },
            {
                name: '数据上传次数',
                type: 'line',
                data: [5, 12, 16, 18, 14, 7],

                smooth: true,
                yAxisIndex: 1
            },
            {
                name: '加密搜索次数',
                type: 'line',
                data: [10, 2, 4, 6, 9, 3],

                smooth: true,
                yAxisIndex: 1
            }, {
                name: '结果分析次数',
                type: 'line',
                data: [5, 20, 16, 11, 24, 18],
                smooth: true,
                yAxisIndex: 1
            },

        ]
    });
});

</script>

<style scoped>

.user-info {
    display: flex;
    align-items: center;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-info-icon {
    padding: 20px;
}

.user-info-cont {
    flex: 1;
    font-size: 34px;
    color: #999;
    font-weight: bold;
    text-align: center;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
    font-weight: bold;
    text-align: center;
}

.user-info-cont div:last-child {
    font-size: 25px;
    color: #999;
    text-align: center;
}

.user-info-list {
    margin-top: 40px;
    font-size: 18px;
    font-weight: bold;
    color: #999;
    line-height: 30px;
    text-align: center;
}


.user-welcome {
    margin-top: 20px;
    font-size:32px;
    font-weight: bold;
    color: black;
    text-align: center;
    font-family: "楷体", serif;

}

.mgb20 {
    margin-bottom: 60px;
}

.function {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
}

.intro {
    font-size: 24px;
    line-height: 80px;
    font-family: 宋体, serif;
}

.intro_p {
    font-size: 30px;
    padding-top: 30px;
    padding-left: 10px;
    text-indent: 2em;
}

.character {
    font-size: 24px;
    line-height: 100px;
    color: rgba(0, 0, 0, 0.7);
    font-family: 方正小标宋简体, serif;
}

.chara1 {
    font-size: 24px;
    line-height: 100px;
    color: chocolate;
    font-family: 楷体, serif;
}

.chara2 {
    font-size: 24px;
    line-height: 100px;
    color: blueviolet;
    font-family: 楷体, serif;
}

.chara3 {
    font-size: 24px;
    line-height: 100px;
    color: indigo;
    font-family: 楷体, serif;
}

.advertise {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    font-family: "华文行楷", serif;
    color: olivedrab;
}

.grid-content {
    display: flex;
    align-items: center;
    height: 100px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
    margin-left: 10px;
}

.grid-num {
    font-size: 35px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(100, 213, 114);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.grid-con-4 .grid-con-icon {
    background: rgb(250, 200, 25);
}

.grid-con-4 .grid-num {
    color: rgb(250, 200, 25);
}

.message {
    font-size: 29px;
}
</style>