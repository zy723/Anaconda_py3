<template>
	<view style="width: 100%;">
		<view class="payBox example-body">
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left"><text>订单编号</text></view>
						<view class="uni-triplex-right">ZX20190403003</view>
					</view>
				</view>
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left"><text>咨询律师</text></view>
						<view class="uni-triplex-right">韩琦</view>
					</view>
				</view>
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left"><text>咨询方式</text></view>
						<view class="uni-triplex-right">按次计费</view>
					</view>
				</view>
				<view class="uni-list-cell">
					<view class="uni-triplex-row">
						<view class="uni-triplex-left"><text>付费方式</text></view>
						<view class="uni-triplex-right">
							<i class="iconfont">&#xe616;</i>
							微信支付
						</view>
					</view>
				</view>
			</view>
			<view class="table-btn-view bttomBox">
				支付金额：￥ 100
				<button class="save-btn" type="primary" form-type="submit" @click="handleBuy">去支付</button>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	components: {},
	data() {
		return {};
	},
	// 监听页面加载，为上个页面传递的数据，用于页面传参
	onLoad() {
		// 重新定义标题
		uni.setNavigationBarTitle({
			title: '支付失败'
		});
	},
	methods: {
		handleBuy: function(e) {
			uni.navigateTo({
				url: '/pages/template/my-advisory/buySucceed'
			});
		}
	}
};
</script>

<style scoped>
.example-body {
	padding-bottom: 0;
}
.bttomBox{
	background: #fff;
	/* display: flex; */
	border-top: 1px solid #f1f1f1;
	line-height: 3;
	padding: 0 0 0 20px;
}
.bttomBox .save-btn {
	width: 30%;
	float: right;
}
.uni-triplex-right {
	width: 40%;
}
.uni-triplex-left {
	width: 60%;
}
</style>
