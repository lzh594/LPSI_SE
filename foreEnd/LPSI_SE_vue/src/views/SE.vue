<template>
    <div>
        <el-row :gutter="20" justify="center">
            <el-col :span="12">
                <el-card shadow="hover" style="height: 830px">
                    <div class="input-num">
                        <el-button-group>
                            <el-button :icon="Plus" round style="height: 60px;width: 130px;font-size: 25px"
                                       type="primary" @click="addSearch">
                                增添
                            </el-button>
                            <el-button round style="height: 60px;width: 130px;font-size: 25px" type="danger"
                                       @click="searchQuery.Keywords=[{key: 0,value: ''},]">重置
                                <span class="icon">
                                    <el-icon>
                                        <Refresh/>
                                    </el-icon>
                                </span>
                            </el-button>
                        </el-button-group>
                    </div>
                    <el-form ref="formRef"
                             :label-position="'left'"
                             label-width="120px"
                             size="large"
                             style="margin-left: 50px"
                             :model="searchQuery">
                        <el-form-item v-for="(Keyword,index) in searchQuery.Keywords"
                                      :label="'关键词' + (index+1)"
                                      :key="Keyword.key"
                                      :prop="'Keywords.' + index + '.value'"
                                      style="margin-top: 30px"
                                      :rules="rules[0]" class="el-form-item__label">
                            <el-input v-model="Keyword.value"
                                      :prefix-icon="Search"
                                      clearable
                                      @clear="Keyword.value=''"
                                      class="handle-input">
                            </el-input>
                            <el-button class="mt-2" @click.prevent="delSearch(Keyword)"
                            >Delete
                            </el-button
                            >
                        </el-form-item>
                    </el-form>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card shadow="hover" style="height: 40%">
                    <el-form
                        ref="formRef"
                        :rules="rules"
                        :model="searchQuery"
                        :label-position="'left'"
                        label-width="150px"
                        size="large"
                        style="margin-left: 10px;text-align: center">
                        <div class="large1">
                            <el-form-item label="数据库">
                                <el-select v-model="searchQuery.QueryDB" placeholder="请选择你查询的数据库"
                                           size="large" style="width: 500px">
                                    <el-option v-for="item in dbOptions"
                                               :key="item.value"
                                               :label="item.label"
                                               :value="item.value"/>
                                </el-select>
                            </el-form-item>
                        </div>
                        <div class="large2">
                            <el-form-item label="查询模式">
                                <el-select v-model="searchQuery.QueryMode" placeholder="请选择你的查询模式" size="large" style="width: 500px">
                                    <el-option label="析取查询" value="disjunctive"/>
                                    <el-option label="联合查询" value="conjunctive"/>
                                </el-select>
                            </el-form-item>
                        </div>
                        <div class="large3">

                        </div>
                    </el-form>
                    <div style="margin: 20px auto;text-align: center">
                        <el-button type="success" :icon="Search" size="large"
                                   style="font-size: 30px;height: 65px;width: 220px; margin-top: 15px"
                                   @click="onSubmit(formRef);">可搜索加密
                        </el-button>
                    </div>
                </el-card>
                <el-card shadow="hover" style="margin-top: 10px; height: 57.15%">
                    <div class="block text-center" style="height: 460px">
                        <div id="chart" style="height: 100%"></div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <el-dialog
            v-model="dialogVisible"
            style="font-size: 28px"
            width="60%"
            center
            :before-close="handleClose"
        >
            <template #header="{ close, titleId, titleClass }">
                <div class="my-header">
                    <h1 :id="titleId" :class="titleClass" style="font-size: 30px">加密搜索结果</h1>
                </div>
            </template>
            <el-table :data="tableData" :key="tableUpdate" style="width: 100%;font-size: 18px" height="435" stripe
                      border>
                <el-table-column fixed prop="id" label="ID" width="60" align="center"/>
                <el-table-column prop="keyword" label="关键词" width="100" align="center"/>
                <el-table-column label="密文结果" align="center">
                    <el-table-column prop="inv_idx1" label="密文结果1" align="center"/>
                    <el-table-column prop="inv_idx2" label="密文结果2" align="center"/>
                    <el-table-column prop="inv_idx3" label="密文结果3" align="center"/>
                    <el-table-column prop="inv_idx4" label="密文结果4" align="center"/>
                </el-table-column>
            </el-table>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="warning" style="font-size: 18px;height: 50px;width: 120px"
                           @click="exportXlsx()">一键导出</el-button>
                <el-button type="primary" style="font-size: 18px;height: 50px;width: 120px"
                           @click="dialogVisible = false;router.push('/result');">
                  结果分析
                </el-button>
              </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import {onMounted, reactive, ref} from 'vue';
import {Plus, Refresh, Search} from '@element-plus/icons-vue';
import {ElMessage, ElMessageBox, FormInstance, FormRules} from "element-plus";
import {useRouter} from "vue-router";
import {requestData} from "../api";
import * as XLSX from "xlsx";
import * as echarts from "echarts";

// 表单变量
const formRef = ref<FormInstance>();
const rules: FormRules = {
    Keywords: [{required: true, message: '请选择需要的搜索关键词', trigger: 'blur'}],
    QueryDB: [{required: true, message: '请选择搜索的数据库', trigger: 'blur'}],
    QueryMode: [{required: true, message: '请选择需要的搜索模式', trigger: 'blur'}],
};

const searchQuery = reactive<{
    Keywords: KeywordItem[]
    QueryDB: string
    QueryMode: string
}>({
    Keywords: [
        {
            key: 0,
            value: ''
        },
    ],
    QueryDB: '',
    QueryMode: ''
})

interface KeywordItem {
    key: number
    value: string
}


// 增减关键词输入框
const addSearch = () => {
    if (searchQuery.Keywords.length !== 8) {
        searchQuery.Keywords.push({
            key: searchQuery.Keywords.length,
            value: '',
        })
    } else {
        ElMessage({
            message: 'Warning! 最多支持8个关键词',
            type: 'warning',
        })
    }
}
const delSearch = (item: KeywordItem) => {
    const index = searchQuery.Keywords.indexOf(item)
    if (index !== 0) {
        searchQuery.Keywords.splice(index, 1)
    } else {
        ElMessage({
            message: 'Warning! 最少需要1个关键词',
            type: 'warning',
        })
    }
}
const router = useRouter();
// 搜索结果弹出框
const dialogVisible = ref(false)
const tableUpdate = ref(false)
const handleClose = (done: () => void) => {
    ElMessageBox.confirm('确定要关闭此窗口吗？')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}

interface TableItem {
    id: number,
    keyword: string,
    inv_idx1: string,
    inv_idx2: string,
    inv_idx3: string,
    inv_idx4: string
}

const tableData = ref<TableItem[]>([])

// 搜索次数增加
const serachTotalUp = () => {
    const last = localStorage.getItem("serachTotal")
    if (last === null) {
        localStorage.setItem("serachTotal", "1")
    } else {
        localStorage.setItem("serachTotal", (parseInt(last) + 1).toString())
    }
}
// 调取已有数据库内容
const dbOptions = []
const dbNames = localStorage.getItem("dbName")
if (dbNames != null) {
    const dbNames_lst = JSON.parse(dbNames)
    let idx
    for (idx in dbNames_lst) {
        let dbn = dbNames_lst[idx]
        dbOptions.push({value: dbn, label: dbn,})
    }
}
// 提交搜索表单
const onSubmit = (formEl: FormInstance | undefined) => {
    // 表单校验
    if (!formEl) return;
    formEl.validate((valid) => {
        if (valid) {
            serachTotalUp()
            searchData()
            dialogVisible.value = true
            // console.log(searchQuery);
            ElMessage.success('搜索成功！');
            onReset(formEl)
        } else {
            ElMessage.error('出错啦！请重新搜索！');
            return false;
        }
    });
};

const request = reactive({
    url: '',
    method: 'post',
    query: {}
})
const searchData = () => {
    request.url = '/search/';
    request.query = searchQuery;
    console.log(searchQuery)
    requestData(request)!.then(res => {
        // tableData.value = []
        tableData.value = res.data.search_data
        tableUpdate.value = !tableUpdate.value
    });
}


// 重置表单
const onReset = (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    formEl.resetFields();
};
const list = [['序号', '关键词', '密文结果1', '密文结果2', '密文结果3', '密文结果4']];

const exportXlsx = () => {
    tableData.value.map((item: any, i: number) => {
        const arr: any[] = [i + 1];
        arr.push(...[item.keyword, item.inv_idx1, item.inv_idx2, item.inv_idx3, item.inv_idx4]);
        list.push(arr);
    });
    let WorkSheet = XLSX.utils.aoa_to_sheet(list);
    let new_workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(new_workbook, WorkSheet, '第一页');
    XLSX.writeFile(new_workbook, `SE.xlsx`);
};

interface ChartItem {
    words: string[],
    count: number[],
}

const chartData = ref<ChartItem>()

const countWords = () => {
    request.url = '/countWords/';
    request.query = {};
    requestData(request)!.then(res => {
        chartData.value = res.data.countWords_data
    })
}
countWords()
onMounted(async () => {
    setTimeout(function () {
        const myChart = echarts.init(document.getElementById('chart'));
        myChart.setOption({
            title: {
                text: '关键词查询次数统计',
                left: 'center',
                textStyle: {
                    fontSize: 30
                }
            },
            tooltip: {},
            xAxis: {
                data: chartData.value?.words,
                axisLabel: {
                    fontSize: 20
                }
            },
            yAxis: [
                {
                    type: 'value',
                    name: '查询次数',
                    min: 0,
                    max: 150,
                    position: 'left',
                    axisLabel: {
                        formatter: '{value} 次',
                        fontSize: 22
                    }
                },
            ],
            series: [

                {
                    name: "搜索次数",
                    type: 'bar',
                    data: chartData.value?.count,
                    smooth: true,
                    yAxisIndex: 0,
                    barWidth: '50%',
                    itemStyle: {
                        normal: {
                            label: {
                                show: true,
                                position: 'top',
                                fontSize: 22
                            },
                            color: function (params: { dataIndex: number; }) {
                                const color = ['#3fb1e3', '#6be6c1', '#96dee8', '#a0a7e6', '#c4ebad']
                                return color[params.dataIndex]
                            }
                        }
                    }
                },
            ],
        });
    }, 500)
})


</script>

<style scoped>

.icon {
    margin-left: 10px;
}

.input-num {
    text-align: center;
    margin: 20px auto;
    width: 60%;
}

.handle-input {
    font-size: 22px;
    width: 300px;
    margin-right: 30px;
    text-align: center;
}

.large1 {
    font-size: 24px;
    margin: 30px 40px;
}

.large2 {
    font-size: 24px;
    margin: 40px 40px;
}

.my-header h1 {
    font-size: 26px;
    margin-top: 15px;
}

.demonstration {
    text-align: center;
    margin: 0 auto;
    color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
    color: #475669;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
    text-align: center;
}

::v-deep .el-form .el-form-item__label {
    font-size: 30px;
    color: black;
}

.handle-input {
    height: 50px;
    width: 300px;
}

.mt-2 {
    font-size: 25px;
}

::v-deep .el-table .el-table__label {
    font-size: 25px !important;
}
</style>