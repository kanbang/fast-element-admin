<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2023-05-26 08:49:32
 * @LastEditors: zhai
 * @LastEditTime: 2023-05-30 12:54:23
-->
<template>
	<div class="layout-footer pb15">
		<div class="layout-footer-warp">
			<div>fast-element-admin，Made by bzx with ❤️</div>
			<div class="mt5">版权所有</div>
		</div>
	</div>
</template>

<script setup lang="ts" name="layoutFooter">
// 此处需有内容（注释也得），否则缓存将失败
</script>

<style scoped lang="scss">
.layout-footer {
	width: 100%;
	display: flex;
	&-warp {
		margin: auto;
		color: var(--el-text-color-secondary);
		text-align: center;
		animation: error-num 0.3s ease;
	}
}
</style>
