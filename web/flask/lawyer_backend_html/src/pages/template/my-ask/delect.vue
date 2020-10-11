<template>
	<view style="width: 100%;">
		<view class="payBox example-body">
			<view class="success">
				<view class="tipBox">
					<div class="successBox" v-if="successShow"></div>
					<div class="errorBox" v-else></div>
					<p>{{successText}}</p>
				</view>
				<view class="btnBox">
					<router-link to="/pages/template/my-ask/ask-list" class="default">返回列表</router-link>
					<router-link to="/pages/template/my-ask/ask">重新提问</router-link>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	components: {},
	data() {
		return {
			successShow: true,
			successText:'删除成功'
		};
		
	},
	onLoad() {},
	methods: {
		handleBuy: function(e) {
			uni.navigateTo({
				url: '/pages/template/ask-details/ask-details?id=' + e.id
			});
		}
	}
};
</script>

<style scoped>
page {
	background-color: #fff !important;
}
</style>
