<template>
	<view class="footer">
		<!-- <view class="footer-left">
			<view class="uni-icon uni-icon-mic" @tap="startRecognize"> </view>
		</view> -->
		<view class="footer-center">
			<input class="input-text" type="text" v-model="inputValue"></input>
		</view>
		<view class="footer-right" @tap="sendMessge">
			<view id='msg-type' >发送</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: "chat-input",
		data() {
			return {
				inputValue: ''
			}
		},
		methods: {
			startRecognize: function () {
				var options = {};
				var that = this;
				options.engine = 'iFly';
				that.inputValue = "";
				plus.speech.startRecognize(options, function (s) {
					console.log(s);
					that.inputValue += s;
				}, function (e) {
					console.log("语音识别失败：" + e.message);
				});
			},
			sendMessge: function () {
				var that = this;
				if (that.inputValue.trim() == '') {

					that.inputValue = '';
				} else {

					//点击发送按钮时，通知父组件用户输入的内容
					this.$emit('send-message', {
						type: 'text',
						content: that.inputValue
					});
					that.inputValue = '';
				}
			}
		}
	}
</script>

<style>
	@import "../../common/icon.css";

	.footer {
		display: flex;
		flex-direction: row;
		/* width: 100%; */
		height: 43px;
		min-height: 43px;
		border-top: solid 1px #e2e2e2;
		overflow: hidden;
		padding: 8px;
		background-color: #f6f6f6;
	}
	.footer-left {

		width: 80px;
		height: 80px;

		display: flex;
		justify-content: center;
		align-items: center;
	}
	.footer-right {
		width: 60px;
		height: 36px;
		display: flex;
		justify-content: center;
		align-items: center;
		color: #fff;
		background: #2e82ff;
		border-radius: 8px;
		margin: 4px 0 0 8px;
	}
	.footer-center {
		flex: 1;
		height: 45px;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.footer-center .input-text {
		flex: 1;
		background: #fff;
		/* border: solid 1px #ddd; */
		padding: 8px !important;
		font-family: verdana !important;
		overflow: hidden;
		border-radius: 8px;
	}
</style>
