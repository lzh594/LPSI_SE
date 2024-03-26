<template>
	<div class="error-page">
        <div>
            <el-image style="width: 590px; height: 200px;" :src="SE1000Img" :fit="'contain'" />
        </div>
		<div class="error-code">4<span>0</span>4</div>
		<div class="error-desc">啊哦~ 你所访问的页面不存在</div>
        <div class="error-desc">你来到了没有知识的荒野哦！</div>

        <div class="error-handle">
			<router-link to="/">
				<el-button type="primary" size="large">返回登录首页</el-button>
			</router-link>
			<el-button class="error-btn" type="primary" size="large" @click="goBack">返回上一页</el-button>
		</div>
	</div>
</template>

<script setup lang="ts" name="404">
import { useRouter } from 'vue-router';
import SE1000Img from "../assets/img/1000_260.png";

const router = useRouter();
const goBack = () => {
	router.go(-1);
};
</script>

<style scoped>
.error-page {
	display: flex;
	justify-content: center;
    margin-top: 60px;
	align-items: center;
	flex-direction: column;
	width: 100%;
	height: 100%;
	background: white;
	box-sizing: border-box;
}
.error-code {
	line-height: 1;
	font-size: 250px;
	font-weight: bolder;
	color: #2d8cf0;
}
.error-code span {
	color: #00a854;
}
.error-desc {
    margin: 20px;
    text-align: center;
	font-size: 36px;
	color: #777;
}
.error-handle {
	margin-top: 30px;
	padding-bottom: 200px;
}
.error-btn {
	margin-left: 100px;
}
</style>
