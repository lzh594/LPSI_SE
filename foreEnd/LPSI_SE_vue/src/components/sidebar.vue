<template>
    <div class="sidebar">
        <el-menu
            class="sidebar-el-menu"
            :default-active="onRoutes"
            :collapse="sidebar.collapse"
            background-color="#324157"
            text-color="#bfcbd9"
            active-text-color="#20a0ff"
            unique-opened
            router
        >
            <template v-for="(item, index) in items">
                <template
                    class="item"
                    v-if="identity === '1' && (item.index !== '/intersection')">
<!--                    v-if="identity === '1' && (item.index === '/dashboard' || item.index === '/intersection' || item.index === '/data' || item.index === '/result') || identity === '0' && (item.index === '/dashboard' || item.index === '/SE')">-->
                    <el-menu-item :index="item.index" :key="item.index" v-permiss="item.permiss" style="margin-bottom: 20px">
                        <el-icon size="28">
                            <component :is="item.icon"></component>
                        </el-icon>
                        <div v-if="sidebar.collapse===false" class="side-font">{{ item.title }}</div>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script setup lang="ts">
import {computed} from 'vue';
import {useSidebarStore} from '../store/sidebar';
import {useRoute} from 'vue-router';

const items = [
    {
        icon: 'Odometer',
        index: '/dashboard',
        title: '系统首页',
        permiss: '1',
    },
    {
        icon: 'Edit',
        index: '/data',
        title: ' 数据上传',
        permiss: '1',
    },
    {
        icon: 'Goods',
        index: '/SE',
        title: '加密搜索',
        permiss: '2',
    },
    {
        icon: 'Calendar',
        index: '/result',
        title: ' 结果分析',
        permiss: '6',
    },
    {
        icon: 'User',
        index: '/intersection',
        title: ' 求交运算',
        permiss: '2',
    },
];

const route = useRoute();
const onRoutes = computed(() => {
    return route.path;
});

const sidebar = useSidebarStore();
const identity = localStorage.getItem('ms_identity')
</script>

<style scoped>
.side-font {
    display: block;
    margin: 0 auto;
    font-size: 40px;
}

.sidebar {
    display: block;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    overflow-y: scroll;
    font-size: 120px;
}

.sidebar::-webkit-scrollbar {
    width: 0;
}

li {
    font-size: 28px;
    font-weight: bolder;
    font-family: "宋体", serif;
}

.sidebar-el-menu:not(.el-menu--collapse) {
    width: 250px;
}

.sidebar > ul {
    height: 100%;
}
</style>