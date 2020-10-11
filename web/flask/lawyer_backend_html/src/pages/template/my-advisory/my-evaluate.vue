<template>
	<view style="width: 100%;">
		<view class="example-box example-body">
			<view class="uni-padding-wrap uni-common-mt">
				<form>
					<view class="uni-media-list">
						<view class="uni-comment-face"><image src="../../../static/image/img1.png" class="iconTips"></image></view>
						<view class="uni-comment-body">
							<view class="uni-comment-top"><text>律师</text></view>
							<!-- <view class="uni-media-list-text-time"><text>从业律师10年</text></view> -->
							<view class="fontCol666 fontSize12">2019-11-11 付费咨询</view>
							<view><uni-rate :value="2" :size="22" @change="onChange" /></view>
						</view>
					</view>
					<view class="evaluateBox">
						<view class="uni-textarea"><textarea placeholder="感觉律师的回答有帮助么？分享下体验吧~" /></view>
					</view>
					<view class="table-btn-view bttomBox"><button class="save-btn" type="primary" form-type="submit">提交</button></view>
				</form>
			</view>
		</view>
		<view class="formBox">
			<label class="radio">
				<radio value="r2" @change="handleChange"/>
				匿名评价
			</label>
			
		</view>
	</view>
</template>

<script>
import uniRate from '@/components/uni-rate/uni-rate.vue';
// import { upQuestion, getType } from '@/api/index.js';
export default {
	components: {
		uniRate
	},
	data() {
		return {
			gradeData: '2'
		};
	},
	onLoad() {
		// this.GetType();
	},
	methods: {
		// 表单提交
		handleSub: function(e) {},
		// 触发评分
		onChange(e) {
			console.log('rate发生改变:' + JSON.stringify(e));
			this.gradeData = e.value;
		},
		handleChange(){
			
		}
	}
};
</script>

<style>
 .order-btn {
	display: block;
	width: 100%;
	height: 90upx;
	line-height: 90upx;
	text-align: center;
	color: white;
	font-size: 32upx;
	background-color: #e11c1c;
	border-radius: 20upx;
	margin: 0upx auto;
}
.input_text {
	width: 100%;
	height: 100upx;
	margin: 20upx auto;
	background-color: #fff;
	border-radius: 20upx;
}
.input_text input {
	border: none;
	border-radius: 16upx;
	padding: 20upx;
}
::-webkit-input-placeholder {
	color: #ccc;
	font-size: 14px;
}
.text {
	width: 100%;
	height: 300upx;
	margin: 10upx auto;
	/* overflow-y: scroll; */
	position: relative;
	padding: 0 0 30px;
}
.text textarea {
	width: 100%;
	height: 300upx;
	background-color: #fff;
	border-radius: 20upx;
	border: none;
	padding: 20upx;
	padding: 0;
}
.text .text_right {
	position: absolute;
	right: 50upx;
	margin-top: -60upx;
	font-size: 14px;
	display: flex;
	bottom: 0;
}
.textInput {
	position: relative;
}
.uni-form .textInput .uni-input {
	padding-right: 40px;
}
.textInput .text_right {
	position: absolute;
	right: 10upx;
	margin-top: 15upx;
	font-size: 14px;
	display: flex;
}
</style>
