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
					<button size="mini" class="btnCommon">返回首页</button>
					<button type="primary" size="mini" class="btnPrimary">开始咨询</button>
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
			successText:'支付成功'
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
