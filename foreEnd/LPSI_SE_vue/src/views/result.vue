<template>
    <div>
        <div class="container">
            <div class="handle-box">
                <el-form ref="formRef" :model="form" size="large" :rules="rules" label-width="auto"
                         :hide-required-asterisk="true">
                    <el-form-item label="结果密文" prop="Cipher" v-model="form.Cipher" class="el-form-item__label">
                        <el-upload
                            class="upload-demo"
                            ref="uploadRef"
                            action="http//localhost:8000/"
                            style="margin: 0 40px;"
                            :auto-upload="false"
                        >
                            <el-button type="primary" style="height: 45px;width: 160px; font-size: 25px">一键导入
                            </el-button>
                        </el-upload>
                    </el-form-item>
                    <el-form-item label="解密算法" prop="Decode" class="el-form-item__label">
                        <el-select v-model="form.Decode" placeholder="请选择您的解密算法" size="large" style="margin-left: 15px">
                            <el-option label="SM4" value="SM4"/>
                            <el-option label="AES" value="AES"/>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="工作模式" prop="Mode" class="el-form-item__label">
                        <el-radio-group v-model="form.Mode" style="margin-left: 15px">
                            <el-radio label="ECB"/>
                            <el-radio label="CBC"/>
                            <el-radio label="CFB"/>
                            <el-radio label="OFB"/>
                            <el-radio label="CTR"/>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="安全参数" prop="Len" class="el-form-item__label">
                        <el-radio-group v-model="form.Len" style="margin-left: 15px">
                            <el-radio label="128"/>
                            <el-radio v-if="form.Decode=='AES'" label="192"/>
                            <el-radio v-if="form.Decode=='AES'" label="256"/>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="对称密钥" prop="CipherKey" v-model="form.CipherKey"
                                  class="el-form-item__label">
                        <el-upload
                            class="upload-demo"
                            ref="uploadRef"
                            action="http://localhost:8000/"
                            style="margin: 0 40px;"
                            :auto-upload="false"
                        >
                            <el-button type="primary" style="height: 45px;width: 160px; font-size: 25px">一键导入
                            </el-button>
                        </el-upload>
                    </el-form-item>
                    <el-form-item label="输出文件格式" prop="Format" class="el-form-item__label">
                        <el-radio-group v-model="form.Format" style="margin-left: 15px">
                            <el-radio label="txt"/>
                            <el-radio label="json"/>
                            <el-radio label="xlsx"/>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="备注信息" prop="Tips" class="el-form-item__label">
                        <el-input v-model="form.Tips" placeholder="这里随心写～" size="large" type="textarea"
                                  style="font-size: 25px; height: 50px; margin-left: 15px"/>
                    </el-form-item>
                </el-form>
                <div class="dec-btn">
                    <el-button style="height: 60px;width: 180px;font-size: 30px;" round type="success"
                               @click="onSubmit(formRef);">
                        一键解密
                    </el-button>
                </div>
            </div>
            <el-dialog
                v-model="dialogVisible"
                style="font-size: 28px"
                width="60%"
                center
                :before-close="handleClose"
            >
                <template #header="{ close, titleId, titleClass }">
                    <div class="my-header">
                        <h1 :id="titleId" :class="titleClass" style="font-size: 30px">解密结果</h1>
                    </div>
                </template>
                <el-descriptions column="1" size="large" border="border" style="height: 300px; margin-top: 15px">
                    <el-descriptions-item label="id" label-align="center" align="center">
                        {{ tableData[0]["id"] }}
                    </el-descriptions-item>
                    <el-descriptions-item label="解密结果1" label-align="center" align="center">
                        {{ tableData[0]["dec_inv_idx1"] }}
                    </el-descriptions-item>
                    <el-descriptions-item label="解密结果2" label-align="center" align="center">
                        {{ tableData[0]["dec_inv_idx2"] }}
                    </el-descriptions-item>
                    <el-descriptions-item label="解密结果3" label-align="center" align="center">
                        {{ tableData[0]["dec_inv_idx3"] }}
                    </el-descriptions-item>
                    <el-descriptions-item label="解密结果4" label-align="center" align="center">
                        {{ tableData[0]["dec_inv_idx4"] }}
                    </el-descriptions-item>
                </el-descriptions>
                <template #footer>
              <span class="dialog-footer">
                <el-button type="primary" style="font-size: 23px;height: 55px;width: 125px;"
                           @click="exportXlsx();dialogVisible = false;">一键导出</el-button>
              </span>
                </template>
            </el-dialog>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {reactive, ref} from 'vue'
import {ElMessage, ElMessageBox, FormInstance, FormRules, UploadInstance} from "element-plus";
import {requestData} from "../api";
import * as XLSX from "xlsx";

// do not use same name with ref
const form = reactive({
    Cipher: '',
    Decode: '',
    Mode: '',
    Len: '',
    CipherKey: '',
    Format: '',
    Tips: '',
})
const formRef = ref<FormInstance>();
const rules: FormRules = {
    Cipher: [{required: false, message: '请选择需要解密的密文', trigger: 'blur'}],
    Decode: [{required: true, message: '请选择需要的解密算法', trigger: 'blur'}],
    Mode: [{required: true, message: '请选择需要的工作模式', trigger: 'blur'}],
    Len: [{required: true, message: '请选择需要的安全参数', trigger: 'blur'}],
    CipherKey: [{required: false, message: '请选择需要的解密密钥', trigger: 'blur'}],
    Format: [{required: true, message: '请选择需要的导出格式', trigger: 'blur'}],
    Tips: [{required: false, message: '请随意填写', trigger: 'blur'}],
};

interface TableItem {
    id: number,
    dec_inv_idx1: string,
    dec_inv_idx2: string,
    dec_inv_idx3: string,
    dec_inv_idx4: string
}

const tableData = ref<TableItem[]>([
    {
        id: 1,
        dec_inv_idx1: 'dec_inv_idx1',
        dec_inv_idx2: 'dec_inv_idx2',
        dec_inv_idx3: 'dec_inv_idx3',
        dec_inv_idx4: 'dec_inv_idx4'
    },
])

// 搜索结果弹出框
const dialogVisible = ref(false)
// 表格刷新
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
const request = reactive({
    url: '',
    method: 'post',
    query: {}
})
const resultData = () => {
    request.url = '/result/';
    request.query = form;
    requestData(request)!.then(res => {
        // tableData.value = []
        tableData.value = res.data.result_data
        tableUpdate.value = !tableUpdate.value
    });
}
const uploadRef = ref<UploadInstance>()

const onSubmit = (formEl: FormInstance | undefined) => {
    // 表单校验
    if (!formEl) return;
    formEl.validate((valid) => {
        if (valid) {
            uploadRef.value!.submit()
            resultData()
            dialogVisible.value = true
            ElMessage.success('解密成功！');
            onReset(formEl)
        } else {
            ElMessage.error('出错啦！请检查后重新解密！');
            return false;
        }
    });
}
// 重置表单
const onReset = (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    formEl.resetFields();
};
// 导出数据
const list = [['序号', '解密结果1', '解密结果2', '解密结果3', '解密结果4']];
const exportXlsx = () => {
    tableData.value.map((item: any, i: number) => {
        const arr: any[] = [i + 1];
        arr.push(...[item.dec_inv_idx1, item.dec_inv_idx2, item.dec_inv_idx3, item.dec_inv_idx4]);
        list.push(arr);
    });
    let WorkSheet = XLSX.utils.aoa_to_sheet(list);
    let new_workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(new_workbook, WorkSheet, '第1页');
    XLSX.writeFile(new_workbook, `result.xlsx`);
};
</script>
<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 150px;
}

.table {
    width: 100%;
    font-size: 14px;
}

.red {
    color: #F56C6C;
}

.mr20 {
    margin-right: 20px;
}

.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}

.dec-btn {
    margin: 30px auto;
    text-align: center;
}

::v-deep .el-form .el-form-item__label {
    font-size: 30px;
    width: 100%;
    margin-bottom: 60px;
    color: black;
}

::v-deep .el-radio .el-radio__label {
    font-size: 28px !important;
}

::v-deep .el-descriptions .el-descriptions__label{
    font-size: 25px !important;
}

::v-deep .el-descriptions .el-descriptions__cell {
    font-size: 25px !important;
}
</style>
