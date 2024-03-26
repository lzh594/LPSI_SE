<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="12">
                <el-card shadow="hover" style="height: 750px;margin-top: 30px">
                    <h3 class="upload-title">选择上传至服务器的数据库文件</h3>
                    <el-upload
                        ref="uploadRef"
                        class="upload-demo"
                        action="http://localhost:8000/SE/uploadFile/"
                        method="post"
                        drag
                        :on-change="handle"
                        :auto-upload="false"
                    >
                        <template #trigger>
                            <el-icon style="font-size: 50px" class="el-icon--upload">
                                <upload-filled/>
                            </el-icon>
                            <div class="el-upload__text">
                                <el-button type="primary" style="font-size: 30px; height: 70px; width: 333px">点击以上传数据文件</el-button>
                            </div>
                        </template>
                        <template #tip>
                            <div class="el-upload__tip" style="font-size: 30px;margin-left: 130px; margin-top: 50px">
                                json/csv文件（不超10M）
                            </div>
                        </template>
                    </el-upload>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card shadow="hover" style="height: 750px;margin-top:30px">
                    <el-form
                        ref="formRef"
                        :rules="rules"
                        :model="form"
                        size="large"
                        :hide-required-asterisk="true"
                        id="selectForm"
                        style="margin: 40px 0">
                        <div class="label">
                            <el-icon :size="30"><MessageBox /></el-icon>
                            <span class="span-content">上传数据库</span>
                        </div>
                        <el-form-item prop="dbName">
                            <el-input v-model="form.dbName" placeholder="请输入数据库名称" style="margin-left: 50px"/>
                        </el-form-item>

                        <div class="label">
                            <el-icon :size="30"><Lock /></el-icon>
                            <span class="span-content">加密算法</span>
                        </div>
                        <el-form-item prop="Encode" class="el-form-item__label">
                            <el-select v-model="form.Encode" placeholder="请选择你的加密算法"
                                       style="height: 50px;width: 260px;" size="large">
                                <el-option label="SM4" value="SM4"/>
                                <el-option label="AES" value="AES"/>
                            </el-select>
                        </el-form-item>

                        <div class="label">
                            <el-icon :size="30"><Tools /></el-icon>
                            <span class="span-content">工作模式</span>
                        </div>
                        <el-form-item prop="Mode" class="el-form-item__label">
                            <el-radio-group v-model="form.Mode">
                                <el-radio label="ECB"/>
                                <el-radio label="CBC"/>
                                <el-radio label="CFB"/>
                                <el-radio label="OFB"/>
                                <el-radio label="CTR"/>
                            </el-radio-group>
                        </el-form-item>

                        <div class="label">
                            <el-icon :size="30"><Memo /></el-icon>
                            <span class="span-content">安全参数</span>
                        </div>
                        <el-form-item prop="Len" class="el-form-item__label">
                            <el-radio-group v-model="form.Len">
                                <el-radio label="128"/>
                                <el-radio v-if="form.Encode=='AES'" label="192"/>
                                <el-radio v-if="form.Encode=='AES'" label="256"/>
                            </el-radio-group>
                        </el-form-item>

                        <div class="label">
                            <el-icon :size="30"><Key /></el-icon>
                            <span class="span-content">对称密钥</span>
                        </div>
                        <el-form-item prop="Key" class="el-form-item__label">
                            <el-upload
                                class="upload-demo"
                                ref="uploadRef2"
                                :auto-upload="false"
                                action="http://localhost:8000/"
                            >
                                <el-button type="primary" style="height: 45px ;width: 160px; font-size: 26px">一键导入</el-button>
                            </el-upload>
                        </el-form-item>
                    </el-form>
                    <el-button size="large" style="margin: 1px 200px;height: 50px; width: 180px; font-size: 30px" type="success"
                               @click="dialogVisible=true">
                        加密文件
                    </el-button>
                </el-card>
            </el-col>
        </el-row>
        <el-dialog
            v-model="dialogVisible"
            width="60%"
            center
            :before-close="handleClose"
        >
            <template #header="{ close, titleId, titleClass }">
                <div class="my-header">
                    <h1 :id="titleId" :class="titleClass" style="font-size: 35px;margin-top: 30px">数据库加密成功</h1>
                </div>
            </template>
            <el-descriptions
                class="margin-top"
                size="large"
                :column="2"
                border>
                <template #title>
                    <el-tag type="success" style="width: 250px;height: 60px;font-size: 30px;">加密数据库信息</el-tag>
                </template>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <el-icon :style="iconStyle">
                                <Postcard/>
                            </el-icon>
                            数据库名称
                        </div>
                    </template>
                        {{ form.dbName }}
                </el-descriptions-item>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <el-icon :style="iconStyle">
                                <Key/>
                            </el-icon>
                            加密算法
                        </div>
                    </template>
                    {{ form.Encode }}
                </el-descriptions-item>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <el-icon :style="iconStyle">
                                <Connection/>
                            </el-icon>
                            工作模式
                        </div>
                    </template>
                    {{ form.Mode }}
                </el-descriptions-item>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <el-icon :style="iconStyle">
                                <Operation/>
                            </el-icon>
                            安全参数
                        </div>
                    </template>
                    {{ form.Len }}
                </el-descriptions-item>
            </el-descriptions>
            <template #footer>
                <div style="margin: 20px auto;text-align: center;font-size: 18px">
                    是否上传该加密数据库至服务器
                </div>
                <span class="dialog-footer">
                    <el-button style="font-size: 16px;height: 50px;width: 80px" @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" style="font-size: 16px;height: 50px;width: 80px" @click="onSubmit(formRef);">
                        上传
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import {Connection, Operation, UploadFilled} from "@element-plus/icons-vue";
import {computed, reactive, ref} from "vue";

const uploadRef = ref<UploadInstance>()
const uploadRef2 = ref<UploadInstance>()
import type {FormInstance, FormRules, UploadInstance} from 'element-plus'
import {ElMessage, ElMessageBox} from "element-plus";
import {requestData} from "../api";

const dialogVisible = ref(false)
const formRef = ref<FormInstance>();

const form = reactive({
    dbName: '',
    Encode: '',
    Mode: '',
    Len: '',
})
const rules: FormRules = {
    dbName: [{required: true, message: '请输入此数据库的名称', trigger: 'blur'}],
    Encode: [{required: true, message: '请选择需要的加密算法', trigger: 'blur'}],
    Mode: [{required: true, message: '请选择需要的工作模式', trigger: 'blur'}],
    Len: [{required: true, message: '请选择需要的密钥长度', trigger: 'blur'}],
    Key: [{required: false, message: '请上传加密密钥', trigger: 'blur'}],
};
const handle = (rawFile: any) => {
    console.log(rawFile);
};
const dbNumUp = () => {
    const last = localStorage.getItem("dbNums")
    if (last === null) {
        localStorage.setItem("dbNums", "1")
    } else {
        localStorage.setItem("dbNums", (parseInt(last) + 1).toString())
    }
}
const dbNameUp = () => {
    const last = localStorage.getItem("dbName")
    console.log("all databases")
    console.log(last)
    if (last === null) {
        localStorage.setItem("dbName", JSON.stringify([form.dbName]))
    } else {
        const dbName_lst = JSON.parse(last)
        if (dbName_lst.indexOf(form.dbName) === -1) {
            dbName_lst.push(form.dbName)
            console.log(dbName_lst)
            localStorage.setItem("dbName", JSON.stringify(dbName_lst))
        }
    }
}
const request = reactive({
    url: '',
    method: 'post',
    query: {}
})
const uploadData = () => {
    request.url = '/upload/';
    request.query = form;
    requestData(request)!.then(res => {
    });
}
const submitUpload = () => {
    uploadRef.value!.submit()
    uploadRef2.value!.submit()
    uploadData()
    dbNumUp()
    dbNameUp()
}

// 提交
const onSubmit = (formEl: FormInstance | undefined) => {
    // 表单校验
    if (!formEl) return;
    formEl.validate((valid) => {
        if (valid) {
            submitUpload()
            dialogVisible.value = false
            console.log(form);
            ElMessage.success('上传成功！');
            onReset(formEl)
        } else {
            ElMessage.error('出错啦！请重新上传！');
            return false;
        }
    });
};
const onReset = (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    formEl.resetFields();
};
const handleClose = (done: () => void) => {
    ElMessageBox.confirm('确定要关闭此窗口吗？')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}
const iconStyle = computed(() => {
    const marginMap = {
        large: '20px',
    }
    return {
        marginRight: marginMap.large,
    }
})
</script>

<style scoped>


.upload-title {
    margin: 40px 80px;
    color: #1f2f3d;
    font-size: 33px;
    text-align: center;
}

.upload-demo {
    margin: 0 auto;
    width: 100%;
    height: 100%;
}

.el-icon--upload {
    margin: 137px 160px;
    text-align: center;
}

.el-descriptions {
    margin-top: 20px;
}

.cell-item {
    font-size: 25px;
    display: flex;
    align-items: center;
}

.margin-top {
    margin-top: 20px;
}

.span-content {
    font-size: 28px;
    margin-left: 10px;
}

.label {
    margin-left: 20px;
    margin-bottom: 20px;
}

::v-deep .el-form .el-form-item__label {
    margin-left: 50px;
}

::v-deep .el-radio .el-radio__label{
    font-size: 21px !important;
}
</style>
