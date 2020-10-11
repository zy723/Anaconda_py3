<template>
	<!-- <view class="m-item" :id="'message'+id">
		<view class="m-left">
			<image class="head_icon" :src="abosultPaht+user.home.img" v-if="message.user=='home'"></image>
		</view>
		<view class="m-content">
			<view class="m-content-head" :class="{'m-content-head-right':message.user=='customer'}">
				<view :class="'m-content-head-'+message.user">{{message.content}} </view>
			</view>
		</view>
		<view class="m-right">
			<image class="head_icon" :src="abosultPaht+user.customer.img" v-if="message.user=='customer'"></image>
		</view>
	</view> -->
	<view class="m-item">
		<view class="m-left">
			<image class="head_icon" src="../../static/image/customerHL.png"></image>
		</view>
		<view class="m-content">
			<view class="m-content-head" :class="{'m-content-head-right':message.user=='customer'}">
				<view :class="'m-content-head-'+message.user">你好</view>
			</view>
		</view>
		<view class="m-right">
			<image class="head_icon" src="../../static/image/customerHL.png" v-if="message.user=='customer'"></image>
		</view>
	</view>
</template>

<script>
	import {
		mapState
	} from 'vuex'

	export default {
		data() {
			return {
				abosultPaht: "../../"
			}
		},
		props: ['message', 'id'],
		computed: mapState(['user'])
	}
</script>

<style>
	.m-item {
		display: flex;
		flex-direction: row;
		padding-top: 40px;
	}
	.m-left {
		display: flex;
		width: 120upx;
		justify-content: center;
		align-items: flex-start;
	}
	.m-content {
		display: flex;
		flex: 1;
		flex-direction: column;
		justify-content: center;
		word-break: break-all;
	}
	.m-right {
		display: flex;
		width: 120upx;
		justify-content: center;
		align-items: flex-start;
	}
	.head_icon {
		width: 80upx;
		height: 80upx;
	}
	.m-content-head {
		position: relative;
	}
	.m-content-head-right {
		display: flex;
		justify-content: flex-end;
	}
	.m-content-head-home {
		text-align: left;
		background: #f5f5f5;
		border: 1px #f5f5f5 solid;
		border-radius: 10px;
		padding: 10px;
		color: #444;
	}
	/* .m-content-head-home:before {
		border: 15px solid transparent;
		border-right: 15px solid #1482d1;
		left: -26px;
		width: 0;
		height: 0;
		position: absolute;
		content: ' '
	} */
	.m-content-head-customer {
		border: 1px #cee2ff solid;
		background: #cee2ff;
		border-radius: 10px;
		padding: 10px;
	}
	/* .m-content-head-customer:after {
		border: 15px solid transparent;
		border-left: 15px solid white;
		top: 20px;
		right: -26px;
		width: 0;
		height: 0;
		position: absolute;
		content: ' '
	} */
</style>
